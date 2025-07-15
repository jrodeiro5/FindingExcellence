"""
Icon Converter Script for FindingExcellence
Converts PNG images to ICO format for Windows applications
"""

try:
    from PIL import Image
    import os
    import sys
    
    def convert_png_to_ico(png_path, ico_path):
        """
        Convert PNG image to ICO format for Windows applications
        """
        try:
            # Open the PNG image
            img = Image.open(png_path)
            
            # Convert to RGBA if not already (for transparency support)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize to common icon sizes
            # Windows typically uses 16x16, 32x32, 48x48, 256x256
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Create ICO file with multiple sizes
            img.save(ico_path, format='ICO', sizes=sizes)
            
            print(f"✓ Successfully converted {png_path} to {ico_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error converting image: {e}")
            return False

    def main():
        # Paths relative to the build_resources directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        png_file = os.path.join(project_root, "resources", "FindingExcellence_new_logo.png")
        ico_file = os.path.join(os.path.dirname(__file__), "icons", "app_icon.ico")
        
        print("FindingExcellence Icon Converter")
        print("=" * 40)
        
        # Check if PNG file exists
        if not os.path.exists(png_file):
            print(f"✗ PNG file not found: {png_file}")
            input("Press Enter to exit...")
            return
        
        # Create icons directory if it doesn't exist
        icons_dir = os.path.dirname(ico_file)
        os.makedirs(icons_dir, exist_ok=True)
        
        print(f"Converting: {os.path.basename(png_file)}")
        print(f"To: {ico_file}")
        print()
        
        # Convert the image
        if convert_png_to_ico(png_file, ico_file):
            print()
            print("Conversion completed successfully!")
            print("You can now rebuild your executable to use the new icon.")
            print("Run 'install_executable.bat' to rebuild with the new icon.")
        else:
            print()
            print("Conversion failed. Please check the error message above.")
        
        print()
        input("Press Enter to exit...")

    if __name__ == "__main__":
        main()
        
except ImportError:
    print("PIL (Pillow) library is required for icon conversion.")
    print("Install it using: pip install Pillow")
    print()
    print("Alternative: Use an online converter like:")
    print("https://convertio.co/png-ico/ (Safe and reliable)")
    print("https://icoconvert.com/ (Free online converter)")
    print()
    input("Press Enter to exit...")
