import os
import csv
from athec import misc, saliency

# Define the directories
base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder = os.path.join(base_dir, "image", "transform")
results_folder = os.path.join(base_dir, "results")

# Ensure that the results directory exists
os.makedirs(results_folder, exist_ok=True)

# Define CSV file path and headers
results_csv_path = os.path.join(results_folder, "saliency_results.csv")
headers = ["Image Name", "Saliency Spectral Total", "Saliency Fine Total", "Saliency Box Size", "Saliency Box Coordinates (x1, y1, x2, y2)", "Saliency Consistency", "COM X", "COM Y", "Distance to Center", "Rule of Thirds Max"]

# Open the CSV file and write the header
with open(results_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    # Loop through images in the resize directory
    for imgname in os.listdir(resize_folder):
        if imgname.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            img_path = os.path.join(resize_folder, imgname)
            print(f"Processing: {imgname}")

            # Apply saliency detection methods
            saliency_spectral = saliency.tf_saliency_spectral_residual(
                img_path, save_path=os.path.join(tf_folder, "saliency spectral", imgname))
            saliency_fine = saliency.tf_saliency_fine_grained(
                img_path, save_path=os.path.join(tf_folder, "saliency fine", imgname))

            # Calculate complexity and attributes
            complexity_spectral = saliency.attr_complexity_saliency(saliency_spectral)
            complexity_fine = saliency.attr_complexity_saliency(saliency_fine)
            complexity_box = saliency.attr_complexity_saliency_box(saliency_spectral)
            consistency = saliency.attr_complexity_saliency_consistency(saliency_spectral, saliency_fine)
            com = saliency.attr_ruleofthirds_centroid(saliency_spectral)
            thirds_max = saliency.attr_ruleofthirds_band(saliency_spectral)

            # Prepare the row to be written for this image
            row = [
                imgname,
                complexity_spectral["saliency_total"],
                complexity_fine["saliency_total"],
                complexity_box["saliency_box_size"],
                f'({complexity_box["saliency_box_x1"]}, {complexity_box["saliency_box_y1"]}, {complexity_box["saliency_box_x2"]}, {complexity_box["saliency_box_y2"]})',
                consistency["saliency_consistency"],
                com["com_x"],
                com["com_y"],
                com["balance_com_center"],
                thirds_max["rot_band_int"]
            ]

            # Write the row to the CSV file
            writer.writerow(row)

            print(f"Results for {imgname} written to CSV.")
