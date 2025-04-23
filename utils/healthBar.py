from pygame.locals import *
import pygame

from utils.variables import *

pygame.init()


# Health Bar (for player and enemy)
class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    # def draw(self, hp):

    #     # Update with new health
    #     self.hp = hp
    #     ratio = self.hp / self.max_hp

    #     # Calculate health ratio
    #     pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
    #     pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
    
    def draw(self, hp, max_hp=None):
        # Permite atualizar a vida máxima, se necessário
        if max_hp is not None:
            self.max_hp = max_hp

        self.hp = hp
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

