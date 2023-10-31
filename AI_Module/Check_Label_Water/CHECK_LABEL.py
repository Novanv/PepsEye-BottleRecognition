import cv2
import numpy as np

image_path = "image_data/l1.jpg"
image = cv2.imread(image_path)
image = image[60:420,120:520]

# Chuyển đổi ảnh sang không gian màu HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Xác định màu sắc chính của chai nước (ví dụ: màu xanh lá)
target_color_low = np.array([80, 80, 80])
target_color_high = np.array([120, 255, 255])

# Tạo mask cho màu sắc chính của chai nước lấy màu xanh từ ảnh HSV
color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high)

# Áp dụng mask để chỉ giữ lại phần của ảnh có màu sắc chính của chai nước
highlighted_image = cv2.bitwise_and(image, image, mask=color_mask)

# Chuyển sang ảnh có màu trắng và đen thôi
ret,image_thres = cv2.threshold(highlighted_image, 0, 255,cv2.THRESH_BINARY)
# Chuyển ảnh màu thành ảnh xám
gray_image = cv2.cvtColor(image_thres, cv2.COLOR_BGR2GRAY)

# Sử dụng cv2.countNonZero trên ảnh xám
white_pixel_count = cv2.countNonZero(gray_image)
if white_pixel_count < 500:
    # Chuyển tất cả pixel màu trắng thành đen
    image_thres = np.zeros_like(image_thres)
# Số pixel màu trắng
print("Số pixel màu trắng:", white_pixel_count)

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

