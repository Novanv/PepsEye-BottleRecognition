import pygame
import cv2
from pygame.locals import *
import os
from threading import Timer
import numpy as np
import pandas as pd

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
camera = cv2.VideoCapture(1)
    
# Bắt đầu luồng chụp ảnh
capture_thread = None

#Logo ))
logo_fpt_path = os.path.join("image_set/logofptuniversity.png")
logo_fpt_surface = pygame.image.load(logo_fpt_path)
logo_fpt_surface = pygame.transform.scale(logo_fpt_surface, (150, 58))

#Exit ))
exit_path = os.path.join("image_set/exit.png")
exit_surface = pygame.image.load(exit_path)
exit_surface = pygame.transform.scale(exit_surface, (40, 40))
exit_clickable_area = pygame.Rect(20, screen_height - 70, 40, 40)

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

# Thong tin good - error
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



#--------------------------------------------------------------        AI MODULE        ---------------------------------------------------------


# Hàm check bottle = > return [0] = Good hoặc [1] = Error

# Hàm check water level = > return [0] = Good hoặc [1] = Error



# Hàm check Label = > return [0] = Good hoặc [1] = Error
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




def MODULE_CHECK(image_path):
    # Đây là hàm thực thi các AI module
    # CHECK là một list nhận các giá trị [0,1,2,3] 
    # + Thực hiện kiểm tra Các biến trên để đưa lại kết quả cho CHECK để dẫn đến kết luận cuối cùng.

    CHECK = []
    # SIZE = (500,500) # Tất cả các ảnh đều resize về (500,500)

    # Biến check bottle = List giá trị trả về từ hàm Check bottle (image_path)

    # Biến check water level = List giá trị trả về từ hàm Check water level (image_path)

    # Biến check Label = List giá trị trả về từ hàm Check Label (image_path)

    LABEL_CHECK = LABEL_CHECK(image_path) # Lấy kết quả từ hàm kiểm tra vỏ chai 
    if 1 in LABEL_CHECK:                   # Nếu kết quả kiểm tra vỏ chai là lỗi, thêm giá trị 1 vào danh sách 'CHECK'
        CHECK.append(3)
    else:                                   # Nếu kết quả kiểm tra vỏ chai là tốt, thêm giá trị 0 vào danh sách 'CHECK'
        CHECK.append(0)

    

    return CHECK

#-----------------------------------------------------------------------------------------------------------------------------------------------




TYPE_ERROR = []
is_csv = False

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

    global capture_image
    global TYPE_ERROR
    while capture_image:
        TYPE_ERROR = capture_frame()
        pygame.time.wait(5000)  # Chờ 5 giây


# Bắt đầu luồng chụp ảnh
capture_thread = None

# Biến để kiểm soát
capture_image = False
is_square_detail_visible = False
is_detail_button_visible = True
is_start_button_visible = True
is_started = False
running = True

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
                    
                    capture_image = False
                    capture_thread.cancel()
                else:
                    status_light_color = (0,255,0)
                    button_start_color = (255, 0, 0)  # Màu đỏ
                    is_detail_button_visible = False
                    button_start_text = font.render("  END", True, (255, 255, 255))
                    
                    if not capture_image:
                        capture_image = True
                        capture_thread = Timer(5, capture_loop)  # Sử dụng Timer để tạo một luồng mới
                        capture_thread.start()    
                is_started = not is_started
                
                
            if  exit_clickable_area.collidepoint(event.pos):
                running = False
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
            
        pygame.display.flip()

camera.release()
pygame.quit()
