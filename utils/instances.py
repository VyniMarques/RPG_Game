import pygame

from characters.fighter import Fighter
from characters.npc import Npc
from utils.quest import Mission

pygame.init()


# ======== Object Instances ========

damage_text_group = pygame.sprite.Group()
misc_text_group = pygame.sprite.Group()

# ====== NPCs ======

# Blacksmith
blacksmith = Npc(650, 310, "Blacksmith", 4, 2.6)
blacksmith_city = Npc(340, 260, "Blacksmith", 4, 5)
# Merchant
merchant = Npc(390, 310, "Merchant", 4, 2.6)
merchant_city = Npc(510, 260, "Merchant", 4, 5)
# Dog
dog = Npc(550, 310, "Dog", 4, 2.6)
# Beggar
beggar = Npc(145, 315, "Beggar", 5, 2.6)

# ====== Enemy List ======

# Forest
enemy_options1 = [
    Fighter(0, 0, "Bandit", 10, 6, 1, 20, 3, 8, 3, 10, 8),
    Fighter(0, 0, "Bandit", 10, 6, 1, 20, 3, 8, 3, 10, 8),
]

# Cave
enemy_options2 = [
    Fighter(0, 0, "Goblin", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "Skeleton", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "FlyingEye", 20, 5, 0, 20, 2.4, 8, 4, 4, 8),
    Fighter(0, 0, "Mushroom", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "Goblin", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "Skeleton", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
    Fighter(0, 0, "FlyingEye", 20, 5, 0, 20, 2.4, 8, 4, 4, 8),
    Fighter(0, 0, "Mushroom", 20, 5, 0, 20, 2.4, 4, 4, 4, 8),
]
