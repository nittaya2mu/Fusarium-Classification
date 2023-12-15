import cv2
import numpy as np
import os

def process_image(image_path, output_folder):
    # Read the input image
    image = cv2.imread(image_path)

    # Ensure the image is not None
    if image is not None:
        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds of the white color (including shadow) in HSV
        lower_white = np.array([0, 0, 150], dtype=np.uint8)
        upper_white = np.array([255, 50, 255], dtype=np.uint8)

        # Create a binary mask using color thresholding
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # Invert the mask to select the foreground
        foreground_mask = cv2.bitwise_not(mask)

        # Create a black background of the same size as the original image
        black_background = np.zeros_like(image)

        # Copy the foreground (non-white regions) to the black background
        black_background[foreground_mask != 0] = image[foreground_mask != 0]

        # Save the result with a new name in the output folder
        output_path = os.path.join(output_folder, f'result_{os.path.basename(image_path)}')
        cv2.imwrite(output_path, black_background)
        
        #print(f"Processed: {image_path} -> {output_path}")
    else:
        print(f"Failed to read image: {image_path}")

def process_images_in_folder(input_folder, output_folder):
    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        print("Input folder not found.")
        return
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):  # Consider only image files
            # Construct the full path to the input image
            input_path = os.path.join(input_folder, filename)

            # Process the image
            process_image(input_path, output_folder)

# Specify the input folder containing the images
input_folder_path = 'crop/day15new'  # Replace with the actual input folder path

# Specify the output folder for processed images
output_folder_path = 'process/day15process'  # Replace with the actual output folder path

# Perform the processing for all images in the folder
process_images_in_folder(input_folder_path, output_folder_path)
print("complete")