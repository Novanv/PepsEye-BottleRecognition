import cv2
import numpy as np
import matplotlib.pyplot as plt

SIZE = (500, 500)
CHECK = []

image_path = "image_data/w2.jpg"
image = cv2.imread(image_path)
image = image[60:420,120:520]
# Áp dụng Gaussian Blur
image_GauBlur = cv2.GaussianBlur(image, (3, 3), 0)
cv2.imshow("..",image_GauBlur)
# Chuyển đổi ảnh sang ảnh grayscale
gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)
# Áp dụng phép Canny để phát hiện biên
edges = cv2.Canny(gray, 20, 80)
cv2.imshow("mm",edges)
# Tìm các đường biên sau khi làm mịn
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
max_y = min_y = contours[0][0][0][1]
max_x = min_x = contours[0][0][0][0]

for contour in contours:
    for point in contour:
        x, y = point[0]
        max_x = max(max_x, x)
        min_x = min(min_x, x)
        max_y = max(max_y, y)
        min_y = min(min_y, y)

# Lấy phần nội dung bên trong hộp chữ nhật
roi_content = image_GauBlur[min_y:max_y, min_x:max_x]
hsv_image = cv2.cvtColor(roi_content, cv2.COLOR_BGR2HSV)
target_color_low = np.array([0, 0, 0])
target_color_high = np.array([180, 255, 60])
color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high)
# Lật vùng trắng và đen
color_mask = cv2.bitwise_not(color_mask)
WIDTH,HEIGHT = color_mask.shape[1],color_mask.shape[0]

# Tạo một hình chữ nhật chỉ định khu vực mực nước chuẩn.
X_ROI_WATER, Y_ROI_WATER = 0, int((0.202*HEIGHT))
size_x_ROI_WATER = WIDTH
size_y_ROI_WATER = int(0.04*HEIGHT)
ROI_WATER = color_mask[Y_ROI_WATER : Y_ROI_WATER + size_y_ROI_WATER,X_ROI_WATER:X_ROI_WATER + size_x_ROI_WATER]

# Tạo một hình chữ Nhật kiểm tra lượng nước vượt mức giới hạn
X_ROI_WATER_OUT, Y_ROI_WATER_OUT = 0,(Y_ROI_WATER - int(0.04*HEIGHT))
size_x_ROI_WATER_OUT = WIDTH
size_y_ROI_WATER_OUT = int(0.04*HEIGHT)
ROI_WATER_OUT = color_mask[Y_ROI_WATER_OUT : Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT,X_ROI_WATER_OUT:X_ROI_WATER_OUT + size_x_ROI_WATER_OUT]

if np.any(ROI_WATER_OUT != 255):
    CHECK.append("ERRORLABEL") 
# Kiểm tra xem có pixel 225 trong khu vực mực nước được chỉ định không, 
if np.any(ROI_WATER != 255):
    CHECK.append("GOOD")
else:
   CHECK.append("ERRORLABEL")

if "ERRORLABEL" in CHECK:
    cv2.putText(image,"Water: ERROR", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2 )
    cv2.imshow("Image_error_highlighted",image)
else:
    cv2.putText(image,"Water: GOOD", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2 )
    cv2.imshow("Org",image)
cv2.rectangle(color_mask,(X_ROI_WATER,Y_ROI_WATER),(X_ROI_WATER + size_x_ROI_WATER,Y_ROI_WATER + size_y_ROI_WATER), (0,0,255),2)
cv2.rectangle(color_mask,(X_ROI_WATER_OUT,Y_ROI_WATER_OUT),(X_ROI_WATER_OUT + size_x_ROI_WATER_OUT,Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT), (0,0,255),2)
cv2.imshow("color_mask",color_mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
