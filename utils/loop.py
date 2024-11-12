from pygame.locals import *
import pygame

from utils.draw import draw_bg, draw_gold, draw_panel
from utils.variables import *


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
