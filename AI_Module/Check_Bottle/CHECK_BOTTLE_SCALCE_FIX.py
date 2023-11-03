def BOTTLE_CHECK(image_path):
# Đây là hàm BOTTLE_CHECK có mục đích là kiểm tra xem vỏ chai có lỗi hay không
# Tham số đầu vào sẽ là đường dẫn của 1 ảnh 'image_path'
# Tham số đầu ra sẽ 1 list với 1 phần tử duy nhất là '[0]' hoặc '[1]'
# '[0]' có nghĩa là vỏ chai không có lỗi, '[1]' là có lỗi
#------------------------------------------------------------------------------------#

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    img = cv2.imread(image_path)

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