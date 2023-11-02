import pygame
import cv2
from pygame.locals import *
import os
from threading import Timer
import numpy as np
import pandas as pd
import os

pygame.init()

screen_width = 1280
screen_height = 720

# Kích thước cửa sổ hiển thị camera
camera_width = 500
camera_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DETECT ERRORS")

font = pygame.font.Font(None, 36)
border_radius_button = 30

# Thiết lập camera
camera = cv2.VideoCapture(0)
    
# Bắt đầu luồng chụp ảnh
capture_thread = None

#Logo ))
logo_fpt_path = os.path.join("UI/image_set/logofptuniversity.png")
logo_fpt_surface = pygame.image.load(logo_fpt_path)
logo_fpt_surface = pygame.transform.scale(logo_fpt_surface, (150, 58))

#Exit button ))

exit_path = os.path.join("UI/image_set/exit.png")
exit_surface = pygame.image.load(exit_path)
exit_surface = pygame.transform.scale(exit_surface, (40, 40))
exit_clickable_area = pygame.Rect(20, screen_height - 70, 40, 40)

#Exit setting button ))
exit_setting_path = os.path.join("UI/image_set/exit_setting.png")
exit_setting_surface = pygame.image.load(exit_setting_path)
exit_setting_surface = pygame.transform.scale(exit_setting_surface, (30, 30))
exit_setting_clickable_area = pygame.Rect(710,10, 30, 30)

#setting button ))
setting_path = os.path.join("UI/image_set/settings.png")
setting_surface = pygame.image.load(setting_path)
setting_surface = pygame.transform.scale(setting_surface, (40, 40))
setting_clickable_area = pygame.Rect(20, screen_height - 120, 40, 40)

#Time - icon ))
time_icon_path = os.path.join("UI/image_set/time.png")
time_icon_surface = pygame.image.load(time_icon_path)
time_icon_surface = pygame.transform.scale(time_icon_surface, (25, 25))

# Button Start - End
button_start_rect = pygame.Rect(screen_width - 410, screen_height - 120, 120, 50)  
button_start_color = (0,128,0)
button_start_text = font.render("START", True, (255, 255, 255))
text_start_rect = button_start_text.get_rect(center=button_start_rect.center)


# Button Detail
button_detail_rect = pygame.Rect(screen_width - 240, screen_height - 120, 120, 50)
button_detail_color = (128,128,0)
button_detail_text = font.render("DETAIL", True, (255, 255, 255))
text_detail_rect = button_detail_text.get_rect(center=button_detail_rect.center)

# Button submit time
button_submit_time_rect = pygame.Rect(screen_width - 240, screen_height - 120, 120, 50)
button_submit_time_color = (255,0,0)
button_submit_time_text = font.render("submit", True, (255, 255, 255))
text_submit_time_rect = button_submit_time_text.get_rect(center=button_detail_rect.center)


# hộp để show thông tin
big_square_rect = pygame.Rect((screen_width - 500 - 30), 30, 500, 500) 
big_square_color = (255, 255, 255)   

# Tạo đường phân tách hộp thông tin
separation_rect = pygame.Rect((screen_width - 500 - 30 + 3), 350, (500-6), 3) 
separation_color = (0, 0, 0)  

# Thông báo trạng thái hoạt động
font_status = pygame.font.Font(None, 26)
status_text = font_status.render("STATUS: ", True, (0, 0, 0))
status_rect = button_detail_text.get_rect(center=(570, 540 + 20))

# Đèn thông báo status
status_light_rect = pygame.Rect(620, 540, 30, 30) 
status_light_color = (255,0,0) 

# Các thành phần trong hộp thông tin
bottle_error_text = font.render("Bottle: ", True, (0, 0, 0))
bottle_error_rect = button_detail_text.get_rect(center=((screen_width - 470), 370 + 20))

label_error_text = font.render("Label : ", True, (0, 0, 0))
label_error_rect = button_detail_text.get_rect(center=((screen_width - 470), 410 + 20))

water_error_text = font.render("Water level: ", True, (0, 0, 0))
water_error_rect = button_detail_text.get_rect(center=((screen_width - 470), 450 + 20))

# Thông tin good - error
bottle_info_color = (0,200,0)
bottle_info_error_text = font.render("-", True, bottle_info_color)
bottle_info_error_rect = button_detail_text.get_rect(center=((screen_width - 280), 370 + 20))

label_info_color = (0,200,0)
label_info_error_text = font.render("-", True, label_info_color)
label_info_error_rect = button_detail_text.get_rect(center=((screen_width - 280), 410 + 20))

water_info_color = (0,200,0)
water_info_error_text = font.render("-", True, water_info_color)
water_info_error_rect = button_detail_text.get_rect(center=((screen_width - 280), 450 + 20))

# hộp để show thông tin khi bấm nút detail
big_square_detail_rect = pygame.Rect((screen_width - 500 - 30), 30, 500, 500) 
big_square_detail_color = (255, 255, 255) 

# hộp để setting thông tin khi bấm nút setting
big_square_setting_rect = pygame.Rect(700, -10 , 700,screen_height + 20) 
big_square_setting_color = (255, 255, 255) 

#Input waiting time number
input_box = pygame.Rect(1050, 102, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color_input_box_wt = color_inactive
text_waiting_time = ''

<<<<<<< HEAD
#Thẻ cha chứa On button và OFF button phần Boot time trong setting
div_ON_OFF_boot = pygame.draw.rect(screen,(255, 0, 255),(1050,187,200,40))

## ---------On button set boot time
boot_time_text_on = font.render("ON", True, (0,0,0))
boot_time_rect_on = boot_time_text_on.get_rect(center=(1096,210))
boot_time_rect_on_box = pygame.draw.rect(screen,(255, 255, 255),(1050,187,100,40))

## ----------OFF button set boot time
boot_time_text_off = font.render("OFF", True, (0,0,0))
boot_time_rect_off = boot_time_text_off.get_rect(center=(1200,210))
boot_time_rect_off_box = pygame.draw.rect(screen,(255, 255, 255),(1150,187,100,40))

#Thẻ cha chứa On button và OFF button phần sample data trong setting
div_ON_OFF_sample = pygame.draw.rect(screen,(255, 0, 255),(1050,267,200,40))

## ------------On button set sample data
sample_data_text_on = font.render("ON", True, (0,0,0))
sample_data_rect_on = sample_data_text_on.get_rect(center=(1096,289))
sample_data_rect_on_box = pygame.draw.rect(screen,(255, 255, 255),(1050,267,100,40))

## -------------OFF button set sample data
sample_data_text_off = font.render("OFF", True, (0,0,0))
sample_data_rect_off = sample_data_text_off.get_rect(center=(1200,289))
sample_data_rect_off_box = pygame.draw.rect(screen,(255, 255, 255),(1150,267,100,40))

# Button capture sample
button_capture_sample_rect = pygame.Rect(400, 600, 120, 50)
button_capture_sample_color = (0,0,128)
button_capture_sample_text = font.render("capture", True, (255,255,255))
text_capture_sample_rect = button_capture_sample_text.get_rect(center=button_capture_sample_rect.center)


=======
>>>>>>> 05d733bdc7e3ce6af10e0283ada6d0f186a2919e
#--------------------------------------------------------------        AI MODULE        ---------------------------------------------------------





# Hàm check bottle = > return [0] = Good hoặc [1] = Error -------------------------------/
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

    # Áp dụng Gaussian Blur để làm mịn ảnh, dùng bộ lọc 3x3 với độ lệch chuẩn 1 (mức độ mịn)
    image_GauBlur = cv2.GaussianBlur(img_roi, (3, 3), 1)    # Sau đó gán cho biến 'image_GauBlur'

    # Chuyển đổi ảnh sang ảnh grayscale (thang màu xám), cụ thể từ không gian màu Blue,Green,Red sang Gray
    gray = cv2.cvtColor(image_GauBlur, cv2.COLOR_BGR2GRAY)  # Gán ảnh ở grayscale cho biến 'gray'

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges = cv2.Canny(gray, 30, 90)     # Gán ảnh phát hiện ra cạnh của chai nước cho biến 'edges'

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
    roi_1_x1 = int(height*0.1269)
    roi_1_x2 = int(height*0.1746)
    roi_2_x1 = int(height*0.1904)
    roi_2_x2 = int(height*0.3492)

    # Phần thân giữa lấy 2 vị trí, lần lượt mỗi vị trí sẽ lấy hai tham số là 'x' trong cột 'Oxy'
    roi_3_x1 = int(height*0.3968)
    roi_3_x2 = int(height*0.4761)
    roi_4_x1 = int(height*0.5873)
    roi_4_x2 = int(height*0.6984)

    # Phần thân dưới lấy 2 vị trí, lần lượt mỗi vị trí sẽ lấy hai tham số là 'x' trong cột 'Oxy' 
    roi_5_x1 = int(height*0.7142)
    roi_5_x2 = int(height*0.7619)
    roi_6_x1 = int(height*0.7936)
    roi_6_x2 = int(height*0.9841)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi1 = cv2.Canny(gray_roi1, 20, 80)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi2 = cv2.Canny(gray_roi2, 20, 80)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi3 = cv2.Canny(gray_roi3, 20, 80)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi4 = cv2.Canny(gray_roi4, 20, 80)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi5 = cv2.Canny(gray_roi5, 20, 80)

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

    # Áp dụng phương pháp Canny để phát hiện các cạnh của chai nước với ngưỡng dưới là 20 và ngưỡng trên là 80
    edges_roi6 = cv2.Canny(gray_roi6, 20, 80)

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
    if 0.84 <= (wide_1 / wide_2) <= 1 : 
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_3 vs roi_4
    if 0.96 <(wide_3 / wide_4) < 1.04:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_5 vs roi_6
    if 0.93 <= (wide_5 / wide_6) <= 1:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_2 vs roi_3
    if 0.94 <= (wide_3 / wide_2) < 0.98:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_2 vs roi_6
    if 0.97 < (wide_2 / wide_6) < 1.03:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu rong roi_3 vs roi_6
    if 0.94 <= (wide_3 / wide_6) < 0.98:
        CHECK.append(0)
    else:
        CHECK.append(1)

    # Xet chieu cao 
    if 3.25 < (height / wide_2) < 3.7:
        CHECK.append(0)
    else:
        CHECK.append(1)

    if 3.4 < (height / wide_4) < 3.85:
        CHECK.append(0)
    else:
        CHECK.append(1)

    if 3.25 < (height / wide_2) < 3.7:
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
def LABEL_CHECK(image_path):
    # Tạo một danh sách để check xem vỏ chai có lỗi không
    CHECK = []

    # Đọc ảnh từ đường dẫn và gán cho biến 'img'
    image = cv2.imread(image_path)

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
    if white_pixel_count < 500: #Check màu pixel < 500 (nhỏ hơn 500)
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


def MODULE_CHECK(image_path):
    # Đây là hàm thực thi các AI module
    # CHECK là một list nhận các giá trị [0,1,2,3] 
    # + Thực hiện kiểm tra Các biến trên để đưa lại kết quả cho CHECK để dẫn đến kết luận cuối cùng.

    CHECK = []

    # Biến check bottle = List giá trị trả về từ hàm Check bottle (image_path)
    BOTTLE_CHECK_ = BOTTLE_CHECK(image_path) # Lấy kết quả từ hàm kiểm tra vỏ chai 
    if 1 in BOTTLE_CHECK_:                   # Nếu kết quả kiểm tra vỏ chai là lỗi, thêm giá trị 1 vào danh sách 'CHECK'
        CHECK.append(1)
    else:                                   # Nếu kết quả kiểm tra vỏ chai là tốt, thêm giá trị 0 vào danh sách 'CHECK'
        CHECK.append(0)       


    # Biến check Label = List giá trị trả về từ hàm Check Label (image_path)
    LABEL_CHECK_ = LABEL_CHECK(image_path) # Lấy kết quả từ hàm kiểm tra vỏ chai 
    if 1 in LABEL_CHECK_:                   # Nếu kết quả kiểm tra vỏ chai là lỗi, thêm giá trị 1 vào danh sách 'CHECK'
        CHECK.append(2)
    else:                                   # Nếu kết quả kiểm tra vỏ chai là tốt, thêm giá trị 0 vào danh sách 'CHECK'
        CHECK.append(0)

        
    # Biến check water level = List giá trị trả về từ hàm Check water level (image_path)
    WATER_CHECK_ = WATER_CHECK(image_path) # Lấy kết quả từ hàm kiểm tra  
    if 1 in WATER_CHECK_:                   # Nếu kết quả kiểm tra water level là lỗi, thêm giá trị 2 vào danh sách 'CHECK'
        CHECK.append(3)
    else:                                   # Nếu kết quả kiểm tra water level là tốt, thêm giá trị 0 vào danh sách 'CHECK'
        CHECK.append(0)

    return CHECK

# #-----------------------------------------------------------------------------------------------------------------------------------------------


# # --------------------------------------------Các biến kểm soát------------------------------------------------------------/
TYPE_ERROR = []

Timer_wait = 0
waiting_time_var = 5 # Biến kiểm soát thời gian đợi để chụp ảnh tiếp theo
boot_time_var = 5 # Biến kiểm soát thời gian boot

# Biến để kiểm soát
is_csv = False
is_countdown = False
capture_image = False
is_square_detail_visible = False
is_square_setting_visible = False
is_detail_button_visible = True
is_start_button_visible = True
is_exit_setting_button_visible = False
is_started = False
running = True
input_text_waiting_time_active = False
is_error_wt = False
is_starting_up = False
is_boot_time = True
is_sample_data = False

# Bắt đầu luồng chụp ảnh
capture_thread = None

def is_valid_input(text):
    # Hàm này kiểm tra xem chuỗi nhập vào chỉ chứa số hay không
    if (len(text) < 3) and (text.isdigit() == True):
        return True
    else:
        return False

# Tách riêng hàm chụp ảnh thủ công, hàm này thực hiện chụp ảnh khi người dùng bấm nước CAPTURE trong mục setting để tạo bộ ảnh sample một cách thủ công.
def capture_sample():
    ret, frame = camera.read()
    folder_path = "sample_data"
    if ret:
        item_count = len(os.listdir(folder_path))
        sample_image = "sample_" + str(item_count + 1) + ".jpg"
        path_sample_image = folder_path + "/"+ sample_image
        cv2.imwrite(path_sample_image,frame)


# Hàm chụp ảnh và lưu vào thư mục hiện tại
def capture_frame():
    # Hàm thực hiện việc chụp ảnh
    # Ảnh đã chụp sẽ được lưu thành captured_image.jpg
    # List_error có thể nhận các giá trị [0,1,2,3] để thực hiện việc kiểm tra điều kiện để show thông tin kiểm tra chai nước ra ngoài màn hình
    # is_csv để thực hiện việc [on] cho biến [nút on/off] cho việc kiêm tra, thực thi với file csv

    global is_csv
    list_error = []
    ret, frame = camera.read()
    if ret:
        image_path = "captured_image.jpg"
        cv2.imwrite(image_path, frame)
        list_error = MODULE_CHECK(image_path)
        is_csv = True
        return list_error

# Hàm để chạy đồng hồ đếm và chụp ảnh sau mỗi 5 giây


def capture_loop():

    #Hàm thực hiện việc đợi 5s
    global is_countdown
    global capture_image
    global TYPE_ERROR
    global Timer_wait
    global is_starting_up
    while capture_image:
        TYPE_ERROR = capture_frame()
        Timer_wait = pygame.time.get_ticks()
        is_countdown = True
        is_starting_up = False
        pygame.time.wait(waiting_time_var*1000)  # Chờ 5 giây


# Phần thân chính chạy app-------------------------------------------------------------------------------------------------------------------|

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if button_start_rect.collidepoint(event.pos):
                if is_started:
                    status_light_color = (255,0,0)
                    button_start_color = (0,128,0)  # Màu xanh
                    is_detail_button_visible = True
                    button_start_text = font.render("START", True, (255, 255, 255))
                    
                    is_starting_up = False
                    capture_image = False
                    is_countdown = False
                    capture_thread.cancel()
                else:
                    is_starting_up = True
                    status_light_color = (0,255,0)
                    button_start_color = (255, 0, 0)  # Màu đỏ
                    is_detail_button_visible = False
                    button_start_text = font.render("  END", True, (255, 255, 255))
                    
                    if not capture_image:
                        capture_image = True
                        capture_thread = Timer(boot_time_var, capture_loop)  # Sử dụng Timer để tạo một luồng mới
                        capture_thread.start()    
                is_started = not is_started
                
              
            if setting_clickable_area.collidepoint(event.pos):
                if is_sample_data == False:
                    is_square_setting_visible = True
                    is_exit_setting_button_visible = True
            
            if exit_setting_clickable_area.collidepoint(event.pos):
                if is_sample_data == False:
                    if is_square_setting_visible:    
                        is_square_setting_visible = False
                        is_exit_setting_button_visible = False
            
            if is_square_setting_visible:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_text_waiting_time_active = not input_text_waiting_time_active
                    else:
                        input_text_waiting_time_active = False
                    color_input_box_wt = color_active if input_text_waiting_time_active else color_inactive

            if is_square_setting_visible == False:  
                if button_detail_rect.collidepoint(event.pos):
                    if is_square_detail_visible:
                        is_start_button_visible = True
                        button_detail_color = (128,128,0)
                        button_detail_text = font.render("DETAIL", True, (255, 255, 255))
                    else:
                        is_start_button_visible = False
                        button_detail_color = (0,0,0)
                        button_detail_text = font.render(" BACK", True, (255, 255, 255))
                    is_square_detail_visible = not is_square_detail_visible
            
            # điều kiện kết thúc app    
            if  exit_clickable_area.collidepoint(event.pos):
                running = False  
                
            if is_square_setting_visible == True and (not is_started == True):
                if button_submit_time_rect.collidepoint(event.pos):
                    if is_valid_input(text_waiting_time):
                        waiting_time_var = int(text_waiting_time)
                        is_error_wt = False
                    else:
                        is_error_wt = True
                    text_waiting_time = ''

                if boot_time_rect_on_box.collidepoint(event.pos):
                    is_boot_time = True
                if boot_time_rect_off_box.collidepoint(event.pos):
                    is_boot_time = False
                
                if sample_data_rect_on_box.collidepoint(event.pos):
                    is_sample_data = True
                    is_exit_setting_button_visible = False
                if sample_data_rect_off_box.collidepoint(event.pos):
                    is_sample_data = False
                    is_exit_setting_button_visible = True
            
            if button_capture_sample_rect.collidepoint(event.pos):
                if is_square_setting_visible ==True and is_sample_data == True:
                    capture_sample()
                      
        if event.type == pygame.KEYDOWN:
            if input_text_waiting_time_active:
                if event.key == pygame.K_BACKSPACE:
                    text_waiting_time = text_waiting_time[:-1]
                else:
                    text_waiting_time += event.unicode         
    # Vẽ nền trắng
    screen.fill((192,192,192))    
      
    ret, frame = camera.read()
    if ret:
        # Lật ảnh theo chiều ngang
        frame = cv2.flip(frame, 1)
        # Xoay hình ảnh -90 độ
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, (camera_width, camera_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (30, 30))
            
        pygame.draw.rect(screen, big_square_color, big_square_rect)
        pygame.draw.rect(screen, (0,0,128), big_square_rect, 3)
        
        # signal starting up 
        if is_starting_up:
            font_starting_up_text = pygame.font.Font(None, 36)
            starting_up_text = font_starting_up_text.render("...", True, (255, 0, 0))
            starting_up_rect = starting_up_text.get_rect(center=(430, 557))
            screen.blit(starting_up_text, starting_up_rect)
        
        if len(TYPE_ERROR) > 0:
            #image Show
            captured_image_path = os.path.join("captured_image.jpg")
            captured_image_surface = pygame.image.load(captured_image_path)
            original_image_width, original_image_height = captured_image_surface.get_size()
            
            w_show = 400
            h_show = 300
            x_show = (original_image_width - w_show) // 2
            y_show = (original_image_height - h_show) // 2
            captured_image_surface = captured_image_surface.subsurface(x_show,y_show,w_show,h_show)
            captured_image_surface = pygame.transform.scale(captured_image_surface, (450, 300))
            screen.blit(captured_image_surface,(screen_width - 505, 40))
            
            if 0 in TYPE_ERROR:
                # Thêm thông tin và hồ sơ csv
                if is_csv:
                    df = pd.read_csv("data.csv")
                    id = int(df.shape[0])
                    new_data = pd.DataFrame({
                        "id" : id,
                        "bottle": [0],
                        "label" : [0],
                        "water" : [0],
                        "type" : [0]
                    })
                    result = pd.concat([df,new_data],ignore_index=True)
                    result.to_csv("data.csv",index=False)
                    is_csv = not is_csv
                
                bottle_info_error_text = font.render("GOOD", True, bottle_info_color)
                label_info_error_text = font.render("GOOD", True, label_info_color)
                water_info_error_text = font.render("GOOD", True, water_info_color)
            else:
                # Thêm thông tin và hồ sơ csv
                df = pd.read_csv("data.csv")
                id = int(df.shape[0])
                bottle_csv = 0
                label_csv = 0
                water_csv = 0
                
                bottle_info_error_text = font.render("GOOD", True, bottle_info_color)
                label_info_error_text = font.render("GOOD", True, label_info_color)
                water_info_error_text = font.render("GOOD", True, water_info_color)
                if 1 in TYPE_ERROR:
                    bottle_csv = 1
                    bottle_info_error_text = font.render("ERROR", True, (200,0,0))
                if 2 in TYPE_ERROR:
                    label_csv = 1
                    label_info_error_text = font.render("ERROR", True, (200,0,0))
                if 3 in TYPE_ERROR:
                    water_csv = 1
                    water_info_error_text = font.render("ERROR", True, (200,0,0))
                
                if is_csv:
                    df = pd.read_csv("data.csv")
                    new_data = pd.DataFrame({
                        "id" : id,
                        "bottle": [bottle_csv],
                        "label" : [label_csv],
                        "water" : [water_csv],
                        "type" : [1]
                    })
                    result = pd.concat([df,new_data],ignore_index=True)
                    result.to_csv("data.csv",index=False)
                    is_csv = not is_csv
            
                
        if is_detail_button_visible:
            pygame.draw.rect(screen, button_detail_color, button_detail_rect, border_radius = border_radius_button)
            screen.blit(button_detail_text, text_detail_rect)
        if is_start_button_visible:
            pygame.draw.rect(screen, button_start_color, button_start_rect, border_radius = border_radius_button)
            screen.blit(button_start_text, text_start_rect)
        
        pygame.draw.rect(screen, (0,0,0), separation_rect, 3)
        pygame.draw.rect(screen, separation_color, separation_rect)
        
        pygame.draw.rect(screen, status_light_color, status_light_rect, border_radius = border_radius_button)
        screen.blit(status_text, status_rect)
        
        screen.blit(bottle_error_text, bottle_error_rect)
        screen.blit(label_error_text, label_error_rect)
        screen.blit(water_error_text, water_error_rect)
        
        screen.blit(bottle_info_error_text, bottle_info_error_rect)
        screen.blit(label_info_error_text, label_info_error_rect)
        screen.blit(water_info_error_text, water_info_error_rect)

        screen.blit(logo_fpt_surface,(120, screen_height - 100))
        
        screen.blit(exit_surface,(20, screen_height - 70))
        
        screen.blit(setting_surface,(20, screen_height - 120))
        
        screen.blit(time_icon_surface,(380, 538))
        
        if is_square_setting_visible:
            pygame.draw.rect(screen, big_square_setting_color, big_square_setting_rect)
            pygame.draw.rect(screen, (0,0,128), big_square_setting_rect, 3)
            if is_exit_setting_button_visible:
                screen.blit(exit_setting_surface,(710,10))
            
            if is_started:
                font_noti_submit_text = pygame.font.Font(None, 20)
                noti_submit_text = font_noti_submit_text.render("Stop the program before setting", True, (255, 0, 0))
                noti_submit_rect = noti_submit_text.get_rect(center=(screen_width-120, screen_height-20))
                screen.blit(noti_submit_text, noti_submit_rect)
            
            if not is_started:
                pygame.draw.rect(screen, button_submit_time_color, button_submit_time_rect, border_radius = border_radius_button)
                screen.blit(button_submit_time_text, text_submit_time_rect)
            
            # Các thành phàn trong ô settings
            # ----------- Phần setting title ----------------------------------------------------/
            title_setting_text = font.render("SETTINGS", True, (255, 0, 0))
            title_setting_rect = title_setting_text.get_rect(center=(980, 80))
            screen.blit(title_setting_text, title_setting_rect)
            
            # ----------- Phần set waiting time ----------------------------------------------/
            waiting_time_text = font.render("Waiting time: ", True, (0, 0, 0))
            waiting_time_rect = waiting_time_text.get_rect(center=(800,130))
            screen.blit(waiting_time_text, waiting_time_rect)
            
            time_text = font.render(str(waiting_time_var), True, (255,0,255))
            time_rect = waiting_time_text.get_rect(center=(1000,132))
            screen.blit(time_text,  time_rect)
            
            font_set_time_text = pygame.font.Font(None, 26)
            set_time_text = font_set_time_text.render("Change", True, (0,0,0))
            set_time_rect = set_time_text.get_rect(center=(1000,134))
            screen.blit(set_time_text, set_time_rect)
            
            txt_surface = font.render(text_waiting_time, True, (0,0,0))
            width = max(100, txt_surface.get_width()+10)
            input_box.w = width
            text_y = input_box.centery - txt_surface.get_height() // 2
            screen.blit(txt_surface, (input_box.x+10, text_y))
            pygame.draw.rect(screen, color_input_box_wt, input_box, 2)
            
            # -------------------Phần set start up time --------------------------------------------/
            boost_time_text = font.render("Boot time: ", True, (0, 0, 0))
            boost_time_rect = boost_time_text.get_rect(center=(780,210))
            screen.blit(boost_time_text, boost_time_rect)
            
            screen.blit(boot_time_text_on, boot_time_rect_on)
            
            screen.blit(boot_time_text_off,  boot_time_rect_off)
            
            pygame.draw.rect(screen, (0,0,0), div_ON_OFF_boot, 3)
            
            if is_boot_time == True:
                boot_time_var = 5
                
                boot_time_text_on = font.render("ON", True, (255,0,0))
                boot_time_text_off = font.render("OFF", True, (0,0,0))
                
                boot_time_text_status = font.render("ON", True, (255,0,255))
                boot_time_rect = boot_time_text_status.get_rect(center=(950,210))
                pygame.draw.rect(screen, (255,0,0), boot_time_rect_on_box,3)
                screen.blit(boot_time_text_status,  boot_time_rect)

            else:
                boot_time_var = 0
                
                boot_time_text_on = font.render("ON", True, (0,0,0))
                boot_time_text_off = font.render("OFF", True, (255,0,0))
                
                boot_time_text_status = font.render("OFF", True, (255,0,255))
                boot_time_rect = boot_time_text_status.get_rect(center=(950,210))
                pygame.draw.rect(screen, (255,0,0), boot_time_rect_off_box,3)
                screen.blit(boot_time_text_status,  boot_time_rect)
                
            #---------------------- Phần CAPTURE - Sample data -------------------------------------------------------/
            
            sample_data_text = font.render("Sample data: ", True, (0, 0, 0))
            sample_data_rect = sample_data_text.get_rect(center=(798,290))
            screen.blit(sample_data_text, sample_data_rect)
            
            screen.blit(sample_data_text_on, sample_data_rect_on)
            
            screen.blit(sample_data_text_off,  sample_data_rect_off)
            
            pygame.draw.rect(screen, (0,0,0), div_ON_OFF_sample, 3)
            
            if  is_sample_data: 
                sample_data_text_on = font.render("ON", True, (255,0,0))
                sample_data_text_off = font.render("OFF", True, (0,0,0))
                
                sample_data_text_status = font.render("ON", True, (255,0,255))
                sample_data_rect = sample_data_text_status.get_rect(center=(950,290))
                pygame.draw.rect(screen, (255,0,0), sample_data_rect_on_box,3)
                screen.blit(sample_data_text_status,  sample_data_rect)
                
                pygame.draw.rect(screen, button_capture_sample_color, button_capture_sample_rect, border_radius = border_radius_button)
                screen.blit(button_capture_sample_text, text_capture_sample_rect)
                
                font_noti_sample_data_text = pygame.font.Font(None, 26)
                noti_sample_data_text = font_noti_sample_data_text.render("Turn Off Sample data to Exit the settings", True, (255, 0, 0))
                noti_sample_data_rect = noti_sample_data_text.get_rect(center=(screen_width-395, 20))
                screen.blit(noti_sample_data_text, noti_sample_data_rect)
                
            else:
                sample_data_text_on = font.render("ON", True, (0,0,0))
                sample_data_text_off = font.render("OFF", True, (255,0,0))
                
                sample_data_text_status = font.render("OFF", True, (255,0,255))
                sample_data_rect = sample_data_text_status.get_rect(center=(950,290))
                pygame.draw.rect(screen, (255,0,0), sample_data_rect_off_box,3)
                screen.blit(sample_data_text_status,  sample_data_rect)
                
                   
            if is_error_wt:
                font_error_wt_text = pygame.font.Font(None, 18)
                error_wt_text = font_error_wt_text.render("Only numbers < 100", True, (255, 0, 0))
                error_wt_rect = error_wt_text.get_rect(center=(1108, 162))
                screen.blit(error_wt_text, error_wt_rect)
            
        if is_square_detail_visible:
            df = pd.read_csv("data.csv")
            type_counts = df['type'].value_counts()
            pygame.draw.rect(screen, big_square_detail_color, big_square_detail_rect)
            pygame.draw.rect(screen, (0,0,128), big_square_rect, 3)
            
            #Show thông tin lấy từ file csv
            TITTLE_info_color = (200,0,0)
            TITTLE_info_error_text = font.render("DATA", True, TITTLE_info_color)
            TITTLE_info_error_rect = button_detail_text.get_rect(center=((screen_width - 270), 70))
            screen.blit(TITTLE_info_error_text, TITTLE_info_error_rect)
            
            TOTAL_info_color = (0,0,0)
            TOTAL_content = str("Total number of products: " + str(df.shape[0]))
            TOTAL_info_error_text = font.render(TOTAL_content, True, TOTAL_info_color)
            TOTAL_info_error_rect = button_detail_text.get_rect(center=((screen_width - 440), 130))
            screen.blit(TOTAL_info_error_text, TOTAL_info_error_rect)
            
            good_info_color = (0,0,0)
            TOTAL_GOOD_content = str("Number of good products: " + str(type_counts.get(0,0)))
            good_info_error_text = font.render(TOTAL_GOOD_content, True, good_info_color)
            good_info_error_rect = button_detail_text.get_rect(center=((screen_width - 440), 200))
            screen.blit(good_info_error_text, good_info_error_rect)
            
            error_info_color = (0,0,0)
            TOTAL_ERROR_content = str("Number of defective products: " + str(type_counts.get(1,1)))
            error_info_error_text = font.render(TOTAL_ERROR_content, True, error_info_color)
            error_info_error_rect = button_detail_text.get_rect(center=((screen_width - 440), 270))
            screen.blit(error_info_error_text, error_info_error_rect)

            
        if is_countdown:
            elapsed_time = (pygame.time.get_ticks() - Timer_wait) // 1000
            if 0 <= elapsed_time <= waiting_time_var:
                countdown_text = font.render(str(waiting_time_var - elapsed_time) if (waiting_time_var - elapsed_time) != 0 else "-", True, (0,0,255))
                screen.blit(countdown_text, (425, 540))
            else:
                countdown_text = waiting_time_var
        pygame.display.flip()

camera.release()
pygame.quit()
