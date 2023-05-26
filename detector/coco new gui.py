# STEP 1: Import the necessary modules.
import numpy as np
import os
import mediapipe as mp
import time
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import customtkinter
from tkinter import Tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

# STEP 2: Create an ObjectDetector object.
base_options = python.BaseOptions(model_asset_path="efficientdet_lite0.tflite")
options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.4)
detector = vision.ObjectDetector.create_from_options(options)


# input variable for implementation
con = []
out = []

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("500x350")
root.title('CocoAI')
root.iconbitmap("AppLogo.ico")

tabview = customtkinter.CTkTabview(master=root)
tabview.pack(pady=20, padx=60, fill="both", expand=True)

tabview.add("Scan")
tabview.add("Search")
tabview.set("Scan")

def path_entry():
    global dir
    global con 
    con = []
    dir = askdirectory(title='Select Folder')
    # start; goes to path
    for x in os.listdir(dir):
        # searches for specific filetypes
        if x.endswith(".jpg"):
            con.append(x)   
    # eliminates empty strings from list
    con = list(filter(None, con))
    print(con)
    text.configure(text=con)


def image_scan():
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
        out.append(dir + "/" + con[fscan])
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
    text2.configure(text=out)


def search():
    command = entry2.get()
    # search algorythm
    f = 1
    nr_res = 0
    while f < len(out):
        if command in out[f]:
            nr_res += 1
            print("Found in image: ", out[f-1])
            text3.configure(text="Found in image: " + out[f-1])
        f += 2
    if nr_res == 0:
        print("No results found")
        text3.configure(text="No results found")

label =customtkinter.CTkLabel(tabview.tab("Scan"), text="Insert Folder path")
label.pack(pady=12, padx=10)

# path to folder box
entry1 = customtkinter.CTkButton(tabview.tab("Scan"), text="Select", command= path_entry )
entry1.pack()

# output folder scan
text = customtkinter.CTkLabel(tabview.tab("Scan"), width=40, height=10, text="")
text.pack()

# confirm scan
button1 = customtkinter.CTkButton(tabview.tab("Scan"), text="Scan", command= image_scan )
button1.pack()

# image scan output
text2 = customtkinter.CTkLabel(tabview.tab("Scan"), width=40, height=10, text="")
text2.pack()

# search intruction
label =customtkinter.CTkLabel(tabview.tab("Search"), text="Search elements in images")
label.pack(pady=12, padx=10)

# search box
entry2 = customtkinter.CTkEntry(tabview.tab("Search"), placeholder_text="Search elements in images: ")
entry2.pack(pady=12, padx=10)

# confirm search
button2 = customtkinter.CTkButton(tabview.tab("Search"), text="Search", command= search)
button2.pack()

# search output
text3 = customtkinter.CTkLabel(tabview.tab("Search"), width=40, height=10, text="")
text3.pack()

root.mainloop()