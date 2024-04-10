import os
import csv
from athec import misc, color, colordict

# Define directories.
base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder = os.path.join(base_dir, "image", "transform")
results_folder = os.path.join(base_dir, "results")

# Ensure the results directory exists.
os.makedirs(results_folder, exist_ok=True) 
# CSV file path
csv_file_path = os.path.join(results_folder, "color_results_full.csv")

# Function to process an image and write results to CSV
def process_image(image_path, csv_writer):
    imgname = os.path.basename(image_path)
    print(f"Processing {imgname}...")

    # Full RGB attributes
    rgb_result = color.attr_RGB(image_path, return_full=True)
    
    # HSV attributes
    hsv_result = color.attr_HSV(image_path)
    
    # HSL attributes
    hsl_result = color.attr_HSL(image_path)
    
    # XYZ attributes
    xyz_result = color.attr_XYZ(image_path)
    
    # Lab attributes
    lab_result = color.attr_Lab(image_path)
    
    # Grayscale attributes and transformation
    grayscale_result = color.attr_grayscale(image_path)
    color.tf_grayscale(image_path, save_path = os.path.join(tf_folder, "grayscale", imgname))
    
    # Calculate contrast range
    contrast_range_result = color.attr_contrast_range(image_path, threshold=0.90)
    
    # Calculate contrast based on peak detection
    contrast_peak_result = color.attr_contrast_peak(image_path,
                                                    savgol_filter_window_length=51,
                                                    savgol_filter_polyorder=5,
                                                    savgol_filter_mode="constant",
                                                    argrelmax_order=20)

    # Colorfulness measures
    colorful_result = color.attr_colorful(image_path)
    colorful_emd_result = color.attr_colorful_emd(image_path)
    
    # Get the color dictionary and calculate color percentages
    cd = colordict.color_dict()
    color_percentage_result = color.attr_color_percentage(image_path, color_dict=cd, save_path = os.path.join(tf_folder, "color percentage", imgname))

    # Calculate hue count
    hue_count_result = color.attr_hue_count(image_path, 
                                            saturation_low=0.2, 
                                            value_low=0.15, 
                                            value_high=0.95, 
                                            hue_count_alpha=0.05)

    # Writing results to CSV
    csv_writer.writerow(
    [imgname] +
    [contrast_range_result['contrast_range'], contrast_range_result['contrast_range_lower'], contrast_range_result['contrast_range_upper']] +
    [contrast_peak_result['contrast_n_peak'], contrast_peak_result['contrast_peak_distance']] +
    [','.join(map(str, contrast_peak_result['contrast_peak_list']))] +  # Assuming inclusion of peak list as a string
    [hue_count_result['hue_count'], color_percentage_result['color_shannon'], color_percentage_result['color_simpson']] +
    [color_percentage_result.get(color, 0) for color in ['black', 'blue', 'brown', 'gray', 'green', 'orange', 'pink', 'purple', 'red', 'white', 'yellow']] +
    list(rgb_result.values()) +  # Flatten RGB result values
    list(hsv_result.values()) +  # Flatten HSV result values
    list(hsl_result.values()) +  # Flatten HSL result values
    list(xyz_result.values()) +  # Flatten XYZ result values
    list(lab_result.values()) +  # Flatten Lab result values
    list(grayscale_result.values()) +
    [colorful_result, colorful_emd_result]  # Colorfulness metrics
)

headers = [
    "Image Name", 
    "Contrast Range", "Contrast Range Lower", "Contrast Range Upper",
    "Contrast Peaks Number", "Largest Peak Gap", "Contrast Peak List", "Hue Count",
    "Color Shannon Index", "Color Simpson Index",
    "Black", "Blue", "Brown", "Gray", "Green", "Orange", "Pink", "Purple", "Red", "White", "Yellow",
    # Headers for RGB metrics
    "RGB_R_mean", "RGB_R_median", "RGB_R_std_dev", "RGB_R_min", "RGB_R_max", "RGB_R_quartile_1", "RGB_R_quartile_3", "RGB_R_skew", "RGB_R_kurtosis", "RGB_R_entropy",
    "RGB_G_mean", "RGB_G_median", "RGB_G_std_dev", "RGB_G_min", "RGB_G_max", "RGB_G_quartile_1", "RGB_G_quartile_3", "RGB_G_skew", "RGB_G_kurtosis", "RGB_G_entropy",
    "RGB_B_mean", "RGB_B_median", "RGB_B_std_dev", "RGB_B_min", "RGB_B_max", "RGB_B_quartile_1", "RGB_B_quartile_3", "RGB_B_skew", "RGB_B_kurtosis", "RGB_B_entropy",
    # Headers for HSV metrics
    "HSV_H_mean", "HSV_H_std_dev", "HSV_S_mean", "HSV_S_std_dev", "HSV_V_mean", "HSV_V_std_dev", "HSV_H_circular_mean", "HSV_H_circular_std_dev",
    # Headers for HSL metrics
    "HSL_H_mean", "HSL_H_std_dev", "HSL_S_mean", "HSL_S_std_dev", "HSL_L_mean", "HSL_L_std_dev", "HSL_H_circular_mean", "HSL_H_circular_std_dev",
    # Headers for XYZ metrics
    "XYZ_X_mean", "XYZ_X_std_dev", "XYZ_Y_mean", "XYZ_Y_std_dev", "XYZ_Z_mean", "XYZ_Z_std_dev",
    # Headers for Lab metrics
    "Lab_L_mean", "Lab_L_std_dev", "Lab_a_mean", "Lab_a_std_dev", "Lab_b_mean", "Lab_b_std_dev",
    # Headers for grayscale metrics
    "Gray_Mean", "Gray_Std_Dev", 
    # Headers for colorfulness metrics
    "Colorful", "Colorful_EMD"
    ]

# Open CSV file and write headers
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(headers)
    
    # Iterate over images in the resize folder and process each
    for imgname in os.listdir(resize_folder):
        img_path = os.path.join(resize_folder, imgname)
        if os.path.isfile(img_path):
            process_image(img_path, csv_writer)
    