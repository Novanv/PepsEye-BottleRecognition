
def BOTTLE_CHECK(image_path):

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
    # Gán lại chiều cao chai nước chi biến 'height'
    height = roi_content.shape[0]


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
    # Gán lại chiều rộng thân trên cho biến 'width_1'
    width_1 = max_x
    

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
    # Gán lại chiều rộng thân giữa cho biến 'width_2'
    width_2 = max_x


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
    # Gán lại chiều rộng thân dưới cho biến width_3 
    width_3 = max_x

    

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Cuối cùng, check xem thử tỉ lệ chai nước có lỗi hay không.
    # Tạo một danh sách để tổng kết xem vỏ chai có lỗi hay không
    BOTTLE_CHECK = []

    # Tạo một danh sách để check xem từng tỉ lệ cho chiều rộng và chiều cao của vỏ chai.
    CHECK = []

    # Xét tỉ lệ chiều rộng thân trên với thân giữa
    if (width_1 / width_2) > 1: # Thân trên luôn luôn lớn hơn thân giữa
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xét tỉ lệ chiều rộng thân trên với thân dưới
    if 0.98 <(width_1 / width_3) < 1.02:    # Thân trên và thân dưới có tỉ lệ chiều rộng xấp xỉ bằng 1
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xét tỉ lệ chiều cao với chiều rộng 
    if 2.63 < (height / width_1) < 2.67:    # Tỉ lệ xấp xỉ của chiều cao và chiều rộng thân trên 
        CHECK.append(0)
    else:
        CHECK.append(1)

    if 2.79 < (height / width_2) < 2.83:    # Tỉ lệ xấp xỉ của chiều cao và chiều rộng thân giữa 
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xét xem có lỗi tỉ lệ chai nước không. 
    BOTTLE_CHECK = []
    if 1 in CHECK :             # Nếu có thì trả về cho danh sách kết quả 'BOTTLE_CHECK' là 1 
        BOTTLE_CHECK.append(1)
    else:                       # Nếu không thì trả về cho danh sách kết quả 'BOTTLE_CHECK' là 0
        BOTTLE_CHECK.append(0)  
    return BOTTLE_CHECK
