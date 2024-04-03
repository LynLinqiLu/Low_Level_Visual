import os
import csv
from athec import misc, segment

# Define the base directory and subdirectories
base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder_quickshift = os.path.join(base_dir, "image", "transform", "segment quickshift")
tf_folder_normalized_cut = os.path.join(base_dir, "image", "transform", "segment normalized cut")
results_csv_path = os.path.join(base_dir, "segmentation_results.csv")

# Ensure target folders for output exist
os.makedirs(tf_folder_quickshift, exist_ok=True)
os.makedirs(tf_folder_normalized_cut, exist_ok=True)

# Prepare CSV file for results
with open(results_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the headers to the CSV file
    writer.writerow(["Image Name", "Segmentation Method", "Number of Segments",
                     "Segments > 0.05", "Segments > 0.02", "Segments > 0.01",
                     "Top 5 Areas"])

# Process each image
images = [f for f in os.listdir(resize_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for imgname in images:
    img_path = os.path.join(resize_folder, imgname)
    
    # Perform Quickshift segmentation
    segment_qs = segment.tf_segment_quickshift(img_path,
                                               save_path=os.path.join(tf_folder_quickshift, imgname),
                                               ratio=1,
                                               kernel_siz=5,
                                               max_dist=10,
                                               sigma=0)
    # Calculate complexity for Quickshift
    result_qs = segment.attr_complexity_segment(segment_qs,
                                                segment_thresholds=[0.05, 0.02, 0.01],
                                                top_areas=5)

    # Perform Normalized Cut segmentation
    segment_nc = segment.tf_segment_normalized_cut(img_path,
                                                   save_path=os.path.join(tf_folder_normalized_cut, imgname),
                                                   km_n_segments=100,
                                                   km_compactness=30,
                                                   rag_sigma=100,
                                                   nc_thresh=0.001,
                                                   nc_num_cuts=10,
                                                   nc_max_edge=1.0)
    # Calculate complexity for Normalized Cut
    result_nc = segment.attr_complexity_segment(segment_nc)

    # Open the CSV file and write the results for each segmentation
    with open(results_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([imgname, "Quickshift", *result_qs.values()])
        writer.writerow([imgname, "Normalized Cut", *result_nc.values()])

print("All images processed and results saved to CSV.")
