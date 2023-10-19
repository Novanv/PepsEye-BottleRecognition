import cv2
import numpy as np

SIZE = (500, 500)
# Đọc hình ảnh chai nước
image_path = "D:\A.I\PROJECT\Check_water\Group_3\image_product\good.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image, SIZE)

# Đọc hình ảnh đối tượng
object_image_path = "D:\A.I\PROJECT\Check_water\Group_3\image_product\pessi(black_color).jpg"
object_image = cv2.imread(object_image_path)
object_image = cv2.resize(object_image, SIZE)

#Chuyển ảnh về ảnh xám
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
object_image_gray = cv2.cvtColor(object_image, cv2.COLOR_BGR2GRAY)

# Sử dụng phát hiện cạnh Canny
imgae_edges = cv2.Canny(image_gray, threshold1=30, threshold2=100)
object_image_edges = cv2.Canny(object_image_gray, threshold1=30, threshold2=100)

# Sử dụng phương pháp tìm kiếm hình ảnh
result = cv2.matchTemplate(imgae_edges, object_image_edges, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)



# Thiết lập ngưỡng để xác định ngưỡng cho sự khớp
threshold = 0.8  # Giá trị ngưỡng dựa trên kết quả tìm kiếm hình ảnh

# Tìm vị trí của sự khớp
locations = np.where(result >= threshold)
for pt in zip(*locations[::-1]):
    # Vẽ một hộp xung quanh nhãn dán trên hình ảnh gốc
    cv2.rectangle(image, pt, (pt[0] + object_image.shape[1], pt[1] + object_image.shape[0]), (0, 255, 0), 2)
# Tọa độ và kích thước của vùng ROI_LABEL
X_ROI_LABEL, Y_ROI_LABEL = 170, 250
size_x_ROI_LABEL = 150
size_y_ROI_LABEL = 150
# Vẽ hộp xung quanh ROI_LABEL trên hình ảnh gốc
cv2.rectangle(image, (X_ROI_LABEL, Y_ROI_LABEL), (X_ROI_LABEL + size_x_ROI_LABEL, Y_ROI_LABEL + size_y_ROI_LABEL), (255, 0, 0), 2)
# Kiểm tra xem có sự khớp nào hay không
if locations[0].size > 0:
    print("Label: Good")
    cv2.putText(object_image, "Label: GOOD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.rectangle(object_image, (X_ROI_LABEL, Y_ROI_LABEL), (X_ROI_LABEL + size_x_ROI_LABEL, Y_ROI_LABEL + size_y_ROI_LABEL), (255, 0, 0), 2)
    cv2.imshow("Org",object_image)

else:
    print("Label: Error")
    cv2.putText(object_image, "Label: Error", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.rectangle(object_image, (X_ROI_LABEL, Y_ROI_LABEL),(X_ROI_LABEL + size_x_ROI_LABEL, Y_ROI_LABEL + size_y_ROI_LABEL), (0, 0, 255), 2)
    cv2.imshow("Image_error_highlighted",object_image)

# Hiển thị hình ảnh với hộp xung quanh nhãn dán (nếu có)
cv2.rectangle(imgae_edges,(X_ROI_LABEL,Y_ROI_LABEL),(X_ROI_LABEL + size_x_ROI_LABEL,Y_ROI_LABEL + size_y_ROI_LABEL), (0,0,255), 2)
cv2.imshow("ThresHold",imgae_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
