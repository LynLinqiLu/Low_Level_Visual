import os
import csv
from athec import misc, color, colordict

# Define the directories
base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder = os.path.join(base_dir, "image", "transform")
results_folder = os.path.join(base_dir, "results")
from athec import misc, color, colordict
# Ensure that the results directory exists
os.makedirs(results_folder, exist_ok=True)

# CSV file setup
csv_file_path = os.path.join(results_folder, "color_analysis_results.csv")
headers = [
    "Image Name", "RGB Mean", "RGB StdDev", "HSV Mean", "HSV StdDev",
    "HSL Mean", "HSL StdDev", "XYZ Mean", "XYZ StdDev", "Lab Mean",
    "Lab StdDev", "Grayscale Mean", "Grayscale StdDev", "Contrast Range",
    "Contrast Lower", "Contrast Upper", "Contrast Peak Number",
    "Contrast Largest Gap", "Colorfulness Hasler", "Colorfulness EMD",
    "Color Percentage", "Hue Count"
]

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header

    # Loop through each image in the resize folder
    for imgname in os.listdir(resize_folder):
        if imgname.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(resize_folder, imgname)
            row = [imgname]  # Start a new row with the image name

            try:
                # Read the image
                img = misc.read_img_rgb(img_path)
                
                # Get color dictionaries if needed
                cd = colordict.color_dict()
                
                # Perform color analysis and collect results
                row.extend(list(color.attr_RGB(img, return_full=True).values()))
                row.extend(list(color.attr_HSV(img, return_full=True).values()))
                row.extend(list(color.attr_HSL(img, return_full=True).values()))
                row.extend(list(color.attr_XYZ(img, return_full=True).values()))
                row.extend(list(color.attr_Lab(img, return_full=True).values()))
                row.extend(list(color.attr_grayscale(img, return_full=True).values()))
                
                # Additional color analyses
                contrast_range_result = color.attr_contrast_range(img)
                row.extend([
                    contrast_range_result['contrast_range'],
                    contrast_range_result['contrast_range_lower'],
                    contrast_range_result['contrast_range_upper']
                ])
                
                contrast_peak_result = color.attr_contrast_peak(img)
                row.extend([
                    contrast_peak_result['contrast_n_peak'],
                    contrast_peak_result['contrast_peak_distance']
                ])
                
                row.append(color.attr_colorful(img)['colorful'])
                row.append(color.attr_colorful_emd(img)['colorful_emd'])
                
                color_percentage_result = color.attr_color_percentage(img, color_dict=cd)
                row.extend(color_percentage_result.values())
                
                hue_count_result = color.attr_hue_count(img)
                row.append(hue_count_result['hue_count'])
                
                # Write the row to the CSV file
                writer.writerow(row)
            except Exception as e:
                print(f"Error processing {imgname}: {e}")
                # Write a row with 'Error' for all values except the image name
                writer.writerow([imgname] + ['Error'] * (len(headers) - 1))

print(f"Color analysis results have been saved to {csv_file_path}.")
