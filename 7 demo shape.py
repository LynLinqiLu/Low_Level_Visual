import os
import csv
from athec import misc, edge, shape
import numpy as np

# Directories
img_folder = os.path.join("image", "original")
resize_folder = os.path.join("image", "resize")
tf_folder = os.path.join("image", "transform")
line_hough_edge_canny_folder = os.path.join(tf_folder, "line hough edge canny")

# Ensure the folder for saving line detection visualizations exists
if not os.path.exists(line_hough_edge_canny_folder):
    os.makedirs(line_hough_edge_canny_folder)

# CSV file to store the results
csv_file = os.path.join("image", "line_statistics.csv")

# Prepare the header for the CSV file
header = ['image_name', 'n_line', 'n_line_hor', 'n_line_slant', 'n_line_ver']

# Function to process each image and return the required line statistics
def process_image(image_path):
    # Perform Canny edge detection
    edges = edge.tf_edge_canny(image_path, otsu_ratio=0.5, gaussian_blur_kernel=(5,5))

    # Calculate line dynamics based on the edge map
    result = shape.attr_line_hough_edge(
        edges,
        save_path = os.path.join(line_hough_edge_canny_folder, os.path.basename(image_path)),
        horizontal_degree = 10,
        vertical_degree = 80,
        HoughLinesP_rho = 1,
        HoughLinesP_theta = np.pi/90,
        HoughLinesP_threshold = 50,
        HoughLinesP_minLineLength = 10,
        HoughLinesP_maxLineGap = 2,
        return_summary = True
    )

    return result

# Write the header to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# Loop through the images in the resize folder and process them
for img_name in os.listdir(resize_folder):
    img_path = os.path.join(resize_folder, img_name)
    if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        result = process_image(img_path)

        # Extract the required attributes
        line_stats = {
            'n_line': result['n_line'],
            'n_line_hor': result['n_line_hor'],
            'n_line_slant': result['n_line_slant'],
            'n_line_ver': result['n_line_ver']
        }

        # Write the extracted attributes to the CSV file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([img_name, line_stats['n_line'], line_stats['n_line_hor'], line_stats['n_line_slant'], line_stats['n_line_ver']])

print("Processing complete. The line statistics have been saved to", csv_file)
