from pygame.locals import *
import pygame

from utils.draw import draw_bg, draw_gold, draw_panel

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("assets/Icons/espadas.png").convert_alpha()

# ======== FPS ========
clock = pygame.time.Clock()
fps = 30

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False

def basic(place, hero, enemies=None):
    screen.fill(black)
    clock.tick(fps)

    draw_bg(place)
    draw_panel(hero, enemies)
    draw_gold(hero)