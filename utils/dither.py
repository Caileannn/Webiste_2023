import os
from PIL import Image
import hitherdither
import shutil

def dither_image(img_path, rel_dir):
    # Open the original image
    img = Image.open(img_path).convert('RGB')
    #new_size = (int(img.width * 0.5), int(img.height * 0.5))
    #img_resized = img.resize(new_size)
    # 'low-tech': hitherdither.palette.Palette([(30,32,40), (11,21,71),(57,77,174),(158,168,218),(187,196,230),(243,244,250)]),
	# 'obsolete': hitherdither.palette.Palette([(9,74,58), (58,136,118),(101,163,148),(144,189,179),(169,204,195),(242,247,246)]),
	# 'high-tech': hitherdither.palette.Palette([(86,9,6), (197,49,45),(228,130,124),(233,155,151),(242,193,190),(252,241,240)]),
	# 'grayscale': hitherdither.palette.Palette([(25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250)])

    #dwelling = hitherdither.palette.Palette([(255, 255, 138), (25,25,25), (75,75,75),(125,125,125),(175,175,175),(225,225,225),(250,250,250), (255, 13, 13), (252, 237, 28), (255, 128, 128)])
    palette = hitherdither.palette.Palette.image_distance(img)
    # Create a palette using median cut

    # Perform Bayer dithering
    img_dithered = hitherdither.ordered.bayer.bayer_dithering(
        img, palette, [16, 16, 16], order=8)

    # Resize the dithered image back to the original size
    img_dithered_resized = img_dithered

    # Construct the output path with "d_" prefix and original filename, and change the extension to .png
    output_filename = f"d_{os.path.splitext(os.path.basename(img_path))[0]}.png"
    output_path = os.path.join(os.path.dirname(img_path), output_filename)

    # Save the resized dithered image with the .png extension
    img_dithered_resized.save(output_path)

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
