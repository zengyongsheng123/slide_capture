# import os
# import shutil
#
# # Specify the source and destination folders
# source_folder = "test_images"  # Replace with your source folder path
# destination_folder = "labels"  # Replace with your destination folder path
#
# # Create the destination folder if it doesn't exist
# if not os.path.exists(destination_folder):
#     os.makedirs(destination_folder)
#
# # Loop through all files in the source folder
# for filename in os.listdir(source_folder):
#     # Check if the file is a .txt file
#     if filename.lower().endswith('.txt'):
#         # Construct the full file paths
#         source_path = os.path.join(source_folder, filename)
#         destination_path = os.path.join(destination_folder, filename)
#
#         # Move the file to the destination folder
#         shutil.move(source_path, destination_path)
#         print(f"Moved: {filename}")

# import os
#
# # Specify the folder path containing the .txt files
# folder_path = "labels"  # Replace with your folder path
#
# # Loop through all files in the folder
# for filename in os.listdir(folder_path):
#     # Check if the file is a .txt file
#     if filename.lower().endswith('.txt'):
#         # Construct the full file path
#         file_path = os.path.join(folder_path, filename)
#
#         try:
#             # Read all lines from the file
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 lines = file.readlines()
#
#             # Process only if there are at least 2 lines
#             if len(lines) >= 2:
#                 # Modify the first line (if it starts with "187")
#                 if lines[0].strip().startswith("187"):
#                     lines[0] = "slide" + lines[0][3:]
#
#                 # Modify the second line (if it starts with "188")
#                 if lines[1].strip().startswith("188"):
#                     lines[1] = "target" + lines[1][3:]
#
#             # Join the lines back with original line endings
#             new_content = "".join(lines)
#
#             # Write the modified content back to the file
#             with open(file_path, 'w', encoding='utf-8') as file:
#                 file.write(new_content)
#
#             print(f"Modified: {filename}")
#         except UnicodeDecodeError:
#             print(f"Error: Could not read {filename} with utf-8 encoding.")
#         except IndexError:
#             print(f"Skipped: {filename} (less than 2 lines)")
#
# print("Processing complete.")

import os

# Specify the folder path containing the label files
labels_folder = r"E:\验证码训练\slide_match-main_1\3.yolov8\datasets\train\labels"  # Adjust to your labels folder

# Loop through all files in the labels folder
for filename in os.listdir(labels_folder):
    if filename.lower().endswith('.txt'):
        file_path = os.path.join(labels_folder, filename)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Process each line
        new_lines = []
        for line in lines:
            line = line.strip()
            if not line:  # Skip empty lines
                continue
            parts = line.split()
            if len(parts) < 5:  # Ensure the line has enough parts (class_id + 4 numbers)
                print(f"Skipping invalid line in {filename}: {line}")
                continue
            # Replace 'slide' with '0' and 'target' with '1'
            if parts[0] == 'slide':
                parts[0] = '0'
            elif parts[0] == 'target':
                parts[0] = '1'
            new_lines.append(' '.join(parts))

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_lines) + '\n')

        print(f"Fixed: {filename}")