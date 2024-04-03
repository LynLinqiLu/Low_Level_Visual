import os
import csv


# Define the base directory where'athec' folder is located
base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"

if base_dir not in sys.path:
    sys.path.append(base_dir)

from athec import misc

# Define the image folders using the base directory
img_folder = os.path.join(base_dir, "image", "original")
resize_folder = os.path.join(base_dir, "image", "resize")

# Ensure the resize folder exists
os.makedirs(resize_folder, exist_ok=True)

#List to store results for each image
results_list = []

# Loop through each image in the original folder
for imgname in os.listdir(img_folder):
    if imgname.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(img_folder, imgname)
        resize_path = os.path.join(resize_folder, imgname)
        
        # Dictionary to store results for the current image
        image_results = {'Image Name': imgname}

        # Get image mode
        result_mode = misc.attr_mode(img_path)
        image_results['Image Mode'] = result_mode
        misc.printd(result_mode)

        # Resize the image while keeping its original aspect ratio
        result_resize = misc.tf_resize(img_path, resize_path, max_side=300)
        image_results['Resize Result'] = result_resize
        misc.printd(result_resize)

        # Calculate various attributes of the resized image
        result_size = misc.attr_size(resize_path)
        image_results['Image Size Attributes'] = result_size
        misc.printd(result_size)
        
        # Add the results for the current image to the results list
        results_list.append(image_results)

# Specify the CSV file name
csv_file = os.path.join(base_dir, "image_processing_results.csv")

# Write the results to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Image Name', 'Image Mode', 'Resize Result', 'Image Size Attributes']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for result in results_list:
        writer.writerow(result)

print(f"Results written to {csv_file}")
















# Loop through each image in the original folder
for imgname in os.listdir(img_folder):
    if imgname.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(img_folder, imgname)
        resize_path = os.path.join(resize_folder, imgname)

        # Get image mode
        result = misc.attr_mode(img_path)
        misc.printd(result)

        # Resize the image while keeping its original aspect ratio
        result = misc.tf_resize(img_path, resize_path, max_side=300)
        misc.printd(result)

        # Calculate various attributes of the resized image
        result = misc.attr_size(resize_path)
        misc.printd(result)
