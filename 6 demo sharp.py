
import os, csv
from athec import misc, saliency, sharp  # Import sharp module as well

# Define the directories
base_dir = "..."
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder = os.path.join(base_dir, "image", "transform")
results_folder = os.path.join(base_dir, "results")

# Ensure the target folders for saving sharpness visualizations exist
for subfolder in ["sharp laplacian", "sharp fft", "sharp mlv"]:
    os.makedirs(os.path.join(tf_folder, subfolder), exist_ok=True)

# CSV file setup
csv_file_path = os.path.join(results_folder, "sharpness_analysis_results_v2.csv")
headers = ["Image Name", "Sharpness Laplacian", "Sharpness FFT", "Sharpness MLV", "DOF Summary"]

# Ensure the results directory exists
os.makedirs(results_folder, exist_ok=True)


# Open CSV file to write results
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write the header row

    # Loop through images in the resize directory
    for imgname in os.listdir(resize_folder):
        if imgname.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            img_path = os.path.join(resize_folder, imgname)

            # Perform sharpness analysis using different methods
            result_laplacian = sharp.attr_sharp_laplacian(img_path,
                                                          save_path=os.path.join(tf_folder, "sharp laplacian", imgname))['sharp_laplacian']
            result_fft = sharp.attr_sharp_fft(img_path,
                                              save_path=os.path.join(tf_folder, "sharp fft", imgname))['sharp_fft']
            result_mlv = sharp.attr_sharp_mlv(img_path,
                                              save_path=os.path.join(tf_folder, "sharp mlv", imgname))['sharp_mlv']
            result_dof = sharp.attr_dof_block(img_path,
                                              sharp_method=sharp.attr_sharp_fft,   
                                              return_summary=True,
                                              return_block=True)  # Adjust based on your preference

            # Create a flattened DOF summary for CSV writing
            dof_summary_flattened = ", ".join(f"{k}: {v}" for k, v in result_dof.items())

            # Write results for the current image to the CSV file
            writer.writerow([imgname, result_laplacian, result_fft, result_mlv, dof_summary_flattened])

print(f"Sharpness analysis results have been saved to {csv_file_path}.")



