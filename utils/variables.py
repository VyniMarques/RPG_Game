from pygame.locals import *
import pygame

from utils.button import Button

pygame.init()

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("assets/Icons/espadas.png").convert_alpha()

# ======== FPS ========
clock = pygame.time.Clock()
fps = 30

# ======== Title ========
pygame.display.set_caption("Battle Game")
pygame.display.set_icon(programIcon)

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)
title = pygame.font.SysFont("Times New Roman", 30)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)

# ======== Game Variables ========
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 45
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

# ======== Load Icons ========

# Panel
panel_img = pygame.image.load("assets/Icons/panel.png").convert_alpha()

# Gold
gold_img = pygame.image.load("assets/Icons/gold.png").convert_alpha()

# Sword
sword_img = pygame.image.load("assets/Icons/sword.png").convert_alpha()

# Potion
potion_img = pygame.image.load("assets/Icons/potion.png").convert_alpha()

# City
city_img = pygame.image.load("assets/Icons/city.png").convert_alpha()

# Forest
forest_img = pygame.image.load("assets/Icons/forest.png").convert_alpha()

# Map
map_img = pygame.image.load("assets/Icons/map.png").convert_alpha()

# Cave
cave_img = pygame.image.load("assets/Icons/cave.png").convert_alpha()

# Potion Store
potion_plus_img = pygame.image.load("assets/Icons/potion_plus.png").convert_alpha()

# Potion buy
potion_plus_b_img = pygame.image.load("assets/Icons/potion_plus2.png").convert_alpha()

# Forge
forge_img = pygame.image.load("assets/Icons/forge.png").convert_alpha()

# Return
return_img = pygame.image.load("assets/Icons/return.png").convert_alpha()

# Run Away
run_img = pygame.image.load("assets/Icons/run.png").convert_alpha()

# Strength
strength_img = pygame.image.load("assets/Icons/strength_plus.png").convert_alpha()

# Defense
defense_img = pygame.image.load("assets/Icons/defense_plus.png").convert_alpha()

# Restart
restart_img = pygame.image.load("assets/Icons/restart.png").convert_alpha()

# Victory
victory_img = pygame.image.load("assets/Icons/victory.png").convert_alpha()

# Defeat
defeat_img = pygame.image.load("assets/Icons/defeat.png").convert_alpha()

# Quest
quest_img = pygame.image.load("assets/Icons/quest.png").convert_alpha()
quest_complete_img = pygame.image.load(
    "assets/Icons/quest_complete.png"
).convert_alpha()

# ======== Load Character Images ========
knight_img = pygame.image.load("assets/Characters/knight.png").convert_alpha()

archer_img = pygame.image.load("assets/Characters/archer.png").convert_alpha()

assasin_img = pygame.image.load("assets/Characters/assasin.png").convert_alpha()

monk_img = pygame.image.load("assets/Characters/monk.png").convert_alpha()

priestess_img = pygame.image.load("assets/Characters/priestess.png").convert_alpha()

mauler_img = pygame.image.load("assets/Characters/mauler.png").convert_alpha()


# ======== Buttons ========
potion_button = Button(
    screen, 100, screen_height - bottom_pannel + 70, potion_img, 64, 64
)
potion_plus_button = Button(
    screen, 600, screen_height - bottom_pannel + 70, potion_plus_b_img, 64, 64
)
strength_plus_button = Button(
    screen, 600, screen_height - bottom_pannel + 70, strength_img, 64, 64
)

defense_plus_button = Button(
    screen, 500, screen_height - bottom_pannel + 70, defense_img, 64, 64
)

restart_button = Button(screen, 330, 120, restart_img, 120, 30)

city_button = Button(screen, 30, 100, city_img, 64, 64)

cave_button = Button(screen, 100, 100, cave_img, 64, 64)

forest_button = Button(screen, 170, 100, forest_img, 64, 64)

map_button = Button(screen, 0, 30, map_img, 64, 64)

return_button = Button(screen, 0, 80, return_img, 64, 64)

run_button = Button(screen, 0, 90, run_img, 64, 64)

quest_button = Button(screen, 0, 100, quest_img, 64, 64)

quest_complete_button = Button(screen, 0, 100, quest_complete_img, 64, 64)


# ======== Character selectors ========
knight_button = Button(screen, 100, 100, knight_img, 165, 165)

archer_button = Button(screen, 100, 285, archer_img, 165, 165)

assasin_button = Button(screen, 330, 100, assasin_img, 165, 165)

monk_button = Button(screen, 315, 285, monk_img, 170, 170)

priestess_button = Button(screen, 550, 100, priestess_img, 165, 165)

mauler_button = Button(screen, 550, 285, mauler_img, 165, 165)

positions = [(530, 270), (700, 270)]

health_bar_positions = [
    (550, screen_height - bottom_pannel + 40),
    (550, screen_height - bottom_pannel + 100),
]
