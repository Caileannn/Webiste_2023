import os
from PIL import Image
import hitherdither
import shutil

def dither_image(img_path, rel_dir):

    output_folder = '../pre-dither_imgs/'

    # Open the original image
    img = Image.open(img_path)

    # Create a palette using median cut
    palette = hitherdither.palette.Palette.create_by_median_cut(img, n=9)

    # Perform Bayer dithering
    img_dithered = hitherdither.ordered.bayer.bayer_dithering(
        img, palette, [256/4, 256/4, 256/4], order=16)

    # Construct the output path with "d_" prefix and original filename, and change the extension to .png
    output_filename = f"d_{os.path.splitext(os.path.basename(img_path))[0]}.png"
    output_path = os.path.join(os.path.dirname(img_path), output_filename)

    # Save the dithered image with the .png extension

    img_dithered.save(output_path, format='PNG')

def process_images(input_folder, output_folder):
    # Loop through all files in the input folder and its subfolders
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            # Check if the file is a .png or .jpg
            if file.lower().endswith(('.png', '.jpg')) and not file.startswith('d_'):

                input_path = os.path.join(root, file)
                print(input_path)
                print(output_folder)
                # Get the relative path from input_folder to the current file
                rel_path = os.path.relpath(input_path, input_folder)
                dir_rel_path = os.path.dirname(rel_path)
                #out = os.path.join(output_folder, rel_path)
               
                dither_image(input_path, dir_rel_path)

                # Construct the output path in the same relative structure within the output_folder
                output_path = os.path.join(output_folder, rel_path.replace(os.path.sep, '/'))

                # # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # # Copy the undithered image to another directory
                shutil.move(input_path, output_path)

                

# Example usage
input_folder = '../public/assets/imgs/'
output_folder = '../pre-dither_imgs/'
process_images(input_folder, output_folder)
