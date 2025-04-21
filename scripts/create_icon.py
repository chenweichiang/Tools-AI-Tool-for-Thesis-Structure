from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

def create_icon():
    # Create a 256x256 image with a blue background
    size = 256
    image = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue square with dark blue outline
    margin = 20
    square_size = size - 2 * margin
    draw.rectangle([(margin, margin), (size - margin, size - margin)], 
                  fill='#007AFF', outline='#005AC1', width=3)
    
    # Add text "LR" in white
    try:
        # Try to load Arial font
        font = ImageFont.truetype("Arial", 120)
    except:
        try:
            # Try to load system font on macOS
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    text = "LR"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    draw.text((x, y), text, fill='white', font=font)
    
    # Save as PNG
    image.save('app_icon.png')
    
    # Save as ICO
    image.save('app_icon.ico', format='ICO', sizes=[(256, 256)])
    
    # For macOS: Create ICNS file
    if os.path.exists('app_icon.png'):
        # Create iconset directory
        if not os.path.exists('app_icon.iconset'):
            os.makedirs('app_icon.iconset')
        
        # Generate different sizes
        icon_sizes = [16, 32, 64, 128, 256, 512]
        for size in icon_sizes:
            img = image.resize((size, size), Image.Resampling.LANCZOS)
            img.save(f'app_icon.iconset/icon_{size}x{size}.png')
            if size <= 256:  # Generate 2x version for sizes up to 256
                img = image.resize((size*2, size*2), Image.Resampling.LANCZOS)
                img.save(f'app_icon.iconset/icon_{size}x{size}@2x.png')
        
        # Convert iconset to icns using iconutil (macOS only)
        try:
            subprocess.run(['iconutil', '-c', 'icns', 'app_icon.iconset'], check=True)
            # Clean up iconset directory
            import shutil
            shutil.rmtree('app_icon.iconset')
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"Warning: Could not create .icns file: {e}")
            print("Make sure you're on macOS and have iconutil installed.")

if __name__ == '__main__':
    create_icon() 