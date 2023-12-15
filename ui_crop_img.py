import cv2
import numpy as np
import os
from tkinter import Tk, filedialog, Button, Label, Frame

class ImageCropperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Image Cropper")

        self.input_folder_path = ""
        self.output_folder_path = ""

        self.label_input_folder = Label(master, text="Input Folder:")
        self.label_input_folder.pack()

        self.button_browse_input = Button(master, text="Browse", command=self.browse_input_folder)
        self.button_browse_input.pack()

        self.label_output_folder = Label(master, text="Output Folder:")
        self.label_output_folder.pack()

        self.button_browse_output = Button(master, text="Browse", command=self.browse_output_folder)
        self.button_browse_output.pack()

        self.button_crop = Button(master, text="Crop Images", command=self.crop_images)
        self.button_crop.pack()

    def browse_input_folder(self):
        self.input_folder_path = filedialog.askdirectory()
        self.label_input_folder["text"] = f"Input Folder: {self.input_folder_path}"

    def browse_output_folder(self):
        self.output_folder_path = filedialog.askdirectory()
        self.label_output_folder["text"] = f"Output Folder: {self.output_folder_path}"

    def crop_images(self):
        if not self.input_folder_path or not self.output_folder_path:
            print("Please select input and output folders.")
            return

        crop_and_save(self.input_folder_path, self.output_folder_path)
        print("Images cropped and saved.")

def crop_and_save(input_folder, output_folder):
    # ตรวจสอบว่า output_folder มีหรือยัง ถ้าไม่มีให้สร้าง
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # อ่านไฟล์ภาพทั้งหมดจาก input_folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # ตรวจสอบนามสกุลไฟล์
            # อ่านภาพ
            image = cv2.imread(os.path.join(input_folder, filename))

            # แปลงภาพเป็นภาพสี HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # กำหนดช่วงสีเขียวที่เป็นสีของใบไม้
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])

            # สร้างมาส์ค์จากช่วงสีเขียว
            mask = cv2.inRange(hsv, lower_green, upper_green)

            # ค้นหา contours จากมาส์ค
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # หา contour ที่มีพื้นที่สูงสุด (เป็นส่วนที่ใหญ่ที่สุด)
            max_contour = max(contours, key=cv2.contourArea)

            # หา bounding box ของ contour ที่ใหญ่ที่สุด
            x, y, w, h = cv2.boundingRect(max_contour)

            # หาจุดกึ่งกลางของ bounding box
            center_x = x + w // 2
            center_y = y + h // 2

            # กำหนดขนาดของรูปที่ต้องการ crop
            crop_size = 512

            # คำนวณตำแหน่งที่จะ crop
            crop_x = max(0, center_x - crop_size // 2)
            crop_y = max(0, center_y - crop_size // 2)

            # Crop ภาพ
            cropped_image = image[crop_y:crop_y + crop_size, crop_x:crop_x + crop_size]

            # ปรับขนาดของรูปที่ crop เป็น 512x512 pixel
            cropped_image = cv2.resize(cropped_image, (512, 512))

            # บันทึกภาพที่ถูก crop ไว้ใน output_folder
            output_path = os.path.join(output_folder, f"cropped_{filename}")
            cv2.imwrite(output_path, cropped_image)


if __name__ == "__main__":
    root = Tk()
    app = ImageCropperGUI(root)
    root.mainloop()