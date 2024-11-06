import pygame
import random

from utils.healthBar import HealthBar

pygame.init()
# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))

positions = [(530, 270), (700, 270)]
health_bar_positions = [
    (550, screen_height - bottom_pannel + 40),
    (550, screen_height - bottom_pannel + 100),
]


# Select Random Enemies
def selectEnemies(enemy_options):
    selected_enemies = random.sample(enemy_options, 2)
    enemies = []
    health_bars = []

    for i, enemy in enumerate(selected_enemies):
        enemy.set_position(positions[i])
        enemies.append(enemy)
        health_bars.append(
            HealthBar(
                health_bar_positions[i][0],
                health_bar_positions[i][1],
                enemy.hp,
                enemy.max_hp,
            )
        )

    return enemies, health_bars
