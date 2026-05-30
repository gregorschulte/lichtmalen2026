# LED Pixelstick for Light Painting

A professional light painting stick using Pimoroni Plasma 2040 with 144 NeoPixel LEDs, designed to display BMP images column-by-column for stunning light painting photography.

## Features

- **144 LED NeoPixel Strip**: Full-height image display (1 meter strip)
- **Dynamic Image Loading**: Reads BMP files from internal storage
- **Flexible Image Widths**: Automatically detects image width
- **Two Playback Modes**: Loop (continuous) and Play Once
- **Professional Operation**: Onboard LED off during playback
- **Status Feedback**: LED flashes indicate mode changes
- **Rainbow Backup**: Built-in rainbow pattern if no images found
- **Easy Controls**: Three button operation

## Hardware Requirements

- **Pimoroni Plasma 2040** microcontroller
- **144/m NeoPixel LED Strip** (1 meter = 144 LEDs total)
- **Power Supply**: Adequate for 144 LEDs (5V, ~8-10A recommended)
- **MicroSD or Internal Storage**: For BMP image files

## Button Controls

| Button | Function |
|--------|----------|
| **A** | Switch to next image |
| **B** | Start/restart current image playback |
| **Boot** | Toggle between Loop mode and Play Once mode |

## Status LED Feedback

| Color | Meaning |
|-------|---------|
| 🟢 **Green Flash** | Loop mode active |
| 🔴 **Red Flash** | Play Once mode active |
| 🔵 **Blue Flash** | Image switched |
| 🟣 **Purple Flash** | Rainbow mode (no images found) |

## Installation

### 1. Setup CircuitPython

1. Download CircuitPython for Plasma 2040 from [circuitpython.org](https://circuitpython.org/board/pimoroni_plasma2040/)
2. Flash CircuitPython to your Plasma 2040
3. The device will appear as a USB drive named `CIRCUITPY`

### 2. Install Required Libraries

Download these libraries from the [CircuitPython Library Bundle](https://circuitpython.org/libraries) and copy to `CIRCUITPY/lib/`:

```
lib/
├── neopixel.mpy
└── adafruit_bus_device/   (if needed for additional sensors)
```

The main libraries you need:
- `neopixel.mpy` - Essential for LED control

### 3. Upload the Code

1. Copy `code.py` to the root of the `CIRCUITPY` drive
2. Create an `images` folder: `CIRCUITPY/images/`
3. The device will automatically restart and run the code

### 4. Prepare Images

Use the included `image_converter.py` to convert your images:

```bash
# Install dependencies (one-time setup)
pip install Pillow tkinterdnd2

# Run the converter
python image_converter.py
```

#### Image Converter Features:
- **Drag & Drop Interface**: Simply drag images onto the window
- **Automatic Resizing**: Converts any image to exactly 144px height
- **Maintains Aspect Ratio**: Width scales proportionally
- **Batch Processing**: Convert multiple images at once
- **Multiple Formats**: Supports JPG, PNG, GIF, BMP, TIFF

### 5. Copy Images to Device

1. Convert your images using `image_converter.py`
2. Copy the generated BMP files from `converted_images/` folder
3. Paste them into the `CIRCUITPY/images/` folder
4. Images will be loaded alphabetically

## Configuration

Edit these settings at the top of `code.py`:

```python
# Configuration
PLAYBACK_SPEED_MS = 50  # Column display duration (milliseconds)
NUM_LEDS = 144          # Number of LEDs (should match your strip)
DEFAULT_MODE = "loop"   # Default playback mode: "loop" or "once"
IMAGES_DIR = "/images"  # Image directory on the device
```

## Usage Guide

### First Time Setup

1. **Power On**: Connect the Pixelstick to power
2. **Status Check**: 
   - Green flash: Loop mode ready
   - Purple flash: No images found (rainbow mode)
3. **Load Images**: If purple flash, add BMP files to `/images/` folder

### Basic Operation

1. **Press B**: Start displaying the current image
2. **Press A**: Switch to next image (blue flash confirms)
3. **Press Boot**: Toggle between Loop and Play Once modes

### Light Painting Tips

- **Loop Mode**: Perfect for practicing and long exposures
- **Play Once Mode**: Ideal for single-shot captures
- **Image Width**: Wider images = longer light trails
- **Movement Speed**: Adjust your movement to match the 50ms column timing
- **LED Orientation**: Distant end of strip = top of image

## File Structure

```
CIRCUITPY/
├── code.py              # Main application
├── lib/                 # CircuitPython libraries
│   └── neopixel.mpy
└── images/              # Your BMP image files
    ├── image1_144px.bmp
    ├── image2_144px.bmp
    └── rainbow.bmp      # (optional)
```

## Troubleshooting

### Common Issues

**No images loading:**
- Check that images are in `/images/` folder
- Ensure files are 24-bit BMP format
- Verify images are exactly 144 pixels tall

**Images look wrong:**
- Check LED strip orientation (distant end = image top)
- Verify image conversion was successful
- Try reducing image complexity

**Buttons not responding:**
- Check physical connections
- Restart the device (unplug/replug power)
- Verify CircuitPython installation

**LED strip issues:**
- Check power supply capacity (144 LEDs need ~8A)
- Verify data line connection to `board.DATA`
- Test with rainbow mode first

### Serial Console

Connect via serial (115200 baud) to see debug output:
- Image loading status
- Button press events
- Error messages
- Current mode status

## Technical Details

### Image Format Requirements
- **Format**: 24-bit BMP
- **Height**: Exactly 144 pixels
- **Width**: Variable (detected automatically)
- **Color Space**: RGB

### Memory Management
- Images are streamed column by column
- No full image caching (memory efficient)
- Supports large width images

### Timing
- **Column Rate**: 50ms per column (20 columns/second)
- **Image Loop**: Seamless in loop mode
- **Button Response**: ~10ms polling rate

## Image Tools & Generators

The project includes multiple powerful tools for creating and converting images:

### **1. Simple Image Converter (`simple_image_converter.py`)**
Command-line tool that converts any image format to 144px height BMP files:
```bash
# Convert single image
python simple_image_converter.py photo.jpg

# Convert multiple images
python simple_image_converter.py *.jpg *.png

# Convert entire folder
python simple_image_converter.py images_folder/
```

### **2. Test Pattern Generator (`test_pattern_generator.py`)**
Creates 19 diagnostic patterns (144×144px) for troubleshooting color and alignment issues:

**Primary Color Tests (01-08):**
- Pure Red, Green, Blue, White, Black
- Yellow, Cyan, Magenta for color mixing tests

**Orientation & Mapping (08):**
- Corner identification with colored markers
- Center crosshair for precise alignment

**Channel Analysis (09-11):**
- Individual RGB channel gradients
- Helps identify BGR vs RGB channel swapping

**Alignment Tests (12-14):**
- Checkerboard pattern for basic alignment
- Grid pattern for precise pixel mapping
- Single pixel lines for fine alignment

**Color Accuracy (15-17):**
- Rainbow gradient for full spectrum test
- Grayscale gradient for brightness linearity
- Color swatches for standard verification

**Precision Test (18):**
- Crosshair target with concentric circles

### **3. Single Column Generator (`single_column_generator.py`)**
Creates 32 ultra-efficient patterns (1×144px) perfect for looped backgrounds:

**Solid Colors (01-16):**
- 16 solid colors including primaries, secondaries, and gray levels
- Perfect for infinite solid color backgrounds when looped

**Vertical Gradients (17-21):**
- Red, Green, Blue, and White gradients
- Smooth transitions from black to full color

**Rainbow Effects (22-24):**
- Vertical rainbow gradients
- Reverse and pastel variations

**Special Effects (25-27):**
- Fire effect (hot bottom to cool top)
- Ocean waves effect
- Sunset gradient

**Utility Patterns (28-32):**
- Stripe patterns for testing
- Single pixel alignment markers

## Sample Images & Test Patterns

### **Generated Test Patterns:**
Run the generators to create comprehensive image sets:
```bash
# Create test patterns for diagnostics
python test_pattern_generator.py

# Create ultra-efficient single column patterns  
python single_column_generator.py

# Generate original sample patterns
python generate_samples.py
```

**Original Sample Images:**
1. **gradient_rainbow_144px.bmp** - Smooth color gradient
2. **stripes_vertical_144px.bmp** - High contrast stripes
3. **wave_pattern_144px.bmp** - Sine wave pattern
4. **circles_144px.bmp** - Expanding circle patterns
5. **fire_effect_144px.bmp** - Fire simulation
6. **sparkles_144px.bmp** - Starfield effect
7. **text_scroll_144px.bmp** - Scrolling text demo

### **Storage Efficiency:**
- **Test Patterns**: 19 patterns (~1.2MB total) for comprehensive diagnostics
- **Single Columns**: 32 patterns (~132KB total) for maximum storage efficiency
- **Sample Images**: 7 patterns (~732KB total) for immediate testing

## Development

### Modifying the Code

Key areas for customization:

1. **Playback Speed**: Change `PLAYBACK_SPEED_MS`
2. **LED Brightness**: Adjust `brightness=0.5` in NeoPixel setup
3. **Button Behavior**: Modify `ButtonHandler` class
4. **Visual Effects**: Enhance `RainbowGenerator` or `LEDController`

### Adding New Features

The modular code structure makes it easy to add:
- New image effects
- Additional button functions
- Different playback patterns
- External sensor inputs

## Contributing

Feel free to contribute improvements:
- Enhanced image effects
- Performance optimizations
- Additional file format support
- Better error handling

## License

This project is open source. Use and modify as needed for your light painting adventures!

---

**Happy Light Painting! 📸✨**