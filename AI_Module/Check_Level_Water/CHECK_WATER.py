# KIỂM TRA MỰC NƯỚC CÓ ĐỦ KHÔNG

import cv2
import numpy as np

SIZE = (500,500)
CHECK = []

image_path = "image_product/error_w_l.jpg"
image = cv2.imread(image_path)

image = cv2.resize(image,SIZE)

#Chuyển ảnh về ảnh xám
image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# Điều chỉnh độ mờ, làm mịn ảnh
image_GauBlur = cv2.GaussianBlur(image_gray,(3,3),0) 
ret,image_thres = cv2.threshold(image_GauBlur, 95, 255,cv2.THRESH_BINARY)

# Tạo một hình chữ nhật chỉ định khu vực mực nước chuẩn.
X_ROI_WATER, Y_ROI_WATER = 0,174
size_x_ROI_WATER = 500
size_y_ROI_WATER = 20
ROI_WATER = image_thres[Y_ROI_WATER : Y_ROI_WATER + size_y_ROI_WATER,X_ROI_WATER:X_ROI_WATER + size_x_ROI_WATER]

# Tạo một hình chữ Nhật kiểm tra lượng nước vượt mức giới hạn
X_ROI_WATER_OUT, Y_ROI_WATER_OUT = 0,153
size_x_ROI_WATER_OUT = 500
size_y_ROI_WATER_OUT = 20
ROI_WATER_OUT = image_thres[Y_ROI_WATER_OUT : Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT,X_ROI_WATER_OUT:X_ROI_WATER_OUT + size_x_ROI_WATER_OUT]

if np.any(ROI_WATER_OUT != 255):
    CHECK.append("ERRORLABEL") 
# Kiểm tra xem có pixel 225 trong khu vực mực nước được chỉ định không, 
if np.any(ROI_WATER != 255):
    CHECK.append("GOOD")
else:
   CHECK.append("ERRORLABEL")

if "ERRORLABEL" in CHECK:
    cv2.rectangle(image,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (0,0,255),2)
    cv2.rectangle(image,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (0,0,255),2)
    cv2.putText(image,"Water: ERROR", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2 )
    cv2.imshow("Image_error_highlighted",image)
else:
    cv2.putText(image,"Water: GOOD", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2 )
    cv2.rectangle(image,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (255,0,0),2)
    cv2.rectangle(image,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (255,0,0),2)
    cv2.imshow("Org",image)
cv2.rectangle(image_thres,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (0,0,255),2)
cv2.rectangle(image_thres,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (0,0,255),2)
cv2.imshow("ThresHold",image_thres)

cv2.waitKey(0)
cv2.destroyAllWindows()

