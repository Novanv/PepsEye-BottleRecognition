import cv2
import numpy as np

image_path = "D:\A.I\PROJECT\Check_water\Group_3\image_product\good.jpg"
image = cv2.imread(image_path)
image = cv2.resize(image,(500,500))

# Chuyển đổi ảnh sang không gian màu HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Xác định màu sắc chính của chai nước (ví dụ: màu xanh lá)
target_color_low = np.array([100, 80, 80])
target_color_high = np.array([120, 255, 255])

# Tạo mask cho màu sắc chính của chai nước lấy màu xanh từ ảnh HSV
color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high)

# Áp dụng mask để chỉ giữ lại phần của ảnh có màu sắc chính của chai nước
highlighted_image = cv2.bitwise_and(image, image, mask=color_mask)

# Chuyển sang ảnh có màu trắng và đen thôi
ret,image_thres = cv2.threshold(highlighted_image, 0, 255,cv2.THRESH_BINARY)

has_label = np.any(image_thres == 255)
if has_label:
    cv2.putText(image,"Label: GOOD", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2 )
    cv2.imshow("image",image)
    cv2.imshow("image1",image_thres)
    cv2.imshow("image2",highlighted_image)
else:
    cv2.putText(image,"Label: Error", (50, 50) ,cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2 )
    cv2.imshow("image",image)
    cv2.imshow("image1",image_thres)
    cv2.imshow("image2",highlighted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

