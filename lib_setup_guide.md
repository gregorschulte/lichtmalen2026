# CircuitPython Library Setup Guide

This guide helps you set up the required CircuitPython libraries for your LED Pixelstick project.

## Required Libraries

Your Plasma 2040 needs these libraries to run the Pixelstick code:

### Essential Libraries
- **`neopixel.mpy`** - Controls the LED strip
- **`adafruit_bus_device/`** - Low-level communication (often required by other libraries)

## Installation Steps

### 1. Download CircuitPython Libraries

1. Go to [CircuitPython Libraries](https://circuitpython.org/libraries)
2. Download the **Bundle for Version 8.x** (or whatever version matches your CircuitPython installation)
3. Extract the ZIP file on your computer

### 2. Locate Required Files

In the extracted bundle, find these files/folders:
```
circuitpython-community-bundle-8.x-mpy-xxxxxxxx/
├── lib/
│   ├── neopixel.mpy                    ← Copy this file
│   └── adafruit_bus_device/            ← Copy this folder (if present)
```

### 3. Copy to Plasma 2040

1. Connect your Plasma 2040 to your computer (it should appear as `CIRCUITPY` drive)
2. Create a `lib` folder in the root of `CIRCUITPY` if it doesn't exist
3. Copy the required files:

```
CIRCUITPY/
├── code.py                 # Your main code
├── images/                 # Your BMP images folder
└── lib/                    # Libraries folder
    ├── neopixel.mpy       # Essential for LED control
    └── adafruit_bus_device/    # (if present/needed)
```

## File Structure Verification

After copying, your Plasma 2040 should have this structure:

```
CIRCUITPY/
├── code.py
├── lib/
│   └── neopixel.mpy
├── images/
│   ├── gradient_rainbow_144px.bmp
│   ├── stripes_vertical_144px.bmp
│   └── ...other BMP files
└── (other CircuitPython files)
```

## Alternative Installation Methods

### Method 1: Manual Copy (Recommended)
- Most reliable method
- Download bundle and copy specific files
- Full control over what gets installed

### Method 2: Using `circup` (Advanced)
If you have `circup` installed, you can use it to manage libraries:

```bash
# Install circup (one-time setup)
pip install circup

# Install required library
circup install neopixel
```

Note: Make sure your Plasma 2040 is connected and recognized as `CIRCUITPY`.

## Troubleshooting

### "ImportError: No module named 'neopixel'"
- **Cause**: `neopixel.mpy` is missing from `/lib` folder
- **Solution**: Copy `neopixel.mpy` to `CIRCUITPY/lib/neopixel.mpy`

### "No such device CIRCUITPY"
- **Cause**: CircuitPython not properly installed on Plasma 2040
- **Solution**: Re-flash CircuitPython firmware
  1. Download CircuitPython UF2 file for Plasma 2040
  2. Put Plasma 2040 in bootloader mode (hold BOOT, press RESET)
  3. Copy UF2 file to the `RPI-RP2` drive that appears
  4. Device will restart as `CIRCUITPY`

### "Memory Error" or "Out of Space"
- **Cause**: Too many libraries or large files
- **Solution**: 
  1. Remove unnecessary files from `CIRCUITPY`
  2. Use `.mpy` compiled libraries instead of `.py` source files
  3. Keep only essential libraries

### Libraries Not Loading
- **Cause**: Incorrect file permissions or corrupted files
- **Solution**: 
  1. Delete and re-copy library files
  2. Ensure files are not corrupted during transfer
  3. Check that `lib` directory is in root of `CIRCUITPY`

## Version Compatibility

| CircuitPython Version | Library Bundle Version |
|-----------------------|------------------------|
| 8.x.x | Bundle 8.x.x |
| 7.x.x | Bundle 7.x.x |
| 6.x.x | Bundle 6.x.x |

Always match your library bundle version to your CircuitPython version for best compatibility.

## Minimal Installation

If you're short on storage space, you only need:
- `neopixel.mpy` (essential for LED control)

The code will work with just this single library file.

## Verification

After installation, connect to the serial console (115200 baud) and look for:
- No import errors during startup
- "LED Pixelstick starting..." message
- Status messages about image loading

If you see these messages, your libraries are correctly installed!

## Getting Help

If you encounter issues:
1. Check the serial console for error messages
2. Verify CircuitPython version: `import sys; print(sys.version)`
3. List installed libraries: `import os; print(os.listdir('/lib'))`
4. Try the minimal installation first (just `neopixel.mpy`)

## Library Sources

- **Official Adafruit Libraries**: https://github.com/adafruit/Adafruit_CircuitPython_Bundle
- **Community Libraries**: https://github.com/adafruit/CircuitPython_Community_Bundle
- **Documentation**: https://docs.circuitpython.org/