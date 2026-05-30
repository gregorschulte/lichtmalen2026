#!/usr/bin/env python3
"""
LED Pixelstick Test Pattern Generator
Creates calibration and test patterns for diagnosing color and mapping issues

Generates 144x144 pixel test images to help identify:
- Color channel swapping (RGB vs BGR)
- LED mapping issues
- Color accuracy problems
- Alignment issues
"""

import os
from PIL import Image, ImageDraw, ImageFont
import math

def create_test_patterns():
    """Generate all test patterns"""
    
    # Ensure output directory exists
    output_dir = "test_patterns"
    os.makedirs(output_dir, exist_ok=True)
    
    size = (144, 144)  # Square format matching LED count
    
    print("LED Pixelstick Test Pattern Generator")
    print("=" * 50)
    
    # 1. Primary Colors Test
    print("Creating primary color tests...")
    create_solid_color_test(size, output_dir)
    
    # 2. Corner Identification Pattern
    print("Creating corner identification pattern...")
    create_corner_test(size, output_dir)
    
    # 3. RGB Channel Tests
    print("Creating RGB channel tests...")
    create_rgb_channel_tests(size, output_dir)
    
    # 4. Alignment Tests
    print("Creating alignment test patterns...")
    create_alignment_tests(size, output_dir)
    
    # 5. Color Accuracy Tests
    print("Creating color accuracy tests...")
    create_color_accuracy_tests(size, output_dir)
    
    # 6. Crosshair and Grid Tests
    print("Creating crosshair and grid tests...")
    create_crosshair_tests(size, output_dir)
    
    print(f"\nTest patterns created in '{output_dir}/' directory!")
    print("Copy these BMP files to your Plasma 2040 and test each pattern.")

def create_solid_color_test(size, output_dir):
    """Create solid color test patterns"""
    colors = [
        ("01_red", (255, 0, 0)),
        ("02_green", (0, 255, 0)),
        ("03_blue", (0, 0, 255)),
        ("04_white", (255, 255, 255)),
        ("05_black", (0, 0, 0)),
        ("06_yellow", (255, 255, 0)),
        ("07_cyan", (0, 255, 255)),
        ("08_magenta", (255, 0, 255)),
    ]
    
    for name, color in colors:
        img = Image.new('RGB', size, color)
        filename = f"{output_dir}/{name}_solid.bmp"
        img.save(filename, format='BMP')
        print(f"  ✓ {filename}")

def create_corner_test(size, output_dir):
    """Create corner identification pattern with center crosshair"""
    img = Image.new('RGB', size, (128, 128, 128))  # Gray background
    draw = ImageDraw.Draw(img)
    
    width, height = size
    corner_size = 20
    
    # Corner markers
    # Top-left: Red
    draw.rectangle([0, 0, corner_size, corner_size], fill=(255, 0, 0))
    # Top-right: Green
    draw.rectangle([width-corner_size, 0, width, corner_size], fill=(0, 255, 0))
    # Bottom-left: Blue
    draw.rectangle([0, height-corner_size, corner_size, height], fill=(0, 0, 255))
    # Bottom-right: White
    draw.rectangle([width-corner_size, height-corner_size, width, height], fill=(255, 255, 255))
    
    # Center crosshair
    center_x, center_y = width // 2, height // 2
    crosshair_size = 15
    crosshair_thickness = 3
    
    # Horizontal line
    draw.rectangle([
        center_x - crosshair_size, center_y - crosshair_thickness//2,
        center_x + crosshair_size, center_y + crosshair_thickness//2
    ], fill=(255, 255, 0))  # Yellow
    
    # Vertical line
    draw.rectangle([
        center_x - crosshair_thickness//2, center_y - crosshair_size,
        center_x + crosshair_thickness//2, center_y + crosshair_size
    ], fill=(255, 255, 0))  # Yellow
    
    # Center circle
    circle_radius = 5
    draw.ellipse([
        center_x - circle_radius, center_y - circle_radius,
        center_x + circle_radius, center_y + circle_radius
    ], fill=(0, 0, 0), outline=(255, 255, 255))
    
    filename = f"{output_dir}/08_corner_identification.bmp"
    img.save(filename, format='BMP')
    print(f"  ✓ {filename}")

def create_rgb_channel_tests(size, output_dir):
    """Create individual RGB channel tests"""
    width, height = size
    
    # Red channel gradient
    img_r = Image.new('RGB', size)
    for x in range(width):
        intensity = int((x / (width - 1)) * 255)
        for y in range(height):
            img_r.putpixel((x, y), (intensity, 0, 0))
    img_r.save(f"{output_dir}/09_red_gradient.bmp", format='BMP')
    
    # Green channel gradient
    img_g = Image.new('RGB', size)
    for x in range(width):
        intensity = int((x / (width - 1)) * 255)
        for y in range(height):
            img_g.putpixel((x, y), (0, intensity, 0))
    img_g.save(f"{output_dir}/10_green_gradient.bmp", format='BMP')
    
    # Blue channel gradient
    img_b = Image.new('RGB', size)
    for x in range(width):
        intensity = int((x / (width - 1)) * 255)
        for y in range(height):
            img_b.putpixel((x, y), (0, 0, intensity))
    img_b.save(f"{output_dir}/11_blue_gradient.bmp", format='BMP')
    
    print(f"  ✓ RGB gradient tests created")

def create_alignment_tests(size, output_dir):
    """Create alignment and mapping test patterns"""
    width, height = size
    
    # Checkerboard pattern
    img_check = Image.new('RGB', size)
    checker_size = 8
    for x in range(width):
        for y in range(height):
            if ((x // checker_size) + (y // checker_size)) % 2 == 0:
                img_check.putpixel((x, y), (255, 255, 255))
            else:
                img_check.putpixel((x, y), (0, 0, 0))
    img_check.save(f"{output_dir}/12_checkerboard.bmp", format='BMP')
    
    # Grid pattern
    img_grid = Image.new('RGB', size, (0, 0, 0))
    draw = ImageDraw.Draw(img_grid)
    grid_spacing = 12
    
    for i in range(0, width, grid_spacing):
        draw.line([(i, 0), (i, height)], fill=(128, 128, 128))
    for i in range(0, height, grid_spacing):
        draw.line([(0, i), (width, i)], fill=(128, 128, 128))
    
    img_grid.save(f"{output_dir}/13_grid.bmp", format='BMP')
    
    # Single pixel lines
    img_lines = Image.new('RGB', size, (0, 0, 0))
    draw = ImageDraw.Draw(img_lines)
    
    # Vertical lines every 24 pixels
    for x in range(0, width, 24):
        draw.line([(x, 0), (x, height)], fill=(255, 0, 0))
    
    # Horizontal lines every 24 pixels  
    for y in range(0, height, 24):
        draw.line([(0, y), (width, y)], fill=(0, 255, 0))
    
    # Center lines
    draw.line([(width//2, 0), (width//2, height)], fill=(255, 255, 0))
    draw.line([(0, height//2), (width, height//2)], fill=(255, 255, 0))
    
    img_lines.save(f"{output_dir}/14_pixel_lines.bmp", format='BMP')
    
    print(f"  ✓ Alignment tests created")

def create_color_accuracy_tests(size, output_dir):
    """Create color accuracy test patterns"""
    width, height = size
    
    # Rainbow gradient
    img_rainbow = Image.new('RGB', size)
    for x in range(width):
        hue = (x / (width - 1)) * 360
        r, g, b = hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))
        for y in range(height):
            img_rainbow.putpixel((x, y), color)
    img_rainbow.save(f"{output_dir}/15_rainbow_gradient.bmp", format='BMP')
    
    # Grayscale gradient
    img_gray = Image.new('RGB', size)
    for x in range(width):
        intensity = int((x / (width - 1)) * 255)
        color = (intensity, intensity, intensity)
        for y in range(height):
            img_gray.putpixel((x, y), color)
    img_gray.save(f"{output_dir}/16_grayscale_gradient.bmp", format='BMP')
    
    # Color swatches
    img_swatches = Image.new('RGB', size, (128, 128, 128))
    draw = ImageDraw.Draw(img_swatches)
    
    swatches = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),    # RGB
        (255, 255, 0), (255, 0, 255), (0, 255, 255),  # CMY
        (255, 128, 0), (128, 255, 0), (0, 128, 255),  # Mixed
        (255, 255, 255), (128, 128, 128), (0, 0, 0)   # Grayscale
    ]
    
    swatch_size = 24
    cols = 6
    rows = 2
    
    for i, color in enumerate(swatches):
        row = i // cols
        col = i % cols
        x = col * swatch_size + 12
        y = row * swatch_size + 48
        draw.rectangle([x, y, x + swatch_size, y + swatch_size], fill=color)
    
    img_swatches.save(f"{output_dir}/17_color_swatches.bmp", format='BMP')
    
    print(f"  ✓ Color accuracy tests created")

def create_crosshair_tests(size, output_dir):
    """Create crosshair and targeting tests"""
    width, height = size
    
    # Large crosshair test
    img = Image.new('RGB', size, (64, 64, 64))
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = width // 2, height // 2
    
    # Main crosshairs
    draw.line([(center_x, 0), (center_x, height)], fill=(255, 0, 0), width=2)
    draw.line([(0, center_y), (width, center_y)], fill=(0, 255, 0), width=2)
    
    # Corner to corner diagonals
    draw.line([(0, 0), (width, height)], fill=(0, 0, 255), width=1)
    draw.line([(0, height), (width, 0)], fill=(255, 255, 0), width=1)
    
    # Concentric circles
    for radius in [10, 20, 30, 50]:
        draw.ellipse([
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius
        ], outline=(255, 255, 255))
    
    # Center dot
    draw.ellipse([
        center_x - 3, center_y - 3,
        center_x + 3, center_y + 3
    ], fill=(255, 255, 255))
    
    img.save(f"{output_dir}/18_crosshair_target.bmp", format='BMP')
    
    print(f"  ✓ Crosshair test created")

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

if __name__ == "__main__":
    try:
        create_test_patterns()
        print("\n" + "=" * 50)
        print("SUCCESS!")
        print("\nNext steps:")
        print("1. Copy BMP files from test_patterns/ to your Plasma 2040")
        print("2. Test each pattern to identify color issues:")
        print("   - Solid colors: Check if RGB channels work correctly")
        print("   - Corner test: Verify LED strip orientation")
        print("   - Gradients: Check color transitions")
        print("   - Grid/lines: Verify pixel mapping")
        print("\nLook for:")
        print("- Wrong colors (RGB vs BGR channel swapping)")
        print("- Missing color channels")
        print("- Incorrect LED mapping/orientation")
        print("- Color accuracy issues")
        
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Run: source venv/bin/activate && pip install Pillow")
    except Exception as e:
        print(f"Error creating test patterns: {e}")