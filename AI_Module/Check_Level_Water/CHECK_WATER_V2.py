# KIỂM TRA MỰC NƯỚC CÓ ĐỦ KHÔNG

import cv2
import numpy as np

SIZE = (500, 500)
CHECK = []

image_path = "image_product/good.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image, SIZE)
# Điều chỉnh độ mờ, làm mịn ảnh
image_GauBlur = cv2.GaussianBlur(image,(3,3),0) 
hsv_image = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2HSV)
target_color_low = np.array([0, 0, 0])
target_color_high = np.array([180, 255, 30])
color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high)
# Lật vùng trắng và đen
color_mask = cv2.bitwise_not(color_mask)
# Tạo một hình chữ nhật chỉ định khu vực mực nước chuẩn.
X_ROI_WATER, Y_ROI_WATER = 0,174
size_x_ROI_WATER = 500
size_y_ROI_WATER = 20
ROI_WATER = color_mask[Y_ROI_WATER : Y_ROI_WATER + size_y_ROI_WATER,X_ROI_WATER:X_ROI_WATER + size_x_ROI_WATER]

# Tạo một hình chữ Nhật kiểm tra lượng nước vượt mức giới hạn
X_ROI_WATER_OUT, Y_ROI_WATER_OUT = 0,153
size_x_ROI_WATER_OUT = 500
size_y_ROI_WATER_OUT = 20
ROI_WATER_OUT = color_mask[Y_ROI_WATER_OUT : Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT,X_ROI_WATER_OUT:X_ROI_WATER_OUT + size_x_ROI_WATER_OUT]

if np.any(ROI_WATER_OUT != 255):
    CHECK.append("ERRORLABEL") 
# Kiểm tra xem có pixel 225 trong khu vực mực nước được chỉ định không, 
if np.any(ROI_WATER != 255):
    CHECK.append("GOOD")
else:
   CHECK.append("ERRORLABEL")

if "ERRORLABEL" in CHECK:
    print("Water: Error")
    cv2.rectangle(image,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (0,0,255),2)
    cv2.rectangle(image,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (0,0,255),2)
    cv2.putText(image,"Water: ERROR", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2 )
    cv2.imshow("Image_error_highlighted",image)
else:
    print("Water: Good")
    cv2.putText(image,"Water: GOOD", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2 )
    cv2.rectangle(image,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (255,0,0),2)
    cv2.rectangle(image,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (255,0,0),2)
    cv2.imshow("Org",image)
cv2.rectangle(color_mask,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (0,0,255),2)
cv2.rectangle(color_mask,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (0,0,255),2)
cv2.imshow("color_mask",color_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()

