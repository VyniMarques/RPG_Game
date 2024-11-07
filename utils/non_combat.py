import pygame

pygame.init()

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)
red = (255, 0, 0)


# Buy upgrade/potions
def buy_upgrade(cost, stat_increase, stat_name, hero, max, npc, group):
    if getattr(hero, stat_name) < max:
        if hero.gold >= cost:
            hero.gold -= cost
            stat_increase()
            print(f"{stat_name}:", getattr(hero, stat_name))
    else:
        print(f"Max {stat_name}")
        message(npc, f"Max {stat_name}", red, group)


class MiscText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(text), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


def message(npc, text, color, group):
    misc_text = MiscText(npc.rect.centerx, npc.rect.y, str(text), color)
    group.add(misc_text)


def text_update(group, screen):
    group.update()
    group.draw(screen)
