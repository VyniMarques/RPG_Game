from pygame.locals import *
from sys import exit
import pygame
import random
import button

pygame.init()

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("midia/Icons/espadas.png").convert_alpha()

# ======== FPS ========
clock = pygame.time.Clock()
fps = 30

# ======== Title ========
pygame.display.set_caption("Battle Game")
pygame.display.set_icon(programIcon)

# ======== Text Variables ========
font = pygame.font.SysFont("Times New Roman", 26)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)

# ======== EnemyPosition ========
positions = [(530, 270), (700, 270)]
health_bar_positions = [
    (550, screen_height - bottom_pannel + 40),  
    (550, screen_height - bottom_pannel + 100),  
]

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
panel_img = pygame.image.load("midia/Icons/panel.png").convert_alpha()

# Sword
sword_img = pygame.image.load("midia/Icons/sword.png").convert_alpha()

# Gold
gold_img = pygame.image.load("midia/Icons/gold.png").convert_alpha()

# Potion
potion_img = pygame.image.load("midia/Icons/potion.png").convert_alpha()

# City
city_img = pygame.image.load("midia/Icons/city.png").convert_alpha()

# Forest
forest_img = pygame.image.load("midia/Icons/forest.png").convert_alpha()

# Map
map_img = pygame.image.load("midia/Icons/map.png").convert_alpha()

# Cave
cave_img = pygame.image.load("midia/Icons/cave.png").convert_alpha()

# Potion Store
potion_plus_img = pygame.image.load("midia/Icons/potion_plus.png").convert_alpha()

# Potion buy
potion_plus_b_img = pygame.image.load("midia/Icons/potion_plus2.png").convert_alpha()

# Forge
forge_img = pygame.image.load("midia/Icons/forge.png").convert_alpha()

# Return
return_img = pygame.image.load("midia/Icons/return.png").convert_alpha()

# Run Away
run_img = pygame.image.load("midia/Icons/run.png").convert_alpha()

# Strength
strength_img = pygame.image.load("midia/Icons/strength_plus.png").convert_alpha()

# Restart
restart_img = pygame.image.load("midia/Icons/restart.png").convert_alpha()

# Victory
victory_img = pygame.image.load("midia/Icons/victory.png").convert_alpha()

# Defeat
defeat_img = pygame.image.load("midia/Icons/defeat.png").convert_alpha()

# ======== Load Character Images ========
knight_img = pygame.image.load("midia/Characters/knight.png").convert_alpha()

archer_img = pygame.image.load("midia/Characters/archer.png").convert_alpha()

assasin_img = pygame.image.load("midia/Characters/assasin.png").convert_alpha()

monk_img = pygame.image.load("midia/Characters/monk.png").convert_alpha()

priestess_img = pygame.image.load("midia/Characters/priestess.png").convert_alpha()

mauler_img = pygame.image.load("midia/Characters/mauler.png").convert_alpha()

# ======== Functions ========


# Draw Background
def draw_bg(place):
    screen.blit(
        pygame.image.load(f"midia/Background/background_{place}.png").convert_alpha(),
        (0, 0),
    )


# Draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Draw Panel
def draw_panel(hero, enemies):
    screen.blit(panel_img, (0, screen_height - bottom_pannel))
    draw_text(
        f"{hero.name} HP: {hero.hp}", font, red, 100, screen_height - bottom_pannel + 10
    )

    if enemies != None:
        for count, enemy in enumerate(enemies):
            draw_text(
                f"{enemy.name} HP: {enemy.hp}",
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


# Select Hero
def selectHero(hero_op):
    global hero, hero_in_city, hero_health_bar

    print("Selecting Hero")

    # x, y, name, max_hp, strength, potions, gold, scale_factor, q_idle, q_hurt, q_death, q_attack
    if hero_op == 0:
        hero1 = Fighter(200, 260, "Knight", 30, 10, 3, 5, 3, 8, 3, 10, 8)
        hero_in_city1 = Fighter(280, 300, "Knight", scale_factor=2, q_idle=8)
    elif hero_op == 1:
        hero1 = Fighter(200, 160, "Archer", 30, 10, 3, 5, 2.8, 12, 6, 19, 15)
        hero_in_city1 = Fighter(280, 230, "Archer", scale_factor=2, q_idle=12)
    elif hero_op == 2:
        hero1 = Fighter(200, 160, "Assasin", 30, 10, 3, 5, 2.8, 8, 6, 12, 6)
        hero_in_city1 = Fighter(280, 225, "Assasin", scale_factor=2, q_idle=8)
    elif hero_op == 3:
        hero1 = Fighter(200, 165, "Monk", 30, 10, 3, 5, 3, 6, 6, 18, 6)
        hero_in_city1 = Fighter(280, 235, "Monk", scale_factor=2, q_idle=6)
    elif hero_op == 4:
        hero1 = Fighter(200, 150, "Priestess", 30, 10, 3, 5, 3, 8, 7, 16, 7)
        hero_in_city1 = Fighter(280, 220, "Priestess", scale_factor=2, q_idle=8)
    elif hero_op == 5:
        hero1 = Fighter(200, 150, "Mauler", 30, 10, 3, 5, 3, 8, 6, 15, 7)
        hero_in_city1 = Fighter(280, 220, "Mauler", scale_factor=2, q_idle=8)

    hero = hero1
    hero_in_city = hero_in_city1

    print("Heroi selected: " + hero.name)

    # ======== Health bar ========
    hero_health_bar = HealthBar(
        100, screen_height - bottom_pannel + 40, hero.hp, hero.max_hp
    )


# Select Random Enemies
def select_random_enemies(enemy_options):
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


def reset_battle(hero, enemies):
    global game_over, current_fighter
    hero.reset()
    for enemy in enemies:
        enemy.reset()
    current_fighter = 1
    action_cooldown
    game_over = 0


# ======== Classes ========


# Fighter (Basic for player and enemy)
class Fighter:
    def __init__(
        self,
        x,
        y,
        name,
        max_hp=10,
        strength=1,
        potions=0,
        gold=0,
        scale_factor=1,
        q_idle=0,
        q_hurt=0,
        q_death=0,
        q_attack=0,
    ):
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

        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(self.rect.x - 40, self.rect.y - 40, 120, 140)

        # Load idle images
        temp_list = []
        for i in range(q_idle):
            img = pygame.image.load(f"midia/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(q_attack):
            img = pygame.image.load(f"midia/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt images
        temp_list = []
        for i in range(q_hurt):
            img = pygame.image.load(f"midia/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death images
        temp_list = []
        for i in range(q_death):
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

    # Set position for the hitbox
    def set_position(self, position):
        self.rect.center = position
        self.hitbox.topleft = (
            self.rect.centerx - self.hitbox.width // 2,
            self.rect.centery - self.hitbox.height // 2,
        )

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
        print("Morreu")
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True
        # self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

        # Hitbox
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

    def dropGold(self, hero):
        amount = int(self.gold / random.randint(1, 3))
        self.gold -= amount
        print("Gold Drop", self.gold)
        hero.gold += amount


# Blacksmith
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


# Merchant
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
            img = pygame.image.load(f"midia/{self.name}/Idle/{i}.png")
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


# Generic NPC
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
            img = pygame.image.load(f"midia/{self.name}/Idle/{i}.png")
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


# Damage text
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


# Gold Text
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

# NPCs
blacksmith = Blacksmith(650, 310, "Blacksmith", 2.6)
blacksmith_city = Blacksmith(340, 260, "Blacksmith", 5)

merchant = Merchant(390, 310, "Merchant", 2.6)
merchant_city = Merchant(510, 260, "Merchant", 5)

dog = Npc(550, 310, "Dog", 4, 2.6)

beggar = Npc(145, 315, "Beggar", 5, 2.6)

# ====== Enemy List ======

# Forest
enemy_options1 = [
    Fighter(0, 0, "Bandit", 10, 6, 0, 20, 3, 8, 3, 10, 8),
    Fighter(0, 0, "Bandit", 10, 6, 0, 20, 3, 8, 3, 10, 8),
]

# Cave
enemy_options2 = [
    Fighter(0, 0, "Goblin", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "Skeleton", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "FlyingEye", 20, 5, 0, 20, 2.4, 8, 4, 4, 8),
    Fighter(0, 0, "Goblin", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "Skeleton", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "FlyingEye", 20, 5, 0, 20, 2.4, 8, 4, 4, 8),
]


# ======== Buttons ========
potion_button = button.Button(
    screen, 100, screen_height - bottom_pannel + 70, potion_img, 64, 64
)
potion_plus_button = button.Button(
    screen, 600, screen_height - bottom_pannel + 70, potion_plus_b_img, 64, 64
)
strength_plus_button = button.Button(
    screen, 600, screen_height - bottom_pannel + 70, strength_img, 64, 64
)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

city_button = button.Button(screen, 30, 100, city_img, 64, 64)

cave_button = button.Button(screen, 100, 100, cave_img, 64, 64)

forest_button = button.Button(screen, 170, 100, forest_img, 64, 64)

map_button = button.Button(screen, 0, 30, map_img, 64, 64)

return_button = button.Button(screen, 0, 80, return_img, 64, 64)

run_button = button.Button(screen, 0, 90, run_img, 64, 64)

# ======== Character selectors ========
knight_button = button.Button(screen, 100, 50, knight_img, 165, 165)

archer_button = button.Button(screen, 100, 200, archer_img, 165, 165)

assasin_button = button.Button(screen, 330, 50, assasin_img, 165, 165)

monk_button = button.Button(screen, 315, 215, monk_img, 170, 170)

priestess_button = button.Button(screen, 550, 50, priestess_img, 165, 165)

mauler_button = button.Button(screen, 550, 200, mauler_img, 165, 165)


# ======== Loops ========


def menu(selecionarHeroi):
    clicked = False
    pygame.mouse.set_visible(True)
    while True:

        screen.fill(black)
        pygame.mouse.set_visible(True)
        draw_bg("map")
        screen.blit(panel_img, (0, screen_height - bottom_pannel))
        clock.tick(fps)

        draw_text("RPG Game", font, black, 350, 20)

        if knight_button.draw():
            selecionarHeroi(0)
            pygame.time.delay(200)
            city()

        if archer_button.draw():
            selecionarHeroi(1)
            pygame.time.delay(200)
            city()

        if assasin_button.draw():
            selecionarHeroi(2)
            pygame.time.delay(200)
            city()

        if monk_button.draw():
            selecionarHeroi(3)
            pygame.time.delay(200)
            pygame.event.clear()
            city()

        if priestess_button.draw():
            selecionarHeroi(4)
            pygame.time.delay(200)
            city()

        if mauler_button.draw():
            selecionarHeroi(5)
            pygame.time.delay(200)
            city()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


def basic(place, hero, enemies=None):
    screen.fill(black)
    clock.tick(fps)

    draw_bg(place)
    draw_panel(hero, enemies)

    gold()


def map():
    clicked = False
    pygame.mouse.set_visible(True)
    while True:

        basic("map", hero)

        if forest_button.draw():
            forest()

        if city_button.draw():
            city()

        if cave_button.draw():
            cave()

        if potion_button.draw():
            potion = True

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        hero_health_bar.draw(hero.hp)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


def city():
    clicked = False
    cursor_hidden = False
    pygame.mouse.set_visible(True)
    while True:

        basic("city", hero)

        if map_button.draw():
            map()

        if potion_button.draw():
            potion = True

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        hero_health_bar.draw(hero.hp)
        hero_in_city.update()
        hero_in_city.draw()
        blacksmith.update()
        blacksmith.draw()
        merchant.update()
        merchant.draw()
        beggar.update()
        beggar.draw()
        dog.update()
        dog.draw()

        pos = pygame.mouse.get_pos()

        if merchant.rect.collidepoint(pos):
            if not cursor_hidden:
                pygame.mouse.set_visible(False)
                cursor_hidden = True  
            screen.blit(potion_plus_img, pos)
            if clicked:
                store()

        elif blacksmith.rect.collidepoint(pos):
            if not cursor_hidden:
                pygame.mouse.set_visible(False)
                cursor_hidden = True
            screen.blit(forge_img, pos)
            if clicked:
                forge()
        else:
            if cursor_hidden:
                pygame.mouse.set_visible(True)
                cursor_hidden = False

        for event in pygame.event.get():
            # Quiting the game
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


def cave():

    hero_turn = 0
    enemy_turn = 0
    enemies, health_bars = select_random_enemies(enemy_options2)
    global game_over, current_fighter, action_cooldown
    pygame.mouse.set_visible(True)
    clicked = False
    while True:

        basic("cave", hero)
        draw_panel(hero, enemies)
        # Reset actions variables
        attack = False
        potion = False
        target = None

        if run_button.draw():
            reset_battle(hero, enemies)
            city()

        if potion_button.draw():
            potion = True

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        hero_health_bar.draw(hero.hp)

        for i, enemy in enumerate(enemies):
            enemy.update()
            enemy.draw()
            health_bars[i].draw(enemy.hp)

        hero.update()
        hero.draw()

        # Draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        pos = pygame.mouse.get_pos()
        # Change mouse icon
        if enemies[0].hitbox.collidepoint(pos) or enemies[1].hitbox.collidepoint(pos):
            # Hide mouse
            pygame.mouse.set_visible(False)
            # Show sword as mouse cursor
            screen.blit(sword_img, pos)
        else:
            pygame.mouse.set_visible(True)

        # Target enemy
        for count, enemy in enumerate(enemies):
            if enemy.hitbox.collidepoint(pos):
                if clicked == True and enemy.alive == True:
                    attack = True
                    target = enemies[count]

        if hero_turn == 1:
            print("Hero Turn")

        if enemy_turn == 1:
            print("Enemy Turn")

        if game_over == 0:
            # Player action
            if hero.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        hero_turn += 1
                        # Look for player action

                        # Attack
                        if attack == True and target != None:
                            hero.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                            hero_turn = 0

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
                                hero_turn = 0
            else:
                game_over = -1

            # Enemy action
            for count, enemy in enumerate(enemies):
                if current_fighter == 2 + count:
                    if enemy.alive:
                        action_cooldown += 1
                        enemy_turn += 1
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
                                enemy_turn = 0
                            else:
                                # Attack
                                enemy.attack(hero)
                                current_fighter += 1
                                action_cooldown = 0
                                enemy_turn = 0
                    else:
                        current_fighter += 1

            # If all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        # Check if all enemies are dead
        alive_enemies = 0
        for enemy in enemies:
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
                reset_battle(hero, enemies)
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


def forest():

    hero_turn = 0
    enemy_turn = 0
    enemies, health_bars = select_random_enemies(enemy_options1)
    global game_over, current_fighter, action_cooldown
    pygame.mouse.set_visible(True)
    clicked = False
    while True:

        basic("forest", hero)
        draw_panel(hero, enemies)

        # Reset actions variables
        attack = False
        potion = False
        target = None

        if run_button.draw():
            reset_battle(hero, enemies)
            city()

        if potion_button.draw():
            potion = True

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        hero_health_bar.draw(hero.hp)

        for i, enemy in enumerate(enemies):
            enemy.update()
            enemy.draw()
            health_bars[i].draw(enemy.hp)

        # Draw fighters
        hero.update()
        hero.draw()

        # Draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        pos = pygame.mouse.get_pos()
        # Change mouse icon
        if enemies[0].hitbox.collidepoint(pos) or enemies[1].hitbox.collidepoint(pos):
            # Hide mouse
            pygame.mouse.set_visible(False)
            # Show sword as mouse cursor
            screen.blit(sword_img, pos)
        else:
            pygame.mouse.set_visible(True)

        # Target enemy
        for count, enemy in enumerate(enemies):
            if enemy.hitbox.collidepoint(pos):
                if clicked == True and enemy.alive == True:
                    attack = True
                    target = enemies[count]

        if hero_turn == 1:
            print("Hero Turn")
        if enemy_turn == 1:
            print("Enemy Turn")

        if game_over == 0:
            # Player action
            if hero.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1

                    if action_cooldown >= action_wait_time:
                        hero_turn += 1
                        # Look for player action

                        # Attack
                        if attack == True and target != None:

                            hero.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                            hero_turn = 0

                        # Potion
                        if potion == True:

                            if hero.potions > 0:
                                # Check heal beyond max helth
                                if hero.max_hp - hero.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = hero.max_hp - hero.hp
                                hero.hp += heal_amount
                                hero.potions -= 1
                                damage_text = DamageText(
                                    hero.rect.centerx,
                                    hero.rect.y,
                                    str(heal_amount),
                                    green,
                                )
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
                                hero_turn = 0
            else:
                game_over = -1

            # Enemy action
            for count, enemy in enumerate(enemies):
                if current_fighter == 2 + count:
                    if enemy.alive:
                        action_cooldown += 1
                        enemy_turn += 1
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
                                enemy_turn = 0
                            else:
                                # Attack
                                enemy.attack(hero)
                                current_fighter += 1
                                action_cooldown = 0
                                enemy_turn = 0
                    else:
                        current_fighter += 1

            # If all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        # Check if all enemies are dead
        alive_enemies = 0
        for enemy in enemies:
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
                reset_battle(hero, enemies)
                city()

        for event in pygame.event.get():
            # Quiting the game
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


def store():
    clicked = False
    pygame.mouse.set_visible(True)
    while True:

        basic("store", hero)

        if return_button.draw():
            city()

        if potion_button.draw():
            potion = True

        if potion_plus_button.draw():
            if hero.gold >= 5:
                hero.gold -= 5
                hero.potions += 1
                print("Potions:", hero.potions)

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        merchant_city.update()
        merchant_city.draw()
        hero_health_bar.draw(hero.hp)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


def forge():
    clicked = False
    pygame.mouse.set_visible(True)
    while True:

        basic("forge", hero)

        if return_button.draw():
            city()

        if potion_button.draw():
            potion = True

        if strength_plus_button.draw():
            if hero.gold >= 10:
                hero.gold -= 10
                hero.strength += 1
                print("Strength:", hero.strength)

        draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)

        blacksmith_city.update()
        blacksmith_city.draw()

        hero_health_bar.draw(hero.hp)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()


menu(selectHero)
