#!/usr/bin/env python3
"""
LED Pixelstick Single Column Pattern Generator
Creates 1x144 pixel images for efficient storage and looped painting

These ultra-narrow images are perfect for:
- Solid color backgrounds (when looped)
- Vertical gradients and effects
- Minimal storage usage
- Quick solid color fills during light painting
"""

import os
from PIL import Image, ImageDraw
import math

def create_single_column_patterns():
    """Generate all single column patterns"""
    
    # Ensure output directory exists
    output_dir = "single_columns"
    os.makedirs(output_dir, exist_ok=True)
    
    size = (1, 144)  # 1 pixel wide, 144 pixels high
    
    print("LED Pixelstick Single Column Generator")
    print("=" * 50)
    
    # 1. Basic Solid Colors
    print("Creating solid color columns...")
    create_solid_colors(size, output_dir)
    
    # 2. Vertical Gradients
    print("Creating vertical gradients...")
    create_vertical_gradients(size, output_dir)
    
    # 3. Rainbow Patterns
    print("Creating rainbow patterns...")
    create_rainbow_patterns(size, output_dir)
    
    # 4. Special Patterns
    print("Creating special patterns...")
    create_special_patterns(size, output_dir)
    
    # 5. Utility Patterns
    print("Creating utility patterns...")
    create_utility_patterns(size, output_dir)
    
    print(f"\nSingle column patterns created in '{output_dir}/' directory!")
    print("These 1-pixel wide images loop perfectly for solid backgrounds!")

def create_solid_colors(size, output_dir):
    """Create solid color single columns"""
    colors = [
        ("01_red", (255, 0, 0)),
        ("02_green", (0, 255, 0)),
        ("03_blue", (0, 0, 255)),
        ("04_white", (255, 255, 255)),
        ("05_black", (0, 0, 0)),
        ("06_yellow", (255, 255, 0)),
        ("07_cyan", (0, 255, 255)),
        ("08_magenta", (255, 0, 255)),
        ("09_orange", (255, 128, 0)),
        ("10_purple", (128, 0, 255)),
        ("11_pink", (255, 128, 192)),
        ("12_lime", (128, 255, 0)),
        ("13_teal", (0, 128, 128)),
        ("14_gray25", (64, 64, 64)),
        ("15_gray50", (128, 128, 128)),
        ("16_gray75", (192, 192, 192)),
    ]
    
    for name, color in colors:
        img = Image.new('RGB', size, color)
        filename = f"{output_dir}/{name}_solid.bmp"
        img.save(filename, format='BMP')
        print(f"  ✓ {filename}")

def create_vertical_gradients(size, output_dir):
    """Create vertical gradient single columns"""
    width, height = size
    
    # Red gradient (black to red)
    img = Image.new('RGB', size)
    for y in range(height):
        intensity = int((y / (height - 1)) * 255)
        img.putpixel((0, y), (intensity, 0, 0))
    img.save(f"{output_dir}/17_red_gradient.bmp", format='BMP')
    
    # Green gradient (black to green)
    img = Image.new('RGB', size)
    for y in range(height):
        intensity = int((y / (height - 1)) * 255)
        img.putpixel((0, y), (0, intensity, 0))
    img.save(f"{output_dir}/18_green_gradient.bmp", format='BMP')
    
    # Blue gradient (black to blue)
    img = Image.new('RGB', size)
    for y in range(height):
        intensity = int((y / (height - 1)) * 255)
        img.putpixel((0, y), (0, 0, intensity))
    img.save(f"{output_dir}/19_blue_gradient.bmp", format='BMP')
    
    # White gradient (black to white)
    img = Image.new('RGB', size)
    for y in range(height):
        intensity = int((y / (height - 1)) * 255)
        img.putpixel((0, y), (intensity, intensity, intensity))
    img.save(f"{output_dir}/20_white_gradient.bmp", format='BMP')
    
    # Reverse white gradient (white to black)
    img = Image.new('RGB', size)
    for y in range(height):
        intensity = int(255 - (y / (height - 1)) * 255)
        img.putpixel((0, y), (intensity, intensity, intensity))
    img.save(f"{output_dir}/21_white_reverse_gradient.bmp", format='BMP')
    
    print(f"  ✓ Vertical gradients created")

def create_rainbow_patterns(size, output_dir):
    """Create rainbow pattern single columns"""
    width, height = size
    
    # Vertical rainbow (top to bottom)
    img = Image.new('RGB', size)
    for y in range(height):
        hue = (y / (height - 1)) * 360
        r, g, b = hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))
        img.putpixel((0, y), color)
    img.save(f"{output_dir}/22_rainbow_vertical.bmp", format='BMP')
    
    # Reverse rainbow (bottom to top)
    img = Image.new('RGB', size)
    for y in range(height):
        hue = (1 - y / (height - 1)) * 360
        r, g, b = hsv_to_rgb(hue, 1.0, 1.0)
        color = (int(r * 255), int(g * 255), int(b * 255))
        img.putpixel((0, y), color)
    img.save(f"{output_dir}/23_rainbow_reverse.bmp", format='BMP')
    
    # Pastel rainbow
    img = Image.new('RGB', size)
    for y in range(height):
        hue = (y / (height - 1)) * 360
        r, g, b = hsv_to_rgb(hue, 0.6, 1.0)  # Lower saturation for pastel
        color = (int(r * 255), int(g * 255), int(b * 255))
        img.putpixel((0, y), color)
    img.save(f"{output_dir}/24_rainbow_pastel.bmp", format='BMP')
    
    print(f"  ✓ Rainbow patterns created")

def create_special_patterns(size, output_dir):
    """Create special effect single columns"""
    width, height = size
    
    # Fire effect (bottom hot, top cool)
    img = Image.new('RGB', size)
    for y in range(height):
        heat = (height - y) / height  # Bottom is hottest
        
        if heat > 0.8:
            # White hot
            r, g, b = 255, 255, int(255 * heat)
        elif heat > 0.5:
            # Yellow to orange
            r = 255
            g = int(255 * (heat - 0.5) / 0.3)
            b = 0
        elif heat > 0.2:
            # Red to yellow
            r = 255
            g = int(255 * (heat - 0.2) / 0.3)
            b = 0
        else:
            # Dark red to black
            r = int(255 * heat / 0.2)
            g, b = 0, 0
        
        img.putpixel((0, y), (min(255, r), min(255, g), min(255, b)))
    img.save(f"{output_dir}/25_fire_effect.bmp", format='BMP')
    
    # Ocean effect (blue gradient with waves)
    img = Image.new('RGB', size)
    for y in range(height):
        base_blue = int(64 + (y / height) * 128)  # Blue gradient
        wave = math.sin(y * 0.2) * 32  # Wave effect
        blue = max(0, min(255, int(base_blue + wave)))
        green = max(0, min(192, int(blue * 0.7)))
        img.putpixel((0, y), (0, green, blue))
    img.save(f"{output_dir}/26_ocean_effect.bmp", format='BMP')
    
    # Sunset effect
    img = Image.new('RGB', size)
    for y in range(height):
        progress = y / (height - 1)
        
        if progress < 0.3:
            # Deep blue (night sky)
            r, g, b = int(20 * progress / 0.3), int(40 * progress / 0.3), int(100 * progress / 0.3)
        elif progress < 0.7:
            # Orange/red (sunset)
            sunset_progress = (progress - 0.3) / 0.4
            r = int(100 + 155 * sunset_progress)
            g = int(40 + 140 * sunset_progress * (1 - sunset_progress * 0.5))
            b = int(100 * (1 - sunset_progress))
        else:
            # Yellow/white (sun)
            sun_progress = (progress - 0.7) / 0.3
            r = 255
            g = int(180 + 75 * sun_progress)
            b = int(100 * sun_progress)
        
        img.putpixel((0, y), (min(255, r), min(255, g), min(255, b)))
    img.save(f"{output_dir}/27_sunset_effect.bmp", format='BMP')
    
    print(f"  ✓ Special effects created")

def create_utility_patterns(size, output_dir):
    """Create utility and test patterns"""
    width, height = size
    
    # Alternating black/white stripes (every 8 pixels)
    img = Image.new('RGB', size)
    stripe_height = 8
    for y in range(height):
        if (y // stripe_height) % 2 == 0:
            img.putpixel((0, y), (255, 255, 255))
        else:
            img.putpixel((0, y), (0, 0, 0))
    img.save(f"{output_dir}/28_stripes_8px.bmp", format='BMP')
    
    # Alternating RGB stripes (every 12 pixels)
    img = Image.new('RGB', size)
    stripe_height = 12
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    for y in range(height):
        color_index = (y // stripe_height) % len(colors)
        img.putpixel((0, y), colors[color_index])
    img.save(f"{output_dir}/29_rgb_stripes.bmp", format='BMP')
    
    # Single white pixel at top (for alignment)
    img = Image.new('RGB', size, (0, 0, 0))
    img.putpixel((0, 0), (255, 255, 255))
    img.save(f"{output_dir}/30_top_pixel.bmp", format='BMP')
    
    # Single white pixel at bottom (for alignment)
    img = Image.new('RGB', size, (0, 0, 0))
    img.putpixel((0, height - 1), (255, 255, 255))
    img.save(f"{output_dir}/31_bottom_pixel.bmp", format='BMP')
    
    # Center white pixel (for alignment)
    img = Image.new('RGB', size, (0, 0, 0))
    img.putpixel((0, height // 2), (255, 255, 255))
    img.save(f"{output_dir}/32_center_pixel.bmp", format='BMP')
    
    print(f"  ✓ Utility patterns created")

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
        create_single_column_patterns()
        print("\n" + "=" * 50)
        print("SUCCESS!")
        print("\nCreated ultra-efficient 1x144 pixel images!")
        print("\nBenefits:")
        print("- Minimal storage usage (32 patterns in ~2KB total)")
        print("- Perfect for looped solid color backgrounds")
        print("- Instant color changes during light painting")
        print("- Vertical gradients and effects")
        print("\nUsage:")
        print("- Copy to your Plasma 2040 /images folder")
        print("- Enable loop mode for solid backgrounds")
        print("- Switch between patterns for instant color changes")
        print("- Great for painting large solid areas efficiently")
        
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Run: source venv/bin/activate && pip install Pillow")
    except Exception as e:
        print(f"Error creating patterns: {e}")