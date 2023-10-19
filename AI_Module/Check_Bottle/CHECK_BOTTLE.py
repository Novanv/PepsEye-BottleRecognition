import cv2
import numpy as np
import matplotlib.pyplot as plt

CHECK = []

# Đọc ảnh từ đường dẫn
img = cv2.imread("image_product/l3.jpg")
img = cv2.resize(img, (500, 500))

# Cắt phần quan tâm của ảnh
img_roi = img[0:500, 100:400]

# Áp dụng Gaussian Blur
image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 1)
# Chuyển đổi ảnh sang ảnh grayscale
gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)
# Áp dụng phép Canny để phát hiện biên
edges = cv2.Canny(gray, 30, 90)
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
roi_content = img_roi[min_y:max_y, min_x:max_x]
print("Height: ",roi_content.shape[0])
if 410 < roi_content.shape[0] < 430:
    CHECK.append("GOOD")
else:
    CHECK.append("ERROR")
roi_1 = roi_content[70:150, 0:max_x]
roi_2 = roi_content[170:300, 0:max_x]
roi_3 = roi_content[310:400, 0:max_x]

# Áp dụng Gaussian Blur
image_GauBlur_roi1 = cv2.GaussianBlur(roi_1, (3, 3), 1)
# Chuyển đổi ảnh sang ảnh grayscale
gray_roi1 = cv2.cvtColor(image_GauBlur_roi1, cv2.COLOR_BGR2GRAY)
# Áp dụng phép Canny để phát hiện biên
edges_roi1 = cv2.Canny(gray_roi1, 30, 90)
contours_1,_ = cv2.findContours(edges_roi1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_y = min_y = contours_1[0][0][0][1]
max_x = min_x = contours_1[0][0][0][0]
for contour_1 in contours_1:
    for point in contour_1:
        x, y = point[0]
        max_x = max(max_x, x) 
print(max_x)        
if 150 < max_x < 170:
    CHECK.append("GOOD")
else: 
    CHECK.append("ERROR")

# Áp dụng Gaussian Blur
image_GauBlur_roi2 = cv2.GaussianBlur(roi_2, (3, 3), 1)
# Chuyển đổi ảnh sang ảnh grayscale
gray_roi2= cv2.cvtColor(image_GauBlur_roi2, cv2.COLOR_BGR2GRAY)
# Áp dụng phép Canny để phát hiện biên
edges_roi2 = cv2.Canny(gray_roi2, 30, 90)
contours_2,_ = cv2.findContours(edges_roi2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_y = min_y = contours_2[0][0][0][1]
max_x = min_x = contours_2[0][0][0][0]
for contour_2 in contours_2:
    for point in contour_2:
        x, y = point[0]
        max_x = max(max_x, x) 
print(max_x)        
if 145 < max_x < 160:
    CHECK.append("GOOD")
else: 
    CHECK.append("ERROR")

# Áp dụng Gaussian Blur
image_GauBlur_roi3 = cv2.GaussianBlur(roi_3, (3, 3), 1)
# Chuyển đổi ảnh sang ảnh grayscale
gray_roi3 = cv2.cvtColor(image_GauBlur_roi3, cv2.COLOR_BGR2GRAY)
# Áp dụng phép Canny để phát hiện biên
edges_roi3 = cv2.Canny(gray_roi3, 30, 90)
contours_3,_ = cv2.findContours(edges_roi3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
max_y = min_y = contours_3[0][0][0][1]
max_x = min_x = contours_3[0][0][0][0]
for contour_3 in contours_3:
    for point in contour_3:
        x, y = point[0]
        max_x = max(max_x, x)            
print(max_x) 
if 150 < max_x < 170:
    CHECK.append("GOOD")
else: 
    CHECK.append("ERROR")


if "ERROR" in CHECK:
    cv2.putText(img,"Bottle: ERROR",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    cv2.imshow("img",img)
else:
    cv2.putText(img,"Bottle: GOOD",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("img",img)

cv2.imshow('ROI Contentrr', roi_content)
cv2.imshow('ROI Contentm', edges_roi1 )
cv2.imshow('ROI Contentb', edges_roi2 )
cv2.imshow('ROI Contentv', edges_roi3 )
cv2.imshow('ROI Contentv  ', edges )
cv2.waitKey(0)
cv2.destroyAllWindows()

