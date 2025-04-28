import pygame
import random

from utils.healthBar import HealthBar
from utils.combat import DamageText
from utils.variables import *

pygame.init()

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

        self.q_idle = q_idle
        self.q_hurt = q_hurt
        self.q_death = q_death
        self.q_attack = q_attack

        self.counted_for_mission = False

        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect(center=(x, y))

        if self.name == "Knight":
            self.hitbox = pygame.Rect(self.rect.x - 40, self.rect.y - 40, 120, 140)
        else:
            self.hitbox = pygame.Rect(self.rect.x - 35, self.rect.y + 60, 120, 140)

        # ======== Health bar ========
        self.health_bar = HealthBar(
            100, SCREEN_HEIGHT - BOTTOM_PANEL + 40, self.hp, self.max_hp
        )

        # Load idle images
        temp_list = []
        for i in range(q_idle):
            img = pygame.image.load(f"assets/{self.name}/Idle/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load attack images
        temp_list = []
        for i in range(q_attack):
            img = pygame.image.load(f"assets/{self.name}/Attack/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load hurt images
        temp_list = []
        for i in range(q_hurt):
            img = pygame.image.load(f"assets/{self.name}/Hurt/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale_factor, img.get_height() * scale_factor)
            )
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Load death images
        temp_list = []
        for i in range(q_death):
            img = pygame.image.load(f"assets/{self.name}/Death/{i}.png")
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
    def attack(self, target, damage_text_group):

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
            target.dropGold(self)

        damage_text = DamageText(
            target.hitbox.centerx, target.hitbox.y, str(damage), red
        )
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
        print(f"{self.name} died")

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
        hero.gold += amount
        
        # Gold Droped
        print(f"Gold Dropped = {amount}\nGold Remaining = {self.gold}")
