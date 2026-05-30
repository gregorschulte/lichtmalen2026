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
PLAYBACK_SPEED_MS = 50  # Column display duration in milliseconds
NUM_LEDS = 144
DEFAULT_MODE = "loop"  # "loop" or "once"
IMAGES_DIR = "/images"

# Hardware setup
pixels = neopixel.NeoPixel(board.DATA, NUM_LEDS, brightness=0.5, auto_write=False)

# Onboard LED setup with CircuitPython 10 compatibility
try:
    # Try the old pin name first (CircuitPython < 10)
    onboard_led = digitalio.DigitalInOut(board.LED)
except AttributeError:
    # CircuitPython 10+ uses different pin names, try alternatives
    try:
        onboard_led = digitalio.DigitalInOut(board.GP25)  # Common LED pin
    except AttributeError:
        try:
            onboard_led = digitalio.DigitalInOut(board.GP2)   # Alternative LED pin
        except AttributeError:
            # If no onboard LED available, create a dummy object
            print("Warning: No onboard LED found, using dummy LED object")
            onboard_led = None

if onboard_led:
    onboard_led.direction = digitalio.Direction.OUTPUT

# Button setup
button_a = digitalio.DigitalInOut(board.SW_A)
button_a.direction = digitalio.Direction.INPUT
button_a.pull = digitalio.Pull.UP

button_b = digitalio.DigitalInOut(board.SW_B)
button_b.direction = digitalio.Direction.INPUT
button_b.pull = digitalio.Pull.UP

button_boot = digitalio.DigitalInOut(board.USER)
button_boot.direction = digitalio.Direction.INPUT
button_boot.pull = digitalio.Pull.UP

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
        """Read BMP header to get image dimensions"""
        try:
            with open(filename, 'rb') as f:
                # Read BMP header
                header = f.read(54)  # Standard BMP header size
                
                # Extract width and height (little-endian)
                width = struct.unpack('<I', header[18:22])[0]
                height = struct.unpack('<I', header[22:26])[0]
                
                return width, height
        except:
            return None, None
    
    @staticmethod
    def read_bmp_column(filename, column, width, height):
        """Read a specific column from BMP file"""
        try:
            with open(filename, 'rb') as f:
                # Skip BMP header
                f.seek(54)
                
                # BMP files are stored bottom-to-top, we need top-to-bottom
                # Each pixel is 3 bytes (BGR format)
                row_size = ((width * 3 + 3) // 4) * 4  # Row size padded to 4 bytes
                
                column_data = []
                for row in range(height):
                    # Calculate position for this pixel (bottom-up in BMP)
                    pixel_row = height - 1 - row  # Flip to top-down
                    pos = 54 + pixel_row * row_size + column * 3
                    f.seek(pos)
                    
                    # Read BGR values
                    bgr = f.read(3)
                    if len(bgr) == 3:
                        # Convert BGR to RGB and add to column
                        r, g, b = bgr[2], bgr[1], bgr[0]
                        column_data.append((r, g, b))
                    else:
                        column_data.append((0, 0, 0))
                
                return column_data
        except:
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
        # Map image pixels to LEDs (distant end = top of image)
        # LED[0] = bottom of image, LED[143] = top of image
        for i, (r, g, b) in enumerate(column_data):
            if i < NUM_LEDS:
                led_index = NUM_LEDS - 1 - i  # Flip mapping
                pixels[led_index] = (r, g, b)
        pixels.show()
    
    def status_flash(self, color, duration=0.1):
        """Flash LED strip with status color"""
        if onboard_led:  # Only set if onboard LED exists
            onboard_led.value = False  # Keep onboard LED off
        pixels.fill(color)
        pixels.show()
        time.sleep(duration)
        pixels.fill((0, 0, 0))
        pixels.show()

class ButtonHandler:
    def __init__(self):
        self.last_a = True
        self.last_b = True
        self.last_boot = True
    
    def check_buttons(self):
        """Check for button presses and return actions"""
        current_a = button_a.value
        current_b = button_b.value
        current_boot = button_boot.value
        
        actions = []
        
        # Button A: Next image (on release)
        if self.last_a and not current_a:
            actions.append('next_image')
        
        # Button B: Start/restart image (on release)
        if self.last_b and not current_b:
            actions.append('start_image')
        
        # Boot button: Toggle mode (on release)
        if self.last_boot and not current_boot:
            actions.append('toggle_mode')
        
        self.last_a = current_a
        self.last_b = current_b
        self.last_boot = current_boot
        
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
    last_column_time = 0
    using_rainbow = len(image_manager.images) == 0
    
    # Turn off onboard LED
    if onboard_led:
        onboard_led.value = False
    
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
                    led_controller.clear()
                    led_controller.status_flash((0, 0, 255), 0.1)  # Blue for image switch
                    print(f"Switched to: {next_img}")
            
            elif action == 'start_image':
                is_playing = True
                current_column = 0
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
                    if image_width == 0:
                        current_image = image_manager.get_current_image()
                        if current_image:
                            width, height = BMPReader.read_bmp_header(f"{IMAGES_DIR}/{current_image}")
                            if width and height == NUM_LEDS:
                                image_width = width
                            else:
                                print(f"Invalid image dimensions: {width}x{height}")
                                is_playing = False
                                continue
                    
                    # Read column data
                    current_image = image_manager.get_current_image()
                    if current_image and current_column < image_width:
                        column_data = BMPReader.read_bmp_column(
                            f"{IMAGES_DIR}/{current_image}", 
                            current_column, 
                            image_width, 
                            NUM_LEDS
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
                        # Play once - stop and clear
                        is_playing = False
                        current_column = 0
                        image_width = 0
                        led_controller.clear()
        
        # Keep onboard LED off during operation
        if onboard_led:
            onboard_led.value = False
        time.sleep(0.01)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()