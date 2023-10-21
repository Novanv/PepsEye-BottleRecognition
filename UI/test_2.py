import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Input App")

font = pygame.font.Font(None, 36)
input_box = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
input_active = False

def is_valid_input(text):
    # Hàm này kiểm tra xem chuỗi nhập vào chỉ chứa số hay không
    return text.isdigit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = not input_active
            else:
                input_active = False
            color = color_active if input_active else color_inactive
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if is_valid_input(text):
                        print(text)  # In số khi nhấn Enter (OK)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill(WHITE)

    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    pygame.display.flip()
