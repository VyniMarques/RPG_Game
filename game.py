from pygame.locals import *
from sys import exit
import pygame
import random
import button

pygame.init()

# FPS
clock = pygame.time.Clock()
fps = 30

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("midia/Icons/espadas.png").convert_alpha()

# ======== Game Variables ========
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# ======== Icon and Title ========
pygame.display.set_caption("Battle Game")
pygame.display.set_icon(programIcon)


# ======== Load Images ========

# ======== Background ========

# Background
background_img = pygame.image.load("midia/Background/background.png").convert_alpha()

background_city_img = pygame.image.load(
    "midia/Background/background_city.png"
).convert_alpha()

# ======== Icons ========
# Panel
panel_img = pygame.image.load("midia/Icons/panel.png").convert_alpha()

# Sword
sword_img = pygame.image.load("midia/Icons/sword.png").convert_alpha()

# Gold
gold_img = pygame.image.load("midia/Icons/gold.png").convert_alpha()

# Button
potion_img = pygame.image.load("midia/Icons/potion.png").convert_alpha()

# City
city_img = pygame.image.load("midia/Icons/city.png").convert_alpha()

# Battle
battle_img = pygame.image.load("midia/Icons/forest.png").convert_alpha()

# Restart
restart_img = pygame.image.load("midia/Icons/restart.png").convert_alpha()

# Victory
victory_img = pygame.image.load("midia/Icons/victory.png").convert_alpha()

# Defeat
defeat_img = pygame.image.load("midia/Icons/defeat.png").convert_alpha()

# Crosshair
crosshair_img = pygame.image.load("midia/Icons/crosshair.png").convert_alpha()

# ======== Functions ========


# Draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Draw Background forest
def draw_bg():
    screen.blit(background_img, (0, 0))


# Draw Background city
def draw_bg_city():
    screen.blit(background_city_img, (0, 0))


# Draw Panel
def draw_panel(city=0):
    screen.blit(panel_img, (0, screen_height - bottom_pannel))

    draw_text(
        f"{hero.name} HP: {hero.hp}",
        font,
        red,
        100,
        screen_height - bottom_pannel + 10,
    )

    if city == 0:
        for count, i in enumerate(enemy_list):
            draw_text(
                f"{i.name} HP: {i.hp}",
                font,
                red,
                550,
                (screen_height - bottom_pannel + 10) + count * 60,
            )


# Draw gold coins
def gold():
    gold_icon = screen.blit(gold_img, (0, 0))
    gold_text = GoldText(32, 0, str(hero.gold), white)
    gold_text.draw()


# ======== Classes ========


# Fighter (Base for player and enemy)
class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions, gold, scale_factor=3):
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.gold = gold
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle 1: attack 2: hurt 3: death
        self.update_time = pygame.time.get_ticks()

        self.scale_factor = scale_factor

        # Load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"midia/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f"midia/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f"midia/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f"midia/{self.name}/Death/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    # Update
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

    # Set variables to Attack animation and deal damage
    def attack(self, target):

        # Deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage

        # Enemy hurt animation
        target.hurt()

        # Check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
            target.dropGold(hero)
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)

        # Set variables to Attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    # Set variables to Idle animation
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    # # Set variables to Hurt animation
    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    # Set variables to Death animation
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

    def draw(self):
        screen.blit(self.image, self.rect)

    def dropGold(self, hero):
        amount = int(self.gold / random.randint(1, 3))
        self.gold -= amount
        hero.gold += amount


class Blacksmith:

    def __init__(self, x, y, name, scale_factor=3) -> None:
        self.name = name
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.scale_factor = scale_factor

        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"midia/{self.name}/idle/idle_0{i}.png")
            img = pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale_factor,
                    img.get_height() * self.scale_factor,
                ),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 300

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

    def draw(self):
        screen.blit(self.image, self.rect)


class Merchant:

    def __init__(self, x, y, name, scale_factor=3) -> None:
        self.name = name
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.scale_factor = scale_factor

        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"midia/{self.name}/merchant_0{i}.png")
            img = pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale_factor,
                    img.get_height() * self.scale_factor,
                ),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 300

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

    def draw(self):
        screen.blit(self.image, self.rect)


class Npc:

    def __init__(self, x, y, name, frames, scale_factor=3):
        self.name = name
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.scale_factor = scale_factor
        self.frames = frames

        temp_list = []
        for i in range(frames):
            img = pygame.image.load(f"midia/{self.name}/{i}.png")
            img = pygame.transform.scale(
                img,
                (
                    img.get_width() * self.scale_factor,
                    img.get_height() * self.scale_factor,
                ),
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 300

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

    def draw(self):
        screen.blit(self.image, self.rect)


# Health Bar (for player and enemy)
class HealthBar:

    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):

        # Update with new health
        self.hp = hp
        ratio = self.hp / self.max_hp

        # Calculate health ratio
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
        # Move damage text up
        self.rect.y -= 1
        # Delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


class GoldText(pygame.sprite.Sprite):

    def __init__(self, x, y, amount, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(amount, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)


# ======== Object Instances ========

damage_text_group = pygame.sprite.Group()

# Hero
hero = Fighter(200, 260, "Knight", 30, 10, 3, 4)
hero_in_city = Fighter(280, 300, "Knight", 30, 10, 3, 4, scale_factor=2)

# Npc
blacksmith = Blacksmith(650, 310, "Blacksmith", 2.6)
merchant = Merchant(390, 310, "Merchant", 2.6)
dog = Npc(550, 310, "Dog", 4, 2.6)
beggar = Npc(145, 315, "Beggar", 5, 2.6)
# Enemy
enemy1 = Fighter(550, 270, "Bandit", 10, 6, 0, 20)
enemy2 = Fighter(700, 270, "Bandit", 20, 6, 1, 5)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)

# Health bar
hero_health_bar = HealthBar(
    100, screen_height - bottom_pannel + 40, hero.hp, hero.max_hp
)
enemy1_health_bar = HealthBar(
    550, screen_height - bottom_pannel + 40, enemy1.hp, enemy1.max_hp
)
enemy2_health_bar = HealthBar(
    550, screen_height - bottom_pannel + 100, enemy2.hp, enemy2.max_hp
)

# Buttons
potion_button = button.Button(
    screen, 100, screen_height - bottom_pannel + 70, potion_img, 64, 64
)

restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

forge_button = button.Button(screen, 0, 30, city_img, 64, 64)
battle_button = button.Button(screen, 0, 30, battle_img, 64, 64)


# ======== Main Loop ========


def city():
    while True:

        screen.fill((0, 0, 0))
        draw_bg_city()
        if battle_button.draw():
            battle()
        draw_panel(1)
        hero_health_bar.draw(hero.hp)
        hero_in_city.update()
        hero_in_city.draw()
        blacksmith.update()
        blacksmith.draw()
        merchant.update()
        merchant.draw()
        potion_button.draw()

        dog.update()
        dog.draw()

        beggar.update()
        beggar.draw()

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)
        gold()

        # Quiting the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        pygame.display.update()


def battle():

    global game_over, current_fighter, action_cooldown

    while True:

        clock.tick(fps)

        screen.fill((0, 0, 0))

        # Draw background
        draw_bg()

        # Draw panel
        draw_panel()
        hero_health_bar.draw(hero.hp)
        enemy1_health_bar.draw(enemy1.hp)
        enemy2_health_bar.draw(enemy2.hp)

        # Draw fighters
        hero.update()
        hero.draw()

        gold()

        for enemy in enemy_list:
            enemy.update()
            enemy.draw()

        # Draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        # Reset actions variables
        attack = False
        potion = False
        target = None

        # Make sure mouse is visible
        pygame.mouse.set_visible(True)

        pos = pygame.mouse.get_pos()
        for count, enemy in enumerate(enemy_list):
            if enemy.rect.collidepoint(pos):
                # Hide mouse
                pygame.mouse.set_visible(False)
                # Show sword as mouse cursor
                screen.blit(sword_img, pos)
                if clicked == True and enemy.alive == True:
                    attack = True
                    target = enemy_list[count]
            else:
                # Mouse não está sobre um inimigo
                pygame.mouse.set_visible(True)

        if potion_button.draw():
            potion = True

        # Show potions remaining
        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        if game_over == 0:
            # Player action
            if hero.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:

                        # Look for player action

                        # Attack
                        if attack == True and target != None:
                            hero.attack(target)
                            current_fighter += 1
                            action_cooldown = 0

                        # Potion
                        if potion == True:
                            if hero.potions > 0:
                                # Check heal beyond max helth
                                if hero.max_hp - hero.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = hero.max_hp - hero.hp
                                hero.hp += heal_amount
                                damage_text = DamageText(
                                    hero.rect.centerx,
                                    hero.rect.y,
                                    str(heal_amount),
                                    green,
                                )
                                damage_text_group.add(damage_text)
                                hero.potions -= 1
                                current_fighter += 1
                                action_cooldown = 0
            else:
                game_over = -1

            # Enemy action
            for count, enemy in enumerate(enemy_list):
                if current_fighter == 2 + count:
                    if enemy.alive:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            # Cheack if enemy need to heal
                            if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                                # Check heal beyond max helth
                                if enemy.max_hp - enemy.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = enemy.max_hp - enemy.hp
                                enemy.hp += heal_amount
                                damage_text = DamageText(
                                    enemy.rect.centerx,
                                    enemy.rect.y,
                                    str(heal_amount),
                                    green,
                                )
                                damage_text_group.add(damage_text)
                                enemy.potions -= 1
                                current_fighter += 1
                                action_cooldown = 0
                            else:
                                # Attack
                                enemy.attack(hero)
                                current_fighter += 1
                                action_cooldown = 0
                    else:
                        current_fighter += 1

            # If all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        # Check if all enemies are dead
        alive_enemies = 0
        for enemy in enemy_list:
            if enemy.alive == True:
                alive_enemies += 1
        if alive_enemies == 0:
            game_over = 1

        # Check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
            if restart_button.draw():
                hero.reset()
                for enemy in enemy_list:
                    enemy.reset()
                current_fighter = 1
                action_cooldown
                game_over = 0

        if forge_button.draw():
            city()

        # Quiting the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

battle()