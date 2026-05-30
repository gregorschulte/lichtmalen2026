#!/usr/bin/env python3
"""
Generate Sample BMP Images for LED Pixelstick
Creates various test patterns and sample images with 144px height
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_sample_images():
    """Generate various sample BMP images for testing"""
    
    # Ensure sample_images directory exists
    output_dir = "sample_images"
    os.makedirs(output_dir, exist_ok=True)
    
    print("Generating sample BMP images...")
    
    # Image dimensions
    height = 144
    
    # 1. Rainbow Gradient
    print("Creating rainbow gradient...")
    width = 200
    rainbow_img = Image.new('RGB', (width, height))
    pixels = rainbow_img.load()
    
    for x in range(width):
        for y in range(height):
            # Create rainbow based on x position
            hue = (x / width) * 360
            # Convert HSV to RGB
            r, g, b = hsv_to_rgb(hue, 1.0, 1.0)
            pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))
    
    rainbow_img.save(os.path.join(output_dir, "gradient_rainbow_144px.bmp"), format='BMP')
    
    # 2. Vertical Stripes
    print("Creating vertical stripes...")
    width = 150
    stripes_img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(stripes_img)
    
    stripe_width = 10
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    
    for x in range(0, width, stripe_width):
        color_index = (x // stripe_width) % len(colors)
        draw.rectangle([x, 0, x + stripe_width, height], fill=colors[color_index])
    
    stripes_img.save(os.path.join(output_dir, "stripes_vertical_144px.bmp"), format='BMP')
    
    # 3. Wave Pattern
    print("Creating wave pattern...")
    width = 300
    wave_img = Image.new('RGB', (width, height))
    pixels = wave_img.load()
    
    for x in range(width):
        for y in range(height):
            # Create sine wave pattern
            wave_y = height // 2 + int(30 * math.sin(x * 0.05))
            distance = abs(y - wave_y)
            
            if distance < 20:
                intensity = 1.0 - (distance / 20.0)
                # Color based on position
                hue = (x * 2) % 360
                r, g, b = hsv_to_rgb(hue, 1.0, intensity)
                pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))
            else:
                pixels[x, y] = (0, 0, 0)
    
    wave_img.save(os.path.join(output_dir, "wave_pattern_144px.bmp"), format='BMP')
    
    # 4. Circular Patterns
    print("Creating circular patterns...")
    width = 250
    circle_img = Image.new('RGB', (width, height))
    pixels = circle_img.load()
    
    center_y = height // 2
    
    for x in range(width):
        for y in range(height):
            # Create expanding circles
            center_x = x
            distance = math.sqrt((y - center_y) ** 2)
            
            # Create ripple effect
            ripple = math.sin(distance * 0.3 + x * 0.1) * 0.5 + 0.5
            
            if ripple > 0.3:
                hue = (x * 1.5) % 360
                r, g, b = hsv_to_rgb(hue, 1.0, ripple)
                pixels[x, y] = (int(r * 255), int(g * 255), int(b * 255))
            else:
                pixels[x, y] = (0, 0, 0)
    
    circle_img.save(os.path.join(output_dir, "circles_144px.bmp"), format='BMP')
    
    # 5. Text Scroll
    print("Creating text scroll...")
    width = 400
    text_img = Image.new('RGB', (width, height), color=(0, 0, 50))
    draw = ImageDraw.Draw(text_img)
    
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Create scrolling text effect
    text = "LED PIXELSTICK"
    text_color = (0, 255, 255)
    
    for i, char in enumerate(text):
        x_pos = i * 25 + 20
        y_pos = height // 2 - 20
        
        if x_pos < width:
            draw.text((x_pos, y_pos), char, fill=text_color, font=font)
            draw.text((x_pos, y_pos + 40), char, fill=(255, 255, 0), font=font)
    
    text_img.save(os.path.join(output_dir, "text_scroll_144px.bmp"), format='BMP')
    
    # 6. Sparkle Effect
    print("Creating sparkle effect...")
    width = 180
    sparkle_img = Image.new('RGB', (width, height))
    pixels = sparkle_img.load()
    
    import random
    random.seed(42)  # For consistent results
    
    # Background gradient
    for x in range(width):
        for y in range(height):
            # Dark blue to black gradient
            intensity = (height - y) / height * 0.3
            pixels[x, y] = (0, 0, int(intensity * 255))
    
    # Add sparkles
    for _ in range(200):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        
        # Random sparkle color
        colors = [(255, 255, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
        color = random.choice(colors)
        
        # Small sparkle pattern
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    if abs(dx) + abs(dy) <= 1:  # Plus pattern
                        pixels[x + dx, y + dy] = color
    
    sparkle_img.save(os.path.join(output_dir, "sparkles_144px.bmp"), format='BMP')
    
    # 7. Fire Effect
    print("Creating fire effect...")
    width = 200
    fire_img = Image.new('RGB', (width, height))
    pixels = fire_img.load()
    
    for x in range(width):
        for y in range(height):
            # Fire effect from bottom to top
            heat = (height - y) / height
            noise = math.sin(x * 0.1 + y * 0.05) * 0.1
            heat += noise
            heat = max(0, min(1, heat))
            
            if heat > 0.7:
                # White hot
                r, g, b = 255, 255, int(255 * heat)
            elif heat > 0.4:
                # Yellow to orange
                r = 255
                g = int(255 * (heat - 0.4) / 0.3)
                b = 0
            elif heat > 0.1:
                # Red to yellow
                r = 255
                g = int(255 * (heat - 0.1) / 0.3)
                b = 0
            else:
                # Dark red to black
                r = int(255 * heat / 0.1)
                g, b = 0, 0
            
            pixels[x, y] = (r, g, b)
    
    fire_img.save(os.path.join(output_dir, "fire_effect_144px.bmp"), format='BMP')
    
    print(f"Sample images created in '{output_dir}/' directory:")
    print("  - gradient_rainbow_144px.bmp")
    print("  - stripes_vertical_144px.bmp") 
    print("  - wave_pattern_144px.bmp")
    print("  - circles_144px.bmp")
    print("  - text_scroll_144px.bmp")
    print("  - sparkles_144px.bmp")
    print("  - fire_effect_144px.bmp")
    print("\nCopy these files to the /images folder on your Plasma 2040!")

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
        create_sample_images()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"Error creating sample images: {e}")