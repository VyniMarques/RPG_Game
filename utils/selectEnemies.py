import pygame

import random

from utils.healthBar import HealthBar
from utils.variables import *

pygame.init()


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
