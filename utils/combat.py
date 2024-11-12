from pygame.locals import *
import pygame
from utils.variables import *
from utils.loop import handle_events
pygame.init()

# Reset battle to initial state
def reset_battle(hero, enemies):
    global game_over, current_fighter, action_cooldown

    hero.reset()
    for enemy in enemies:
        enemy.reset()
    current_fighter = 1
    action_cooldown = 0
    game_over = 0
    print("Game Over", game_over)


# Class DamageText for damage an heal
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# Hides the mouse icon when hovering over a living enemy
def hide_mouse(pos, enemies):
    if (
        enemies[0].hitbox.collidepoint(pos)
        and enemies[0].alive == True
        or enemies[1].hitbox.collidepoint(pos)
        and enemies[1].alive == True
    ):
        pygame.mouse.set_visible(False)
        screen.blit(sword_img, pos)
    else:
        pygame.mouse.set_visible(True)
