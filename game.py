import pygame
from pygame.locals import *
from sys import exit
import random
import button

pygame.init()

# FPS
clock = pygame.time.Clock()
fps = 60

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("midia/Icons/espadas.png").convert_alpha()

# game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0


font = pygame.font.SysFont("Times New Roman", 26)

red = (255, 0, 0)
green = (0, 255, 0)


pygame.display.set_caption("Battle Game")
pygame.display.set_icon(programIcon)


# ======== Load Images ========

# Background Image
background_img = pygame.image.load("midia/Background/background.png").convert_alpha()

# Panel Image
panel_img = pygame.image.load("midia/Icons/panel.png").convert_alpha()

sword_img = pygame.image.load("midia/Icons/sword.png").convert_alpha()

# button image
potion_img = pygame.image.load("midia/Icons/potion.png").convert_alpha()

restart_img = pygame.image.load("midia/Icons/restart.png").convert_alpha()

# load victory and defeat
victory_img = pygame.image.load("midia/Icons/victory.png").convert_alpha()
defeat_img = pygame.image.load("midia/Icons/defeat.png").convert_alpha()


# ======== Functions ========

# Drawing text


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Background
def draw_bg():
    screen.blit(background_img, (0, 0))


# Panel
def draw_panel():
    # rect
    screen.blit(panel_img, (0, screen_height - bottom_pannel))

    draw_text(
        f"{knight.name} HP: {knight.hp}",
        font,
        red,
        100,
        screen_height - bottom_pannel + 10,
    )

    for count, i in enumerate(bandit_list):
        draw_text(
            f"{i.name} HP: {i.hp}",
            font,
            red,
            550,
            (screen_height - bottom_pannel + 10) + count * 60,
        )


# Fighter
class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle 1: attack 2: hurt 3: death
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"midia/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"midia/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # laod hurt image
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f"midia/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # laod death image
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f"midia/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * 3, img.get_height() * 3)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100

        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand

        target.hp -= damage
        # hurt animation
        target.hurt()

        # check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar:

    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):

        # update with new health
        self.hp = hp
        ratio = self.hp / self.max_hp

        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


class DamageText(pygame.sprite.Sprite):

    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

knight = Fighter(200, 260, "Knight", 30, 10, 3)
bandit1 = Fighter(550, 270, "Bandit", 10, 6, 1)
bandit2 = Fighter(700, 270, "Bandit", 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(
    100, screen_height - bottom_pannel + 40, knight.hp, knight.max_hp
)
bandit1_health_bar = HealthBar(
    550, screen_height - bottom_pannel + 40, bandit1.hp, bandit1.max_hp
)
bandit2_health_bar = HealthBar(
    550, screen_height - bottom_pannel + 100, bandit2.hp, bandit2.max_hp
)

# Create Buttons
potion_button = button.Button(
    screen, 100, screen_height - bottom_pannel + 70, potion_img, 64, 64
)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

while True:

    clock.tick(fps)

    screen.fill((0, 0, 0))

    draw_bg()
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    # draw damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # control player actions
    # reset actions variables

    attack = False
    potion = False
    target = None

    pygame.mouse.set_visible(True)

    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            # hide mouse
            pygame.mouse.set_visible(False)
            # show sword
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    # show potions remaining
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_pannel + 70)

    if game_over == 0:
        # player action
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # look for player action
                    # attack
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    # potion
                    if potion == True:
                        if knight.potions > 0:
                            # check heal beyond max helth
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            damage_text = DamageText(
                                knight.rect.centerx,
                                knight.rect.y,
                                str(heal_amount),
                                green,
                            )
                            damage_text_group.add(damage_text)
                            knight.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0
        else:
            game_over = -1

        # enemy action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # cheack if bandit need to heal
                        if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            # check heal beyond max helth
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount = potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            damage_text = DamageText(
                                bandit.rect.centerx,
                                bandit.rect.y,
                                str(heal_amount),
                                green,
                            )
                            damage_text_group.add(damage_text)
                            bandit.potions -= 1
                            current_fighter += 1
                            action_cooldown = 0
                        else:
                            # attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                else:
                    current_fighter += 1

        if current_fighter > total_fighters:
            current_fighter = 1

    # check if all bandits are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandits += 1
    if alive_bandits == 0:
        game_over = 1

    # check if game is over

    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()
