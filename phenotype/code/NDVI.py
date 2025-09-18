import cv2
import numpy as np
from fastiecm import fastiecm

def findLeafArea(image):
    # แสดงภาพต้นฉบับ
    cv2.imshow('Original Image', image)
    cv2.waitKey(0)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # แสดงภาพ HSV
    cv2.imshow('HSV Image', hsv)
    cv2.waitKey(0)
    
    # กำหนดค่าสีต่ำสุดและสีสูงสุด
    lower_val = (0, 18, 0)
    upper_val = (60, 255, 120)
    
    # ทำ Threshold ในภาพ HSV เพื่อให้ได้เฉพาะสีเขียว
    mask = cv2.inRange(hsv, lower_val, upper_val)
    
    # แสดง Mask
    cv2.imshow('Mask', mask)
    cv2.waitKey(0)
    
    # ทำการดำเนินการทางมอร์โฟโลจิค
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # ค้นหา Contours และกรองเพื่อหา Contour ที่ใหญ่ที่สุด
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    
    # สร้าง Mask ที่เป็นไบนารีที่กำหนดเฉพาะวัตถุที่ถูก Segment
    final_mask = np.zeros_like(mask)
    cv2.drawContours(final_mask, [cnts], -1, (255), thickness=cv2.FILLED)
    
    # แสดง Mask ที่เต็มขีด
    cv2.imshow('Filled Mask', final_mask)
    cv2.waitKey(0)
    
    number_of_white_pix = np.sum(final_mask == 255)
    convertToCm = 0.0264583333 * number_of_white_pix
    
    print('ผลลัพธ์ :', convertToCm, 'cm^2 ')
    
    cv2.destroyAllWindows()

    return convertToCm, final_mask

def extractItemWithWhiteBackground(original, final_mask):
    # สร้างพื้นหลังสีขาว
    white_background = np.ones_like(original) * 255

    # คัดลอกวัตถุที่ถูก Segment ไปยังพื้นหลังสีขาว
    result_image = white_background.copy()
    result_image[final_mask == 255] = original[final_mask == 255]

    # แสดงภาพผลลัพธ์
    cv2.imshow('Result Image', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return result_image

def calc_ndvi(image, mask):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom == 0] = 0.01
    ndvi = (r.astype(float) - b) / bottom

    # ใช้ Mask เพื่อไม่รวมพื้นที่ที่ไม่ได้ Segment
    ndvi_masked = ndvi * (mask == 255)

    # พิมพ์สถิติเฉพาะสำหรับพื้นที่ที่ถูก Segment เท่านั้น
    print(f"NDVI min: {ndvi_masked[ndvi_masked != 0].min()}\n"
          f"NDVI max: {ndvi_masked.max()}\n"
          f"NDVI mean: {ndvi_masked[ndvi_masked != 0].mean()}")
    
    return ndvi_masked

def display(image, image_name):
    image = np.array(image, dtype=float) / float(255)
    shape = image.shape
    height = int(shape[0] / 2)
    width = int(shape[1] / 2)
    image = cv2.resize(image, (width, height))
    cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

# ที่อยู่ของภาพนำเข้า
image_path = "C:/phenotype/code/images/2.jpg"
original = cv2.imread(image_path)  # อ่านภาพต้นฉบับ

# รับผลลัพธ์พื้นที่ใบไม้และ Mask สุดท้าย
area, final_mask = findLeafArea(original)

# ดึงวัตถุที่ถูก Segment พร้อมพื้นหลังสีขาว
original = extractItemWithWhiteBackground(original, final_mask)

# แสดงภาพต้นฉบับและภาพที่ปรับความคมชัด
display(original, 'Original')
contrasted = contrast_stretch(original)
display(contrasted, 'Contrasted original')

# บันทึกภาพที่ปรับความคมชัด
cv2.imwrite('contrasted.png', contrasted)

# คำนวณ NDVI และแสดงผล
ndvi = calc_ndvi(original,final_mask)
display(ndvi, 'NDVI')
ndvi_contrasted = contrast_stretch(ndvi)
display(ndvi_contrasted, 'NDVI Contrasted')

# บันทึกภาพ NDVI ที่ปรับความคมชัด
cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)

# จัดสีให้กับ NDVI และแสดงผล
color_mapped_prep = ndvi_contrasted.astype(np.uint8)
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
display(color_mapped_image, 'Color mapped')
cv2.imwrite('color_mapped_image.png', color_mapped_image)
