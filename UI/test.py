import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 400, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Countdown App")

font = pygame.font.Font(None, 36)
start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)

countdown = 7
counting = False
timer = 0
finished = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_button.collidepoint(event.pos) and not counting and not finished:
                counting = True
                timer = pygame.time.get_ticks()

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLACK, start_button)
    start_text = font.render("Start", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - 25, HEIGHT // 2 - 15))

    if counting:
        elapsed_time = (pygame.time.get_ticks() - timer) // 1000
        if elapsed_time <= countdown:
            countdown_text = font.render(str(countdown - elapsed_time), True, BLACK)
            screen.blit(countdown_text, (WIDTH // 2 - 10, HEIGHT // 2 - 15))
        else:
            counting = False
            countdown_text = font.render("Hello", True, BLACK)
            screen.blit(countdown_text, (WIDTH // 2 - 30, HEIGHT // 2 - 15))
            finished = True

    if not counting and finished:
        finished = False
        countdown = 7

    pygame.display.update()
