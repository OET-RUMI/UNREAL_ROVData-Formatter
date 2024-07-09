import os
from PIL import Image
import piexif

def set_exif_data(image_path, focal_length, focal_length_35mm, lens_model, lens_make=None):
    try:
        img = Image.open(image_path)
        
        # Set the focal length in the EXIF data
        exif_dict['Exif'][piexif.ExifIFD.FocalLength] = (int(focal_length * 100), 100)
        exif_dict['Exif'][piexif.ExifIFD.FocalLengthIn35mmFilm] = int(focal_length_35mm)
        
        # Set the lens model in the EXIF data
        exif_dict['Exif'][piexif.ExifIFD.LensModel] = lens_model.encode('utf-8')
        if lens_make:
            exif_dict['Exif'][piexif.ExifIFD.LensMake] = lens_make.encode('utf-8')
        
        # Convert the exif dictionary to bytes
        exif_bytes = piexif.dump(exif_dict)
        
        # Save the image with the new EXIF data
        img.save(image_path, 'jpeg', exif=exif_bytes)
        print(f"Focal length set to {focal_length}mm (35mm equivalent: {focal_length_35mm}mm) with lens model '{lens_model}' for image {image_path}")
    except Exception as e:
        print(f"Error setting EXIF data for image {image_path}: {e}")

def process_images(directory, focal_length, focal_length_35mm, lens_model, lens_make=None):
    # Normalize the directory path
    directory = os.path.abspath(directory)
    
    for filename in os.listdir(directory):
        if filename.lower().endswith(('jpg', 'jpeg')):
            image_path = os.path.join(directory, filename)
            set_exif_data(image_path, focal_length, focal_length_35mm, lens_model, lens_make)

if __name__ == "__main__":
    # User inputs
    directory = input("Enter the directory containing images: ").strip('"')
    focal_length = float(input("Enter the focal length value to set (in mm): "))
    focal_length_35mm = float(input("Enter the 35mm equivalent focal length value (in mm): "))
    lens_model = input("Enter the lens model (e.g., 'Canon EF 8-14mm f/4L Fisheye USM'): ").strip()
    lens_make = input("Enter the lens make (optional, e.g., 'Canon'): ").strip() or None
    
    process_images(directory, focal_length, focal_length_35mm, lens_model, lens_make)
    print("Processing complete.")
