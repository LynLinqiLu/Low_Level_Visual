
import os
import csv
from athec import misc, edge

base_dir = "C:/Users/linqi/Documents/PTCM/Final_1584/after/athec"

img_folder = os.path.join(base_dir, "image", "original")
resize_folder = os.path.join(base_dir, "image", "resize")
tf_folder = os.path.join(base_dir, "image", "transform")
results_folder = os.path.join(base_dir, "results")

# Ensure necessary folders exist
os.makedirs(os.path.join(tf_folder, "edge_canny"), exist_ok=True)
os.makedirs(os.path.join(tf_folder, "bounding_box_edge_canny"), exist_ok=True)


# Initialize list to store results for each image
edge_analysis_results = []

# Loop through each image in the resize folder
for imgname in os.listdir(resize_folder):
    img_path = os.path.join(resize_folder, imgname)
    
    # Perform edge detection
    edges = edge.tf_edge_canny(img_path,
                               save_path=os.path.join(tf_folder, "edge_canny", imgname),
                               thresholds=None, 
                               otsu_ratio=0.5,
                               gaussian_blur_kernel=(5,5))
    
    # Calculate edge complexity
    edge_complexity_result = edge.attr_complexity_edge(edges, n_random=1000)

    # Calculate edge complexity based on bounding box
    edge_box_result = edge.attr_complexity_edge_box(edges,
                                                    save_path=os.path.join(tf_folder, "bounding_box_edge_canny", imgname),
                                                    min_perentage=0.9,
                                                    check_interval=1)
    
    # Collect results
    image_results = {
        'Image Name': imgname,
        'Edge Complexity': edge_complexity_result,
        'Bounding Box Edge Complexity': edge_box_result
    }
    
    edge_analysis_results.append(image_results)

# CSV file path
csv_file = os.path.join(results_folder, "edge_analysis_results.csv")

# Write the results to a CSV file
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Image Name', 'Edge Complexity', 'Bounding Box Edge Complexity']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for result in edge_analysis_results:
        writer.writerow(result)

print(f"Edge analysis results written to {csv_file}")





# imgname = "example1.jpg"
# img = os.path.join(resize_folder, imgname)

# '''
# Perform Canny edge detection.
# Return a 2-D array.
# save_path (optional, default None): str. If provided, a visualization will be saved to this location.
# otsu_ratio (optional, default 0.5): float. Canny edge detection needs input for lower and upper limits. The function will use Otsu method to find the lower and upper limits. otsu_ratio is the ratio between the lower limit and the upper limit.
# thresholds (optional, default None): a tuple of two integers. If provided, the function will use these two numbers as the lower and upper limits. See https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html
# gaussian_blur_kernel (optional, default None): a tuple of two integers. This argument specifies the width and height of the kernel of a Gausssian blur filter. Both numbers should be positive and odd. If this argument is provided, a Gausssian blur will be applied before edge detection. This step is to remove noise in the image. See https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html and https://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
# '''

# edges = edge.tf_edge_canny(img,
#                            save_path = os.path.join(tf_folder, "edge canny", imgname),
#                            thresholds = None, 
#                            otsu_ratio = 0.5,
#                            gaussian_blur_kernel = (5,5))

# '''
# Calculate visual complexity based on the edge map.
# Return the percentage of image area occupied by edges and the average distance among all the pairs of edge points (divided by diagonal length).
# n_random (optional, default None): int. If provided, the function will calculate the average distance among a random subset of edge points to speed up calculations.
# '''

# result = edge.attr_complexity_edge(edges,
#                                    n_random = 1000)
# misc.printd(result)

# '''
# This function can also take the file path of the edge image as the input.
# '''
# edge_path = os.path.join(tf_folder, "edge canny", imgname + '.png')
# result = edge.attr_complexity_edge(edge_path)
# misc.printd(result)

# '''
# Calculate visual complexity based on the relative size of a minimal bounding box that contains a certain percentage of edge points.
# Return:
# (1) The size of the box, divided by image size
# (2) The coordinates of the box. The upper-left corner of the image is (0, 0).
# save_path (optional, default None): str. If provided, a visualization will be saved to this location.
# min_perentage (optional, default 0.9): float. The minimal percentage of edge points this bounding box should contain.
# check_interval (optional, default 1): int. The interval the function will search by for the bounding box. Increasing this number can speed up calculations but results are less accurate.
# '''
# result = edge.attr_complexity_edge_box(edges,
#                                       save_path = os.path.join(tf_folder, "bounding box edge canny", imgname),
#                                       min_perentage = 0.9,
#                                       check_interval = 1)

# misc.printd(result)
