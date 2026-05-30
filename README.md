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

## Sample Images

The project includes several sample images in different styles:

1. **gradient_rainbow_144px.bmp** - Smooth color gradient
2. **stripes_vertical_144px.bmp** - High contrast stripes
3. **wave_pattern_144px.bmp** - Sine wave pattern

These demonstrate different visual effects and can serve as test images.

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