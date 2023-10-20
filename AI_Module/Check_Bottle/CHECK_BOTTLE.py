
def BOTTLE_CHECK(image_path):
    # Tạo một danh sách để check xem vỏ chai có lỗi không
    CHECK = []

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    img = cv2.imread(image_path)

    # chuyển size ảnh về dạng 500 x 500 
    img = cv2.resize(img, (500, 500))

    # Cắt phần quan tâm của ảnh (cắt bớt 100 pixel ở hai bên trái phải) và gán cho biến 'img_roi'
    img_roi = img[0:500, 100:400]


    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 1)    # Sau đó gán cho biến 'image_GauBlur'

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)  # Gán ảnh ở grayscale cho biến 'gray'

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 30 và ngưỡng trên là 90
    edges = cv2.Canny(gray, 30, 90)     # Gán ảnh phát hiện ra cạnh của chai nước cho biến 'edges'

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _  
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Gán danh sách đường viền cho biến 'contours', ở đây mỗi đường viền là một danh sách các điểm


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
    #print("Height: ",roi_content.shape[0])
    # Ta đặt ngưỡng cho chiều cao chai nước, nếu chiều cao nằm ngoài ngưỡng, ta thêm nhãn lỗi ("ERROR") vào danh sách 'CHECK'
    if 410 < roi_content.shape[0] < 430:    # Cụ thể ở đây, ngưỡng dưới là 410 pixel và ngưỡng trên là 430 pixel cho chiều cao.
        CHECK.append("GOOD")                # Thêm nhãn tốt ("GOOD") nếu chiều cao của chai nằm trong ngưỡng cho phép.
    else:
        CHECK.append("ERROR")               # Thêm nhãn lỗi ("ERROR") nếu chiều cao của chai nằm ngoài ngưỡng cho phép.


    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Bước thứ hai: Check chiều rộng của chai nước
    # Ở đây, chúng ta check chiều rộng ở 3 phần thân trên, giữa, dưới của chai nước

    # Chia ảnh bao sát chai nước làm 3 phần
    roi_1 = roi_content[70:150, 0:max_x]    # Cắt từ 70 pixel đến 150 pixel theo chiều cao của ảnh (Oy), chiều rộng giữ nguyên và gán cho biến 'roi_1'
    roi_2 = roi_content[170:300, 0:max_x]   # Cắt từ 170 pixel đến 300 pixel theo chiều cao của ảnh (Oy), chiều rộng giữ nguyên và gán cho biến 'roi_2'
    roi_3 = roi_content[310:400, 0:max_x]   # Cắt từ 310 pixel đến 400 pixel theo chiều cao của ảnh (Oy), chiều rộng giữ nguyên và gán cho biến 'roi_3'
    # Vậy, ta có được 3 ảnh của 3 phần thân trên, giữa, dưới của chai nước


    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    # Check chiều rộng phần thân trên:

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi1 = cv2.GaussianBlur(roi_1, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi1 = cv2.cvtColor(image_GauBlur_roi1, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 30 và ngưỡng trên là 90
    edges_roi1 = cv2.Canny(gray_roi1, 30, 90)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _ 
    contours_1,_ = cv2.findContours(edges_roi1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Gán danh sách đường viền cho biến 'contours_1, ở đây mỗi đường viền là một danh sách các điểm

    # Tìm đường viền cao nhất, thấp nhất, và vị trí rộng nhất 2 bên

    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_1[0][0][0][1]
    max_x = min_x = contours_1[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_1 in contours_1:
        for point in contour_1: # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x) # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    #print(max_x)
    # Đặt ngưỡng cho chiều rộng
    if 150 < max_x < 170:       # Cụ thể ở đây, ngưỡng dưới là 150 pixel và ngưỡng trên là 170 pixel
        CHECK.append("GOOD")    # Nếu chiều rộng nằm trong ngưỡng thì thêm nhãn tốt ("GOOD") vào trong danh sách 'CHECK'
    else: 
        CHECK.append("ERROR")   # Nếu chiều rộng nằm ngoài ngưỡng thì thêm nhãn lỗi ("ERROR") vào trong danh sách 'CHECK'


    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    # Check chiều rộng phần thân giữa:

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi2 = cv2.GaussianBlur(roi_2, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi2= cv2.cvtColor(image_GauBlur_roi2, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 30 và ngưỡng trên là 90
    edges_roi2 = cv2.Canny(gray_roi2, 30, 90)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _ 
    contours_2,_ = cv2.findContours(edges_roi2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Gán danh sách đường viền cho biến 'contours_2, ở đây mỗi đường viền là một danh sách các điểm

    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_2[0][0][0][1]
    max_x = min_x = contours_2[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_2 in contours_2:
        for point in contour_2: # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x) # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất 
    #print(max_x)

    # Đặt ngưỡng cho chiều rộng         
    if 145 < max_x < 160:   # Cụ thể ở đây, ngưỡng dưới là 145 pixel và ngưỡng trên là 160 pixel
        CHECK.append("GOOD")    # Nếu chiều rộng nằm trong ngưỡng thì thêm nhãn tốt ("GOOD") vào trong danh sách 'CHECK'
    else: 
        CHECK.append("ERROR")   # Nếu chiều rộng nằm ngoài ngưỡng thì thêm nhãn lỗi ("ERROR") vào trong danh sách 'CHECK'


    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
    # Check chiều rộng phần thân dưới:

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur_roi3 = cv2.GaussianBlur(roi_3, (3, 3), 1)

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray_roi3 = cv2.cvtColor(image_GauBlur_roi3, cv2.COLOR_BGR2GRAY)

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 30 và ngưỡng trên là 90
    edges_roi3 = cv2.Canny(gray_roi3, 30, 90)

    # Tìm các đường viền của vỏ chai từ ảnh phát hiện cạnh 'edges' bằng hàm 'cv2.findContours', trong đó:
    # 'cv2.RETR_EXTERNAL' là cờ chỉ định cách trích xuất các đường viền, chỉ trích xuất các đường viền bên ngoài (external contours) và không bao gồm các đường viền nằm bên trong chai nước 
    # 'cv2.CHAIN_APPROX_SIMPLE' là cách biểu diễn các đường viền bằng cách lưu trữ chỉ các đỉnh quan trọng của đường viền. Nó loại bỏ các đỉnh không cần thiết để tiết kiệm bộ nhớ
    # Ở đây, chúng ta không quan tâm đến giá trị thứ 2 mà hàm 'cv2.findContours trả về, tức số lỗ hoặc đối tượng con bên trong các đường viền chính nên sử dụng _ 
    contours_3,_ = cv2.findContours(edges_roi3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Gán danh sách đường viền cho biến 'contours_3, ở đây mỗi đường viền là một danh sách các điểm

    # Ban đầu, thiết lập max_x, min_x, max_y, và min_y bằng tọa độ của điểm ảnh đầu tiên trong đường viền đầu tiên
    max_y = min_y = contours_3[0][0][0][1]
    max_x = min_x = contours_3[0][0][0][0]

    # Duyệt qua toàn bộ danh sách contours. Với mỗi đường viền, duyệt qua toàn bộ danh sách các điểm ảnh trong đường viền đó
    for contour_3 in contours_3:
        for point in contour_3: # Với mỗi điểm ảnh point trong đường viền contour, lấy tọa độ x và y của điểm ảnh đó
            x, y = point[0]
            max_x = max(max_x, x)   # So sánh tọa độ x và y của mỗi điểm ảnh với 'max_x' và cập nhật nếu x lớn hơn, ở đây chỉ lấy ra chiều rộng lớn nhất             
    #print(max_x) 

    # Đặt ngưỡng cho chiều rộng  
    if 150 < max_x < 170:   # Cụ thể ở đây, ngưỡng dưới là 150 pixel và ngưỡng trên là 170 pixel
        CHECK.append("GOOD")    # Nếu chiều rộng nằm trong ngưỡng thì thêm nhãn tốt ("GOOD") vào trong danh sách 'CHECK'
    else: 
        CHECK.append("ERROR")   # Nếu chiều rộng nằm ngoài ngưỡng thì thêm nhãn lỗi ("ERROR") vào trong danh sách 'CHECK'


    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Cuối cùng, check xem thử trong danh sách 'CHECK' có nhãn lỗi ("ERROR") hay không

    # Tạo một danh sách để tổng kết xem vỏ chai có lỗi hay không
    BOTTLE_CHECK = []

    # Nếu có nhãn lỗi ("ERROR") trong danh sách 'CHECK'
    if "ERROR" in CHECK:
        BOTTLE_CHECK.append(1)  # Thêm nhãn '1' vào danh sách 'BOTTLE_CHECK'
    # Nếu không có nhãn lỗi ("ERROR") trong danh sách 'CHECK'
    else:                           
        BOTTLE_CHECK.append(0)  # Thêm nhãn '0' vào danh sách 'BOTTLE_CHECK'
    
    # Kết thúc hàm, trả về danh sách 'BOTTLE_CHECK'
    return BOTTLE_CHECK