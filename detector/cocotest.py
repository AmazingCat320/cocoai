# STEP 1: Import the necessary modules.
import numpy as np
import os
import mediapipe as mp
import time
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# STEP 2: Create an ObjectDetector object.
base_options = python.BaseOptions(model_asset_path="efficientdet_lite0.tflite")
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.4)
detector = vision.ObjectDetector.create_from_options(options)

# folderscan
# input variable for implementation
dir = input(r"Enter the path of the folder: ")
con = []
out = []



# start; goes to path
for x in os.listdir(dir):
    # searches for specific filetypes
    if x.endswith(".jpg"):
        con.append(x)
    
# eliminates empty strings from list
con = list(filter(None, con))
print(con)

fscan = 0
while fscan < (len(con)):
    # STEP 3: Load the input image.
    image = mp.Image.create_from_file(con[fscan])
    # STEP 4: Detect objects in the input image.
    detection_result = detector.detect(image)
    result = str(detection_result)

    # result decode
    res = result.split() #split result in words; first pruning
    cls = [] #output list
    nres = len(res) #number of words 
    i = 1
    while i < nres:
        # searches words in res with "category_name" to find class args
        if "category_name" in res[i]:
            j = 14
            obj = str()
            # value of args found after "category_name="; prunes over each letter stopping before ")"
            while res[i][j] != ")":
                obj += res[i][j]
                j += 1
            # output has double brackets "" and '' due to input style
            cls.append(obj)
        i += 1
    # final pruning; eliminates double brackets
    cls = [sub.replace("'", "") for sub in cls]
    cls = list(dict.fromkeys(cls))
    print(cls)
    out.append(dir + con[fscan])
    out.append(cls)

    # STEP 5: Process the detection result. In this case, visualize it.
    image_copy = np.copy(image.numpy_view())
    annotated_image = visualize(image_copy, detection_result)
    rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    cv2.imread(con[fscan])
    cv2.imshow("coco", rgb_annotated_image)
    cv2.waitKey(0)
    
    fscan += 1
    
print(out)
print("second image, first class", out[3][1])

print("Search by class in image; Keywords: ")
command = input(r"Search in images:")

f = 1
nr_res = 0
while f < len(out):
    if command in out[f]:
        nr_res += 1
        print("Found in image: ", out[f-1])
    f += 2
if nr_res == 0:
    print("no results found")