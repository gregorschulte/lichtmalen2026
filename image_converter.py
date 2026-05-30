#!/usr/bin/env python3
"""
LED Pixelstick Image Converter
Drag & Drop Image to BMP Converter for Plasma 2040

Converts any image format to 144px height BMP files suitable for the LED Pixelstick.
Maintains aspect ratio and outputs 24-bit BMP format.

Usage:
1. Run: python image_converter.py
2. Drag and drop images onto the window
3. Converted BMP files will be saved in the 'converted_images' directory
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os
import sys
import threading

class ImageConverter:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("LED Pixelstick Image Converter")
        self.root.geometry("600x500")
        self.root.configure(bg="#2b2b2b")
        
        # Output directory
        self.output_dir = "converted_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.setup_ui()
        self.setup_drag_drop()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="LED Pixelstick Image Converter",
            font=("Arial", 18, "bold"),
            bg="#2b2b2b",
            fg="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Drag & Drop images here or click 'Browse Files'\nConverts to 144px height BMP files",
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="#cccccc",
            justify=tk.CENTER
        )
        instructions.pack(pady=10)
        
        # Drop zone
        self.drop_frame = tk.Frame(
            self.root,
            bg="#404040",
            relief=tk.RAISED,
            borderwidth=2,
            width=500,
            height=200
        )
        self.drop_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.drop_frame.pack_propagate(False)
        
        drop_label = tk.Label(
            self.drop_frame,
            text="📁\n\nDrop images here\n\nSupported: JPG, PNG, GIF, BMP, TIFF",
            font=("Arial", 14),
            bg="#404040",
            fg="#ffffff",
            justify=tk.CENTER
        )
        drop_label.pack(expand=True, fill=tk.BOTH)
        
        # Browse button
        browse_btn = tk.Button(
            self.root,
            text="Browse Files",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            command=self.browse_files
        )
        browse_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='determinate',
            length=400
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text=f"Ready - Output directory: {self.output_dir}/",
            font=("Arial", 10),
            bg="#2b2b2b",
            fg="#cccccc"
        )
        self.status_label.pack(pady=5)
        
        # Output info
        info_text = tk.Label(
            self.root,
            text="Converted files will be saved as 'filename_144px.bmp'\nCopy these files to the /images folder on your Plasma 2040",
            font=("Arial", 9),
            bg="#2b2b2b",
            fg="#888888",
            justify=tk.CENTER
        )
        info_text.pack(pady=10)
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        
        # Also register the main window
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)
    
    def handle_drop(self, event):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        valid_files = [f for f in files if self.is_valid_image(f)]
        
        if valid_files:
            threading.Thread(target=self.convert_images, args=(valid_files,), daemon=True).start()
        else:
            messagebox.showwarning("No Valid Images", "No supported image files found in the dropped items.")
    
    def browse_files(self):
        """Browse for files using file dialog"""
        filetypes = [
            ("All Images", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff;*.tif"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("PNG files", "*.png"),
            ("GIF files", "*.gif"),
            ("BMP files", "*.bmp"),
            ("TIFF files", "*.tiff;*.tif"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Images to Convert",
            filetypes=filetypes
        )
        
        if files:
            threading.Thread(target=self.convert_images, args=(files,), daemon=True).start()
    
    def is_valid_image(self, filepath):
        """Check if file is a valid image"""
        try:
            valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif')
            return filepath.lower().endswith(valid_extensions)
        except:
            return False
    
    def convert_images(self, file_paths):
        """Convert images to 144px height BMP format"""
        total_files = len(file_paths)
        converted_count = 0
        
        # Reset progress bar
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        for i, file_path in enumerate(file_paths):
            try:
                # Update status
                filename = os.path.basename(file_path)
                self.status_label.config(text=f"Converting: {filename}")
                self.root.update_idletasks()
                
                # Open and convert image
                with Image.open(file_path) as img:
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
                    base_name = os.path.splitext(filename)[0]
                    output_filename = f"{base_name}_144px.bmp"
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    # Save as 24-bit BMP
                    resized_img.save(output_path, format='BMP')
                    
                    converted_count += 1
                    print(f"Converted: {filename} -> {output_filename} ({target_width}x{target_height})")
                
            except Exception as e:
                print(f"Error converting {filename}: {str(e)}")
                messagebox.showerror("Conversion Error", f"Failed to convert {filename}:\n{str(e)}")
            
            # Update progress
            self.progress['value'] = i + 1
            self.root.update_idletasks()
        
        # Final status update
        if converted_count > 0:
            self.status_label.config(
                text=f"Completed! Converted {converted_count}/{total_files} files. Check {self.output_dir}/ folder."
            )
            messagebox.showinfo(
                "Conversion Complete", 
                f"Successfully converted {converted_count} image(s)!\n\n"
                f"Files saved to: {self.output_dir}/\n\n"
                f"Copy the BMP files to the /images folder on your Plasma 2040."
            )
        else:
            self.status_label.config(text="No files were converted.")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import PIL
    except ImportError:
        missing_deps.append("Pillow")
    
    try:
        import tkinterdnd2
    except ImportError:
        missing_deps.append("tkinterdnd2")
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing_deps)}")
        sys.exit(1)

def main():
    """Main application entry point"""
    print("LED Pixelstick Image Converter")
    print("=" * 40)
    
    # Check dependencies
    check_dependencies()
    
    # Create and run the converter
    converter = ImageConverter()
    
    try:
        converter.run()
    except KeyboardInterrupt:
        print("\nConverter closed by user.")
    except Exception as e:
        messagebox.showerror("Application Error", f"An error occurred:\n{str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()