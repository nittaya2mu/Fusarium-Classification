import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os

root = tk.Tk()
root.title("GUI")

# Declare a variable for the image
img = None
img_cropped = None
# custom_font = font.Font(family="Arial", size=20)

def selectPic():
     global img
     global img_cropped
     filename = filedialog.askopenfilename(initialdir="/images", title="Select Image", filetypes=(("png images", "*.png"), ("jpeg images", "*.jpeg"), ("jpg images", "*.jpg")))
     img = Image.open(filename)
     img = img.resize((256, 256), Image.ANTIALIAS)
     img_cropped = None 
     img = ImageTk.PhotoImage(img)

    # Display the image in the Label
     img_label.config(image=img, bg="red")
     img_label.image = img

def calCualte_img():
    global img
    global img_cropped
    if img is not None:
        # Continue with the rest of the code as before
        original_width, original_height = img.width(), img.height()
        target_size = (180, 180)

        # Check if the image is large enough to be cropped
        if original_width >= target_size[0] and original_height >= target_size[1]:
            left = (original_width - target_size[0]) // 2
            top = (original_height - target_size[1]) // 2
            right = (original_width + target_size[0]) // 2
            bottom = (original_height + target_size[1]) // 2

          # Crop the image
            # img_cropped = img.crop((left, top, right, bottom))
            img_cropped = img
            # Display the cropped image
            img_label2.config(image=img_cropped, bg="green")
            img_label2.image = img_cropped
        else:
            print("Image is too small for cropping")
            print(original_height,original_width)

def calCualte_img2(img):
     img_label3.config(image=img, bg="blue")
     img_label3.image = img   


     
 
#title image       
Level_result = tk.Label(root,text="Normal Image",fg="red")
Level_result.place(x=90,y=50)

Level_result = tk.Label(root,text="Crop Image",fg="green")
Level_result.place(x=400,y=50)

Level_result = tk.Label(root,text="Subtraction Background Image",fg="blue")
Level_result.place(x=620,y=50)

# Create Label to display the image in the main window
img_label = tk.Label(root)
img_label.place(x=10, y=80)

img_label2 = tk.Label(root)
img_label2.place(x=300, y=80)


img_label3 = tk.Label(root)
img_label3.place(x=590, y=80)

# Create buttons
upload_btn = tk.Button(root, text="Upload Image", fg="red", command=selectPic)
upload_btn.place(x=70, y=350)

calculate_btn = tk.Button(root, text="Calculate Image", command=calCualte_img)
calculate_btn.place(x=60, y=390)

calculate_btn2 = tk.Button(root, text="Calculate Image 2", command=calCualte_img2)
calculate_btn2.place(x=360, y=370)

#Create Level  and
#Create a label to display the numeric value

showLevel_1 = tk.Label(root,text="Level 1")
showLevel_1.place(x=900,y=80)
show_result_1 = tk.Entry(root, text="")
show_result_1.place(x=950,y=80)

showLevel_2 = tk.Label(root,text="Level 2")
showLevel_2.place(x=900,y=120)
show_result_2 = tk.Entry(root, text="")
show_result_2.place(x=950,y=120)

showLevel_3 = tk.Label(root,text="Level 3")
showLevel_3.place(x=900,y=170)
show_result_3 = tk.Entry(root, text="")
show_result_3.place(x=950,y=170)

showLevel_4 = tk.Label(root,text="Level 4")
showLevel_4.place(x=900,y=220)
show_result_4 = tk.Entry(root, text="")
show_result_4.place(x=950,y=220)

showLevel_5 = tk.Label(root,text="Level 5")
showLevel_5.place(x=900,y=270)
show_result_5 = tk.Entry(root, text="")
show_result_5.place(x=950,y=270)


Level_result = tk.Label(root,text="Result",fg="red")
Level_result.place(x=900,y=320)
show_Level_result = tk.Entry(root, text="")
show_Level_result.place(x=950,y=320)


root.geometry("1200x500")
root.mainloop()
