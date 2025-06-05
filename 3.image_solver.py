from PIL import Image
import os

# Specify the folder path containing the images
folder_path = "test_images"  # Replace with your folder path

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image (you can add more extensions if needed)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Open the image
        img = Image.open(file_path)

        # Define the crop dimensions: keep the top 195 pixels
        width, height = img.size
        crop_height = 195  # Keep the top 195 pixels
        cropped_img = img.crop((0, 0, width, crop_height))

        # Save the cropped image, overwriting the original file
        cropped_img.save(file_path)

        print(f"Processed and replaced: {filename}")