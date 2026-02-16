import os
from PIL import Image

def convert_images_to_webp(directory):
    """
    Converts all PNG images in the specified directory to WebP format.
    """
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            filepath = os.path.join(directory, filename)
            webp_filename = os.path.splitext(filename)[0] + ".webp"
            webp_filepath = os.path.join(directory, webp_filename)

            try:
                with Image.open(filepath) as img:
                    img.save(webp_filepath, "WEBP", quality=85)
                    print(f"Converted: {filename} -> {webp_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")

if __name__ == "__main__":
    # Point to the images directory
    images_dir = r"c:\Dharmik\TMD\TMD sub domain\Reverse Engineering Services\images"
    convert_images_to_webp(images_dir)
