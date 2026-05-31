#!/usr/bin/env python3
"""
Simple Command-Line LED Pixelstick Image Converter
Converts images to 144px height BMP files for the LED Pixelstick

Usage:
    python simple_image_converter.py input_image.jpg
    python simple_image_converter.py *.jpg  # Convert multiple files
    python simple_image_converter.py folder_name/  # Convert all images in folder
"""

import sys
import os
import glob
from PIL import Image

def convert_image(input_path, output_dir="converted_images", use_indexed_color=True):
    """Convert a single image to 144px height BMP format"""
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Open and convert image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Calculate new dimensions (height = 144, maintain aspect ratio)
            original_width, original_height = img.size
            target_height = 144
            target_width = int((original_width * target_height) / original_height)
            
            # Resize image
            resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Create output filename
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            
            if use_indexed_color:
                # Convert to 8-bit indexed color for memory efficiency
                # Quantize to 256 colors with high quality algorithm
                indexed_img = resized_img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
                
                output_filename = f"{base_name}_144px_8bit.bmp"
                output_path = os.path.join(output_dir, output_filename)
                
                # Save as 8-bit indexed BMP
                indexed_img.save(output_path, format='BMP')
                
                # Calculate size reduction
                original_size = target_width * target_height * 3  # 24-bit
                indexed_size = target_width * target_height + 256 * 4  # 8-bit + palette
                reduction = (1 - indexed_size / original_size) * 100
                
                print(f"✓ Converted: {os.path.basename(input_path)} -> {output_filename} ({target_width}x{target_height})")
                print(f"  Memory efficient: {reduction:.1f}% smaller than 24-bit")
                
            else:
                # Save as 24-bit BMP (original method)
                output_filename = f"{base_name}_144px.bmp"
                output_path = os.path.join(output_dir, output_filename)
                resized_img.save(output_path, format='BMP')
                
                print(f"✓ Converted: {os.path.basename(input_path)} -> {output_filename} ({target_width}x{target_height})")
            
            return True
            
    except Exception as e:
        print(f"✗ Error converting {input_path}: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("LED Pixelstick Image Converter")
        print("=" * 40)
        print("Usage:")
        print("  python simple_image_converter.py image.jpg")
        print("  python simple_image_converter.py *.jpg")
        print("  python simple_image_converter.py folder/")
        print("\nSupported formats: JPG, PNG, GIF, BMP, TIFF")
        return
    
    # Collect all files to process
    files_to_convert = []
    
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            # Directory - find all image files
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp', '*.tiff', '*.tif']:
                pattern = os.path.join(arg, ext)
                files_to_convert.extend(glob.glob(pattern))
                # Also check uppercase extensions
                files_to_convert.extend(glob.glob(pattern.upper()))
        elif '*' in arg or '?' in arg:
            # Glob pattern
            files_to_convert.extend(glob.glob(arg))
        elif os.path.isfile(arg):
            # Single file
            files_to_convert.append(arg)
        else:
            print(f"Warning: {arg} not found")
    
    # Remove duplicates and sort
    files_to_convert = sorted(list(set(files_to_convert)))
    
    if not files_to_convert:
        print("No image files found to convert!")
        return
    
    print(f"Found {len(files_to_convert)} image(s) to convert:")
    for f in files_to_convert:
        print(f"  - {f}")
    print()
    
    # Convert all files
    success_count = 0
    for file_path in files_to_convert:
        if convert_image(file_path):
            success_count += 1
    
    print()
    print(f"Conversion complete: {success_count}/{len(files_to_convert)} files converted")
    print(f"Output directory: converted_images/")
    print("\nCopy the BMP files to the /images folder on your Plasma 2040!")

if __name__ == "__main__":
    main()