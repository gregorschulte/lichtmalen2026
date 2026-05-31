"""
LED Pixelstick for Light Painting
Pimoroni Plasma 2040 with 144 NeoPixel LED Strip
Controls: A=next image, B=start/restart, Boot=toggle loop/once mode
"""

import board
import neopixel
import digitalio
import time
import os
import struct

# Configuration
PLAYBACK_SPEED_MS = 20  # Column display duration in milliseconds (faster playback)
NUM_LEDS = 144
DEFAULT_MODE = "loop"  # "loop" or "once"
IMAGES_DIR = "/images"
LONG_PRESS_DURATION = 1.0  # Long press threshold in seconds

# Hardware setup
pixels = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=0.3, auto_write=False)

# Onboard LED setup for CircuitPython (try all possible LED pins)
onboard_leds = []
led_pins_to_try = [
    ('LED_R', 'LED_G', 'LED_B'),  # RGB LED pins
    ('GP16', 'GP17', 'GP18'),     # Alternative RGB pins  
    ('GP25',),                     # Single LED pin
    ('LED',),                      # Standard LED pin
    ('GP2',),                      # Alternative single LED
]

print("Detecting onboard LEDs...")
for pins in led_pins_to_try:
    try:
        if len(pins) == 3:  # RGB LED
            led_r = digitalio.DigitalInOut(getattr(board, pins[0]))
            led_g = digitalio.DigitalInOut(getattr(board, pins[1]))
            led_b = digitalio.DigitalInOut(getattr(board, pins[2]))
            led_r.direction = digitalio.Direction.OUTPUT
            led_g.direction = digitalio.Direction.OUTPUT
            led_b.direction = digitalio.Direction.OUTPUT
            # Turn them off immediately
            led_r.value = False
            led_g.value = False
            led_b.value = False
            onboard_leds.append(('rgb', led_r, led_g, led_b))
            print(f"Found RGB LED on pins {pins}")
        else:  # Single LED
            led = digitalio.DigitalInOut(getattr(board, pins[0]))
            led.direction = digitalio.Direction.OUTPUT
            led.value = False  # Turn it off immediately
            onboard_leds.append(('single', led))
            print(f"Found single LED on pin {pins[0]}")
    except AttributeError:
        continue

if onboard_leds:
    print(f"Total LEDs found: {len(onboard_leds)}")
else:
    print("Warning: No onboard LEDs detected")

# Button setup with CircuitPython 10 compatibility
# Button A
try:
    button_a = digitalio.DigitalInOut(board.SW_A)
except AttributeError:
    try:
        button_a = digitalio.DigitalInOut(board.BUTTON_A)
    except AttributeError:
        try:
            button_a = digitalio.DigitalInOut(board.GP12)  # Common button pin
        except AttributeError:
            print("Warning: Button A not found, functionality will be limited")
            button_a = None

if button_a:
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.UP

# Button B  
try:
    button_b = digitalio.DigitalInOut(board.SW_B)
except AttributeError:
    try:
        button_b = digitalio.DigitalInOut(board.BUTTON_B)
    except AttributeError:
        try:
            button_b = digitalio.DigitalInOut(board.GP13)  # Common button pin
        except AttributeError:
            print("Warning: Button B not found, functionality will be limited")
            button_b = None

if button_b:
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.UP

# Boot button removed - using long press on button B instead

class ImageManager:
    def __init__(self):
        self.images = []
        self.current_image_index = 0
        self.scan_images()
    
    def scan_images(self):
        """Scan for BMP files and sort alphabetically"""
        try:
            files = os.listdir(IMAGES_DIR)
            self.images = sorted([f for f in files if f.lower().endswith('.bmp')])
            print(f"Found {len(self.images)} BMP files")
        except OSError:
            print("Images directory not found")
            self.images = []
    
    def get_current_image(self):
        """Get current image filename"""
        if not self.images:
            return None
        return self.images[self.current_image_index]
    
    def next_image(self):
        """Switch to next image"""
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            return self.get_current_image()
        return None

class BMPReader:
    @staticmethod
    def read_bmp_header(filename):
        """Read BMP header to get image dimensions and format info"""
        try:
            with open(filename, 'rb') as f:
                # Read BMP file header (14 bytes) + DIB header (40+ bytes)
                header = f.read(54)
                
                # Extract width and height (little-endian)
                width = struct.unpack('<I', header[18:22])[0]
                height = struct.unpack('<I', header[22:26])[0]
                bits_per_pixel = struct.unpack('<H', header[28:30])[0]
                
                # Determine format and palette info
                format_info = {
                    'width': width,
                    'height': height,
                    'bits_per_pixel': bits_per_pixel,
                    'is_indexed': bits_per_pixel == 8,
                    'palette': None
                }
                
                # If 8-bit indexed, read the palette
                if bits_per_pixel == 8:
                    # Palette starts after header (at offset 54)
                    f.seek(54)
                    palette_data = f.read(256 * 4)  # 256 colors × 4 bytes (BGRA)
                    palette = []
                    for i in range(256):
                        # Extract BGR values (ignore alpha)
                        bgra = palette_data[i*4:(i+1)*4]
                        if len(bgra) >= 3:
                            b, g, r = bgra[0], bgra[1], bgra[2]
                            palette.append((r, g, b))
                        else:
                            palette.append((0, 0, 0))
                    format_info['palette'] = palette
                
                return format_info
        except Exception as e:
            print(f"Error reading BMP header: {e}")
            return None
    
    @staticmethod
    def read_bmp_column(filename, column, format_info):
        """Read a specific column from BMP file (supports 24-bit and 8-bit indexed)"""
        if not format_info:
            return [(0, 0, 0)] * NUM_LEDS
            
        width = format_info['width']
        height = format_info['height']
        is_indexed = format_info['is_indexed']
        palette = format_info.get('palette')
        
        try:
            with open(filename, 'rb') as f:
                column_data = []
                
                if is_indexed and palette:
                    # 8-bit indexed BMP
                    # Data starts after header + palette (54 + 256*4 = 1078 bytes)
                    data_offset = 54 + 256 * 4
                    
                    # Row size padded to 4 bytes
                    row_size = ((width + 3) // 4) * 4
                    
                    for row in range(height):
                        # Calculate position for this pixel (bottom-up in BMP)
                        pixel_row = height - 1 - row  # Flip to top-down
                        pos = data_offset + pixel_row * row_size + column
                        f.seek(pos)
                        
                        # Read palette index
                        index_data = f.read(1)
                        if len(index_data) == 1:
                            palette_index = index_data[0]
                            if palette_index < len(palette):
                                r, g, b = palette[palette_index]
                                column_data.append((r, g, b))
                            else:
                                column_data.append((0, 0, 0))
                        else:
                            column_data.append((0, 0, 0))
                
                else:
                    # 24-bit BMP (original format)
                    f.seek(54)  # Skip header
                    
                    # Row size padded to 4 bytes (3 bytes per pixel)
                    row_size = ((width * 3 + 3) // 4) * 4
                    
                    for row in range(height):
                        # Calculate position for this pixel (bottom-up in BMP)
                        pixel_row = height - 1 - row  # Flip to top-down
                        pos = 54 + pixel_row * row_size + column * 3
                        f.seek(pos)
                        
                        # Read BGR values
                        bgr = f.read(3)
                        if len(bgr) == 3:
                            # Convert BGR to RGB
                            r, g, b = bgr[2], bgr[1], bgr[0]
                            column_data.append((r, g, b))
                        else:
                            column_data.append((0, 0, 0))
                
                return column_data
                
        except Exception as e:
            print(f"Error reading BMP column: {e}")
            return [(0, 0, 0)] * height

class RainbowGenerator:
    @staticmethod
    def generate_column(column_index, width=100):
        """Generate rainbow column data"""
        column_data = []
        for i in range(NUM_LEDS):
            # Create rainbow effect
            hue = (column_index * 2 + i * 2) % 360
            r, g, b = RainbowGenerator.hsv_to_rgb(hue, 1.0, 1.0)
            column_data.append((int(r * 255), int(g * 255), int(b * 255)))
        return column_data, width
    
    @staticmethod
    def hsv_to_rgb(h, s, v):
        """Convert HSV to RGB"""
        h = h % 360
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
            
        return r + m, g + m, b + m

class LEDController:
    def __init__(self):
        self.clear()
    
    def clear(self):
        """Turn off all LEDs"""
        pixels.fill((0, 0, 0))
        pixels.show()
    
    def display_column(self, column_data):
        """Display column data on LED strip"""
        # Ensure onboard LEDs are always off during playback
        self.set_onboard_led_off()
        
        # Map image pixels to LEDs (distant end = top of image)
        # LED[0] = bottom of image, LED[143] = top of image
        for i, (r, g, b) in enumerate(column_data):
            if i < NUM_LEDS:
                led_index = NUM_LEDS - 1 - i  # Flip mapping
                pixels[led_index] = (r, g, b)
        pixels.show()
    
    def status_flash(self, color, duration=0.1):
        """Flash LED strip with status color"""
        self.set_onboard_led_off()  # Keep onboard LED off
        pixels.fill(color)
        pixels.show()
        time.sleep(duration)
        pixels.fill((0, 0, 0))
        pixels.show()
    
    def image_number_indicator(self, image_number, total_images):
        """Show which image is selected by blinking N pixels N times"""
        self.set_onboard_led_off()  # Keep onboard LED off
        
        # Limit to max 10 pixels for practical display
        num_pixels = min(image_number, 10)
        num_blinks = min(image_number, 5)  # Max 5 blinks to keep it reasonable
        
        # Color for image indicator (bright blue)
        color = (0, 100, 255)
        
        for blink in range(num_blinks):
            # Light up N pixels from the bottom (LED end)
            pixels.fill((0, 0, 0))  # Clear all
            for i in range(num_pixels):
                pixels[i] = color
            pixels.show()
            time.sleep(0.2)
            
            # Turn off
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(0.15)
        
        time.sleep(0.3)  # Pause before continuing
    
    def set_onboard_led_off(self):
        """Turn off all onboard LEDs"""
        for led_info in onboard_leds:
            if led_info[0] == 'rgb':  # RGB LED
                led_info[1].value = False  # R
                led_info[2].value = False  # G
                led_info[3].value = False  # B
            elif led_info[0] == 'single':  # Single LED
                led_info[1].value = False

class ButtonHandler:
    def __init__(self):
        self.last_a = True
        self.last_b = True
        self.button_b_press_time = None
    
    def check_buttons(self):
        """Check for button presses and return actions"""
        # Safely read button values, defaulting to True (not pressed) if button doesn't exist
        current_a = button_a.value if button_a else True
        current_b = button_b.value if button_b else True
        
        actions = []
        current_time = time.monotonic()
        
        # Button A: Next image (on release) - only if button exists
        if button_a and self.last_a and not current_a:
            actions.append('next_image')
        
        # Button B: Start/stop toggle + long press for mode toggle
        if button_b:
            # Button B pressed down (start timing)
            if self.last_b and not current_b:
                self.button_b_press_time = current_time
            
            # Button B released - check press duration
            elif not self.last_b and current_b:
                if self.button_b_press_time:
                    press_duration = current_time - self.button_b_press_time
                    
                    if press_duration >= LONG_PRESS_DURATION:
                        # Long press: Toggle playback mode
                        actions.append('toggle_mode')
                    else:
                        # Short press: Toggle start/stop
                        actions.append('toggle_playback')
                    
                    self.button_b_press_time = None
        
        self.last_a = current_a
        self.last_b = current_b
        
        return actions

# Main application
def main():
    print("LED Pixelstick starting...")
    
    # Initialize components
    image_manager = ImageManager()
    led_controller = LEDController()
    button_handler = ButtonHandler()
    
    # State variables
    playback_mode = DEFAULT_MODE
    is_playing = False
    current_column = 0
    image_width = 0
    current_format_info = None
    last_column_time = 0
    using_rainbow = len(image_manager.images) == 0
    
    # Turn off onboard LED
    led_controller.set_onboard_led_off()
    
    # Initial status
    if using_rainbow:
        led_controller.status_flash((255, 0, 255), 0.2)  # Purple for rainbow mode
        print("No images found - using rainbow pattern")
        image_width = 100  # Default rainbow width
    else:
        led_controller.status_flash((0, 255, 0) if playback_mode == "loop" else (255, 0, 0), 0.2)
        print(f"Loaded {len(image_manager.images)} images, mode: {playback_mode}")
    
    while True:
        # Handle button presses
        actions = button_handler.check_buttons()
        
        for action in actions:
            if action == 'next_image' and not using_rainbow:
                next_img = image_manager.next_image()
                if next_img:
                    is_playing = False
                    current_column = 0
                    image_width = 0
                    current_format_info = None  # Reset format info for new image
                    led_controller.clear()
                    # Show image number indicator: N pixels blink N times
                    image_num = image_manager.current_image_index + 1  # 1-based for user
                    led_controller.image_number_indicator(image_num, len(image_manager.images))
                    print(f"Switched to image {image_num}: {next_img}")
            
            elif action == 'toggle_playback':
                if is_playing:
                    # Stop playback
                    is_playing = False
                    led_controller.clear()
                    print("Playback stopped")
                else:
                    # Start playback (resume from current position or restart)
                    is_playing = True
                    last_column_time = time.monotonic() * 1000
                    if using_rainbow:
                        print("Starting rainbow pattern")
                    else:
                        print(f"Starting: {image_manager.get_current_image()}")
            
            elif action == 'toggle_mode':
                playback_mode = "once" if playback_mode == "loop" else "loop"
                color = (0, 255, 0) if playback_mode == "loop" else (255, 0, 0)
                led_controller.status_flash(color, 0.2)
                print(f"Mode: {playback_mode}")
        
        # Handle playback
        if is_playing:
            current_time = time.monotonic() * 1000
            if current_time - last_column_time >= PLAYBACK_SPEED_MS:
                if using_rainbow:
                    # Rainbow pattern
                    column_data, width = RainbowGenerator.generate_column(current_column)
                    image_width = width
                else:
                    # Load current image info if needed
                    if current_format_info is None:
                        current_image = image_manager.get_current_image()
                        if current_image:
                            current_format_info = BMPReader.read_bmp_header(f"{IMAGES_DIR}/{current_image}")
                            if current_format_info and current_format_info['height'] == NUM_LEDS:
                                image_width = current_format_info['width']
                                # Print format information
                                if current_format_info['is_indexed']:
                                    print(f"8-bit indexed BMP: {image_width}x{current_format_info['height']} (Memory efficient!)")
                                else:
                                    print(f"24-bit BMP: {image_width}x{current_format_info['height']}")
                            else:
                                if current_format_info:
                                    print(f"Invalid image dimensions: {current_format_info['width']}x{current_format_info['height']}")
                                else:
                                    print("Error reading BMP file")
                                is_playing = False
                                continue
                    
                    # Read column data
                    current_image = image_manager.get_current_image()
                    if current_image and current_column < image_width:
                        column_data = BMPReader.read_bmp_column(
                            f"{IMAGES_DIR}/{current_image}", 
                            current_column, 
                            current_format_info
                        )
                    else:
                        column_data = [(0, 0, 0)] * NUM_LEDS
                
                # Display column
                led_controller.display_column(column_data)
                
                # Advance to next column
                current_column += 1
                last_column_time = current_time
                
                # Check for end of image
                if current_column >= image_width:
                    if playback_mode == "loop":
                        current_column = 0  # Seamless loop
                    else:
                        # Play once - stop and clear, but allow restart
                        is_playing = False
                        current_column = 0
                        image_width = 0
                        current_format_info = None  # Reset format info to allow restart
                        led_controller.clear()
                        print("Image completed. Press B to restart.")
        
        # Keep onboard LED off during operation
        led_controller.set_onboard_led_off()
        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()