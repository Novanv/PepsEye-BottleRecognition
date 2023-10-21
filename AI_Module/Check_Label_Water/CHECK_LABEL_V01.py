import cv2
import numpy as np
def CHECK_LABEL(image_path):
    # Tạo một danh sách để check xem vỏ chai có lỗi không
    CHECK = []

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    image = cv2.imread(image_path)

    # chuyển size ảnh về dạng 500 x 500
    image = cv2.resize(image, (500, 500))

    # Chuyển đổi ảnh sang không gian màu HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Xác định màu sắc chính của chai nước (ví dụ: màu xanh lá)
    target_color_low = np.array([100, 80, 80])
    target_color_high = np.array([120, 255, 255])

    # Tạo mask cho màu sắc chính của chai nước lấy màu xanh từ ảnh HSV
    color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high)

    # Áp dụng mask để chỉ giữ lại phần của ảnh có màu sắc chính của chai nước
    highlighted_image = cv2.bitwise_and(image, image, mask=color_mask)

    # Chuyển sang ảnh có màu trắng và đen
    ret, image_thres = cv2.threshold(highlighted_image, 0, 255, cv2.THRESH_BINARY)

    # Gán biến "has_label" để check có nhãn hay không
    has_label = np.any(image_thres == 255)

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Tạo một danh sách để tổng kết xem nhãn nước có lỗi hay không
    CHECK_LABEL = []

    # Cuối cùng, check xem thử trong danh sách 'CHECK' có nhãn lỗi ("ERROR") hay không
    if not has_label:
        CHECK.append("ERROR")


    # Nếu có nhãn lỗi ("ERROR") trong danh sách 'CHECK'
    if "ERROR" in CHECK:
        CHECK_LABEL.append(1)  # Thêm nhãn '1' vào danh sách 'CHECK_LABEL'
    # Nếu không có nhãn lỗi ("ERROR") trong danh sách 'CHECK'
    else:
        CHECK_LABEL.append(0)  # Thêm nhãn '0' vào danh sách 'CHECK_LABEL'

    # Kết thúc hàm, trả về danh sách 'CHECK_LABEL'
    return CHECK_LABEL
