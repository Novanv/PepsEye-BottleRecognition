import cv2
import numpy as np
import matplotlib.pyplot as plt

def WATER_CHECK(image_path):
    # Tạo list để chứa các giá trị được thêm vào từ việc xử lí thông tin good hoặc error
    CHECK = []
    
    # Độc thông tin ảnh từ đường dẫn
    image = cv2.imread(image_path)
    
    # Chọn vùng để trị, giới hạn vùng để tránh ảnh hưởng của các đường biên, gây cho model phát hiện các cạnh bị sai
    
    img_roi = image[60:420,120:520]
    
    # Áp dụng Gaussian Blur
    image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 1)
    
    # Chuyển đổi ảnh sang ảnh grayscale
    gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)
    
    # Áp dụng phép Canny để phát hiện cạnh
    edges = cv2.Canny(gray, 20, 80)
    
    # Tìm các đường biên sau khi làm mịn
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên để thực hiện chức năng object detector đối tượng
    # trên một background trắng, tăng tính nổi bậc cho đối tượng - chai nước pepsi
    max_y = min_y = contours[0][0][0][1]
    max_x = min_x = contours[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour in contours:
        for point in contour: # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x', 'min_x', 'max_y', và 'min_y'
            min_x = min(min_x, x)   # Cập nhật giá trị tối đa và tối thiểu. 
            max_y = max(max_y, y)   # Khi có một điểm ảnh có tọa độ x hoặc y lớn hơn tối đa hoặc nhỏ hơn tối thiểu hiện tại, cập nhật giá trị tương ứng.
            min_y = min(min_y, y)   # Mục đích của việc này là lấy ra 4 tọa độ hình chữ nhật bao sát hết chai nước (bounding box)


    # Sau khi có được 4 tọa độ bao sát hết chai nước (bounding box), cắt ra hình chữ nhật theo 4 tọa độ
    roi_content = image_GauBlur[min_y:max_y, min_x:max_x]   # Gán hình ảnh cắt ra theo 4 tọa độ cho biến 'roi_content'
    # --->> Lấy được box của đối tượng.
    
    # Thực hiện region split, theo ngưỡng màu đen. Vì đặt điểm nước của chai peepsi có màu đen, khác biệt hoàn toàn với các đối tượng khác
    # Thực hiện region split theo màu "Đen" là cách tối ưu nhất để lấy chính xác vùng nước.
    hsv_image = cv2.cvtColor(roi_content, cv2.COLOR_BGR2HSV)
    target_color_low = np.array([0, 0, 0]) # Ngưỡng min của màu đen
    target_color_high = np.array([180, 255, 30])    # Ngưỡng max của màu đen
    color_mask = cv2.inRange(hsv_image, target_color_low, target_color_high) # Thực hiện phân vùng theo màu đen
    # -->>> Lấy được chính xác vừng có nuóc
    
    # Lật vùng nước sang 2 màu trắng và đen": Trong đó đen mà nơi có vùng nước, trắng là các đối tượng khác
    # Bây giờ trong ảnh chỉ còn tồn tại 2 màu đen và trắng và biết chính xác nước đang ở đâu
    color_mask = cv2.bitwise_not(color_mask)
    # Lấy kích thước của box 
    WIDTH,HEIGHT = color_mask.shape[1],color_mask.shape[0] # Chiều rộng, chiều dài

    # Tạo một hình chữ nhật chỉ định khu vực mực nước chuẩn. 
    X_ROI_WATER, Y_ROI_WATER = 0, int((0.202*HEIGHT))   # Đặt vị trí (x,y) góc trái trên cùng của hình chữ nhật 
    size_x_ROI_WATER = WIDTH                            # Chiều rộng của vùng kiểm tra mực nước
    size_y_ROI_WATER = int(0.04*HEIGHT)                 # Chiều cao của của vùng kiểm tra mực nước
    ROI_WATER = color_mask[Y_ROI_WATER : Y_ROI_WATER + size_y_ROI_WATER,X_ROI_WATER:X_ROI_WATER + size_x_ROI_WATER] # Thiết lập vùng kiểm tra mực nước

    # Tạo một hình chữ Nhật kiểm tra lượng nước vượt mức giới hạn nếu kiểm tra trong vùng CHUẨN đạt thì phải kiểm tra nước có bị quá mức hay không
    # Vùng này nằm trên vùng "Chuẩn"
    # Nếu không vượt quá thì sẽ đạt # Ngược lại sẽ lỗi 
    X_ROI_WATER_OUT, Y_ROI_WATER_OUT = 0,(Y_ROI_WATER - int(0.04*HEIGHT))   # Đặt vị trí (x,y) góc trái trên cùng của hình chữ nhật 
    size_x_ROI_WATER_OUT = WIDTH                                            # Chiều rộng của vùng kiểm tra mực nước
    size_y_ROI_WATER_OUT = int(0.04*HEIGHT)                                 # Chiều cao của của vùng kiểm tra mực nước
    ROI_WATER_OUT = color_mask[Y_ROI_WATER_OUT : Y_ROI_WATER_OUT + size_y_ROI_WATER_OUT,X_ROI_WATER_OUT:X_ROI_WATER_OUT + size_x_ROI_WATER_OUT] # # Thiết lập vùng kiểm tra mực nước

    if np.any(ROI_WATER_OUT != 255):
        CHECK.append("ERROR") 
    # Kiểm tra xem có pixel 225 trong khu vực mực nước được chỉ định không, 
    if np.any(ROI_WATER != 255):
        CHECK.append("GOOD")
    else:
        CHECK.append("ERROR")

    #-----------------------------------------------------------------------------------------------------------------------------------------------/
    # Cuối cùng, check xem thử trong danh sách 'CHECK' có nhãn lỗi ("ERROR") hay không
    
    # Tạo một danh sách để tổng kết xem mực nước có lỗi hay không = > danh sách này sẽ chỉ chứa [0] hoặc [1]
    WATER_CHECK = []
    
    if "ERROR" in CHECK:
        WATER_CHECK.append(1) # Theo quy ước: 1 -> Lỗi
    else:
        WATER_CHECK.append(0) # 0 -> tốt

    # Kết thúc hàm, trả về danh sách 'WATER_CHECK'
    return WATER_CHECK

image_path = "image_data/g7.jpg"
print(WATER_CHECK(image_path))