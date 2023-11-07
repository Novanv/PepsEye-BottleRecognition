from lib import *

#--------------------------------------------------------------        AI MODULE        ---------------------------------------------------------

def CHECK_EXIST(img):
    # Đây là hàm BOTTLE_EXIST có mục đích là kiểm tra xem có tồn tại đối tượng trong khung của camera hay không
    # Tham số đầu vào sẽ là đường dẫn của 1 ảnh 'image_path'
    # Tham số đầu ra sẽ 1 list với 1 phần tử duy nhất là '["EXIST"]' hoặc '["NOEXIST"]'
    # '["EXIST"]' có nghĩa là có tồn tại đối tượng để kiểm tra, '["NOEXIST"]' là có nghĩa là không tồn tại đối tượng để kiểm tra
    #------------------------------------------------------------------------------------#

    # Cắt phần quan tâm của ảnh để loại bỏ các thành phần không liên quan trong ảnh và gán cho biến 'img_roi'
    img_roi = img[60:420, 120:520]

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 4 (mức độ mịn)
    image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 4)    # Sau đó gán cho biến 'image_GauBlur'

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)  # Gán ảnh ở grayscale cho biến 'gray'

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges = cv2.Canny(gray, 20, 80)     # Gán ảnh phát hiện ra cạnh của chai nước cho biến 'edges'

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # Gán danh sách đường viền cho biến 'contours', ở đây mỗi đường viền là một danh sách các điểm
    if contours == ():
        return ["NOEXIST"]
    else: 
        return ["EXIST"]


# Hàm check bottle = > return [0] = Good hoặc [1] = Error -------------------------------/
def BOTTLE_CHECK(img):
# Đây là hàm BOTTLE_CHECK có mục đích là kiểm tra xem vỏ chai có lỗi hay không
# Tham số đầu vào sẽ là đường dẫn của 1 ảnh 'image_path'
# Tham số đầu ra sẽ 1 list với 1 phần tử duy nhất là '[0]' hoặc '[1]'
# '[0]' có nghĩa là vỏ chai không có lỗi, '[1]' là có lỗi
#------------------------------------------------------------------------------------#

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    # img = cv2.imread(image_path)

    # Cắt phần quan tâm của ảnh để loại bỏ các thành phần không liên quan trong ảnh và gán cho biến 'img_roi'
    img_roi = img[60:420, 120:520]

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 4 (mức độ mịn)
    image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 4)    # Sau đó gán cho biến 'image_GauBlur'

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)  # Gán ảnh ở grayscale cho biến 'gray'

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges = cv2.Canny(gray, 20, 80)     # Gán ảnh phát hiện ra cạnh của chai nước cho biến 'edges'

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   # Gán danh sách đường viền cho biến 'contours', ở đây mỗi đường viền là một danh sách các điểm

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Bước đầu tiên: Check chiều cao của chai nước

    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours[0][0][0][1]
    max_x = min_x = contours[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour in contours:
        for point in contour:       # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x', 'min_x', 'max_y', và 'min_y'
            min_x = min(min_x, x)   # Cập nhật giá trị tối đa và tối thiểu. 
            max_y = max(max_y, y)   # Khi có một điểm ảnh có tọa độ x hoặc y lớn hơn tối đa hoặc nhỏ hơn tối thiểu hiện tại, cập nhật giá trị tương ứng.
            min_y = min(min_y, y)   # Mục đích của việc này là lấy ra 4 tọa độ hình chữ nhật bao sát hết chai nước (bounding box)

   # Sau khi có được 4 tọa độ bao sát hết chai nước (bounding box), cắt ra hình chữ nhật theo 4 tọa độ
    roi_content = img_roi[min_y:max_y, min_x:max_x] # Gán hình ảnh cắt ra theo 4 tọa độ cho biến 'roi_content'

    # Sau khi có được hình chữ nhật bao sát toàn bộ chai nước, ta có được chiều cao của chai nước tính bằng pixel, ở đây là 'roi_content.shape[0]'
    # Gán lại chiều cao chai nước chi biến 'height'
    height = roi_content.shape[0]

    #-----------------------------------------------------------------------------------------
    # Sau khi có được chiều cao, bước tiếp theo là lấy ra các chiều rộng của thân chai
    # Ở đây lấy ra chiều rộng ở 6 vị trí của thân chai
    # Các vị trí đều lấy theo tỉ lệ so với chiều cao

    # Phần thân trên lấy 2 vị trí, lần lượt mỗi vị trí sẽ lấy hai tham số là 'x' trong cột 'Oxy'
    roi_1_x1 = int(height*0.127)
    roi_1_x2 = int(height*0.175)

    roi_2_x1 = int(height*0.222)
    roi_2_x2 = int(height*0.286)
    
    # Phần thân giữa lấy 2 vị trí, lần lượt mỗi vị trí sẽ lấy hai tham số là 'x' trong cột 'Oxy'
    roi_3_x1 = int(height*0.398)
    roi_3_x2 = int(height*0.445)

    roi_4_x1 = int(height*0.589)
    roi_4_x2 = int(height*0.636)

    # Phần thân dưới lấy 2 vị trí, lần lượt mỗi vị trí sẽ lấy hai tham số là 'x' trong cột 'Oxy' 
    roi_5_x1 = int(height*0.668)
    roi_5_x2 = int(height*0.716)

    roi_6_x1 = int(height*0.764)
    roi_6_x2 = int(height*0.828)

    # Sau khi có được khoảng từ 'x_1' đến 'x_2' cho mỗi khoảng vị trí, ta cắt hình ảnh chai nước ra thành 6 phần tương ứng 
    roi_1 = roi_content[roi_1_x1:roi_1_x2, 0:max_x]
    roi_2 = roi_content[roi_2_x1:roi_2_x2, 0:max_x]
    roi_3 = roi_content[roi_3_x1:roi_3_x2, 0:max_x]
    roi_4 = roi_content[roi_4_x1:roi_4_x2, 0:max_x]
    roi_5 = roi_content[roi_5_x1:roi_5_x2, 0:max_x]
    roi_6 = roi_content[roi_6_x1:roi_6_x2, 0:max_x]

    # Sau khi cắt được 6 phần ra từ ảnh, ta bắt đầu lấy ra chiều rộng cho mỗi phần.
    #-------------------------------------------------------------------------
    # Roi 1

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi1 = cv2.GaussianBlur(roi_1, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi1 = cv2.cvtColor(image_GauBlur_roi1, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 5 và ngưỡng trên là 30
    edges_roi1 = cv2.Canny(gray_roi1, 5, 30)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours_1,_ = cv2.findContours(edges_roi1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Gán danh sách đường viền cho biến 'contours_1', ở đây mỗi đường viền là một danh sách các điểm
    
    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_1[0][0][0][1]
    max_x = min_x = contours_1[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_1. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_1 in contours_1:
        for point in contour_1: # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x) # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng thân trên 1 cho biến 'wide_1'
    wide_1 = max_x
    
    #---------------------------------------------------------------------------------------
    # Roi_2

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi2 = cv2.GaussianBlur(roi_2, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi2= cv2.cvtColor(image_GauBlur_roi2, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 5 và ngưỡng trên là 30
    edges_roi2 = cv2.Canny(gray_roi2, 5, 30)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours_2,_ = cv2.findContours(edges_roi2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Gán danh sách đường viền cho biến 'contours_2', ở đây mỗi đường viền là một danh sách các điểm
    
    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_2[0][0][0][1]
    max_x = min_x = contours_2[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_2. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_2 in contours_2:
        for point in contour_2:     # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng thân trên 2 cho biến 'wide_2'
    wide_2 = max_x     
    
    #---------------------------------------------------------------------------------------
    # Roi_3

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi3 = cv2.GaussianBlur(roi_3, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi3 = cv2.cvtColor(image_GauBlur_roi3, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 50 và ngưỡng trên là 30
    edges_roi3 = cv2.Canny(gray_roi3, 5, 30)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours_3,_ = cv2.findContours(edges_roi3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Gán danh sách đường viền cho biến 'contours_3', ở đây mỗi đường viền là một danh sách các điểm
   
    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_3[0][0][0][1]
    max_x = min_x = contours_3[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_3. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_3 in contours_3:
        for point in contour_3:     # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng giữa 1 trên cho biến 'wide_3'
    wide_3 = max_x           
    
    #---------------------------------------------------------------------------------------
    # Roi_4

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi4 = cv2.GaussianBlur(roi_4, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi4 = cv2.cvtColor(image_GauBlur_roi4, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 5 và ngưỡng trên là 30
    edges_roi4 = cv2.Canny(gray_roi4, 5, 30)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours_4,_ = cv2.findContours(edges_roi4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # Gán danh sách đường viền cho biến 'contours_4', ở đây mỗi đường viền là một danh sách các điểm
    
    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_4[0][0][0][1]
    max_x = min_x = contours_4[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_4. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_4 in contours_4:
        for point in contour_4:     # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng giữa 2 trên cho biến 'wide_4'
    wide_4 = max_x           
    
    #---------------------------------------------------------------------------------------
    # Roi_5

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi5 = cv2.GaussianBlur(roi_5, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi5 = cv2.cvtColor(image_GauBlur_roi5, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 5 và ngưỡng trên là 30
    edges_roi5 = cv2.Canny(gray_roi5, 5, 30)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours_5,_ = cv2.findContours(edges_roi5, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    # Gán danh sách đường viền cho biến 'contours_5', ở đây mỗi đường viền là một danh sách các điểm 

    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_5[0][0][0][1]
    max_x = min_x = contours_5[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_5. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_5 in contours_5:
        for point in contour_5:     # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng giữa 2 trên cho biến 'wide_5'
    wide_5 = max_x           
    
    #---------------------------------------------------------------------------------------
    # Roi_6

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi6 = cv2.GaussianBlur(roi_6, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi6 = cv2.cvtColor(image_GauBlur_roi6, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 5 và ngưỡng trên là 30
    edges_roi6 = cv2.Canny(gray_roi6, 5, 30)

    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    contours_6,_ = cv2.findContours(edges_roi6, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên
    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_6[0][0][0][1]
    max_x = min_x = contours_6[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours_6. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_6 in contours_6:
        for point in contour_6:     # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    # Gán lại chiều rộng giữa 2 trên cho biến 'wide_6'
    wide_6 = max_x           
    
    #----------------------------------------------------------------------------------------
    # Sau khi tính toán được chiều cao và các chiều rộng của vỏ chai, ta xét các tỉ lệ
    # Tạo một danh sách để check xem từng tỉ lệ cho chiều rộng và chiều cao của vỏ chai
    CHECK = []

    # Xet chieu rong roi_1 vs roi_2
    if 0.83 <= (wide_1 / wide_2) <= 1 : 
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_3 vs roi_4
    if 0.95 <= (wide_3 / wide_4) <= 1.05:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_5 vs roi_6
    if 0.9 <= (wide_5 / wide_6) <= 1:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_2 vs roi_3
    if 0.9 <= (wide_3 / wide_2) <= 0.98:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_2 vs roi_6
    if 0.95 <= (wide_2 / wide_6) <= 1.05:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_3 vs roi_6
    if 0.9 <= (wide_3 / wide_6) <= 0.98:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu cao 
    if 2.9 <= (height / wide_2) <= 3.7:
        CHECK.append(0)
    else:
        CHECK.append(1)

    if 3.1 <= (height / wide_4) <= 4:
        CHECK.append(0)
    else:
        CHECK.append(1)

    if 2.9 <= (height / wide_2) <= 3.7:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Nếu có bất kì lỗi nào của tỉ lệ, cho rằng đó là sản phẩm lỗi
    BOTTLE_CHECK = []
    if 1 in CHECK :
        BOTTLE_CHECK.append(1)
    else:
        BOTTLE_CHECK.append(0)

    # Trả về danh sách BOTTLE_CHECK
    return BOTTLE_CHECK




# Hàm check Label = > return [0] = Good hoặc [1] = Error -------------------------------/
def LABEL_CHECK(image):
    # Tạo một danh sách để check xem vỏ chai có lỗi không
    CHECK = []

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    # image = cv2.imread(image_path)

    #Crop ảnh với tỉ lệ như dưới:
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

    # Chuyển sang ảnh có màu trắng và đen
    ret, image_thres = cv2.threshold(highlighted_image, 0, 255, cv2.THRESH_BINARY)

    # Chuyển ảnh màu thành ảnh xám
    gray_image = cv2.cvtColor(image_thres, cv2.COLOR_BGR2GRAY)
    
    # Sử dụng cv2.countNonZero trên ảnh xám
    white_pixel_count = cv2.countNonZero(gray_image)
    if white_pixel_count < 1200: #Check màu pixel < 1200 (nhỏ hơn 1200)
        # Chuyển tất cả pixel màu trắng thành đen
        image_thres = np.zeros_like(image_thres)

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


# Hàm check water level = > return [0] = Good hoặc [1] = Error-------------------------------/
def WATER_CHECK(image):
    # Tạo list để chứa các giá trị được thêm vào từ việc xử lí thông tin good hoặc error
    CHECK = []
    
    # Độc thông tin ảnh từ đường dẫn
    # image = cv2.imread(image_path)
    
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
    target_color_high = np.array([180, 255, 80])    # Ngưỡng max của màu đen
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


def MODULE_CHECK(image_path):
    # Đây là hàm thực thi các AI module
    # CHECK là một list nhận các giá trị [0,1,2,3] 
    # + Thực hiện kiểm tra Các biến trên để đưa lại kết quả cho CHECK để dẫn đến kết luận cuối cùng.
    
    image = cv2.imread(image_path)
    CHECK = []
    EXIST_OBJ = CHECK_EXIST(image) 
    
    if EXIST_OBJ[0] == "NOEXIST": # Kiểm tra biến tồn tại 
        return ["NOEXIST"]
    else:
        # Biến check bottle = List giá trị trả về từ hàm Check bottle (image_path)
        BOTTLE_CHECK_ = BOTTLE_CHECK(image) # Lấy kết quả từ hàm kiểm tra vỏ chai 
        if 1 in BOTTLE_CHECK_:                   # Nếu kết quả kiểm tra vỏ chai là lỗi, thêm giá trị 1 vào danh sách 'CHECK'
            CHECK.append(1)
        else:                                   # Nếu kết quả kiểm tra vỏ chai là tốt, thêm giá trị 0 vào danh sách 'CHECK'
            CHECK.append(0)       


        # Biến check Label = List giá trị trả về từ hàm Check Label (image_path)
        LABEL_CHECK_ = LABEL_CHECK(image) # Lấy kết quả từ hàm kiểm tra vỏ chai 
        if 1 in LABEL_CHECK_:                   # Nếu kết quả kiểm tra vỏ chai là lỗi, thêm giá trị 1 vào danh sách 'CHECK'
            CHECK.append(2)
        else:                                   # Nếu kết quả kiểm tra vỏ chai là tốt, thêm giá trị 0 vào danh sách 'CHECK'
            CHECK.append(0)

            
        # Biến check water level = List giá trị trả về từ hàm Check water level (image_path)
        WATER_CHECK_ = WATER_CHECK(image) # Lấy kết quả từ hàm kiểm tra  
        if 1 in WATER_CHECK_:                   # Nếu kết quả kiểm tra water level là lỗi, thêm giá trị 2 vào danh sách 'CHECK'
            CHECK.append(3)
        else:                                   # Nếu kết quả kiểm tra water level là tốt, thêm giá trị 0 vào danh sách 'CHECK'
            CHECK.append(0)

        return CHECK

# #-----------------------------------------------------------------------------------------------------------------------------------------------