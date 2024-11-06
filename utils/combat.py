import pygame

pygame.init()

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)


# Reset battle to initial state
def reset_battle(hero, enemies):
    global game_over, current_fighter, action_cooldown

    hero.reset()
    for enemy in enemies:
        enemy.reset()
    current_fighter = 1
    action_cooldown = 0
    game_over = 0
    print("Game_over", game_over)


# Buy upgrade/potions
def buy_upgrade(cost, stat_increase, stat_name, hero):
    if hero.gold >= cost:
        hero.gold -= cost
        stat_increase()
        print(f"{stat_name}:", getattr(hero, stat_name))


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
