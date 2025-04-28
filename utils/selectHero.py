import pygame

from utils.variables import *

from characters.fighter import Fighter

pygame.init()

hero_configs = [
    {
        "name": "Knight",
        "scale_factor": 3,
        "q_idle": 8,
        "q_hurt": 3,
        "q_death": 10,
        "q_attack": 8,
        "x": 200,
        "y": 260,
        "in_city_x": 280,
        "in_city_y": 300,
    },
    {
        "name": "Archer",
        "scale_factor": 2.8,
        "q_idle": 12,
        "q_hurt": 6,
        "q_death": 19,
        "q_attack": 15,
        "x": 200,
        "y": 160,
        "in_city_x": 280,
        "in_city_y": 230,
    },
    {
        "name": "Assassin",
        "scale_factor": 2.8,
        "q_idle": 8,
        "q_hurt": 6,
        "q_death": 12,
        "q_attack": 6,
        "x": 200,
        "y": 160,
        "in_city_x": 280,
        "in_city_y": 225,
    },
    {
        "name": "Monk",
        "scale_factor": 3,
        "q_idle": 6,
        "q_hurt": 6,
        "q_death": 18,
        "q_attack": 6,
        "x": 200,
        "y": 165,
        "in_city_x": 280,
        "in_city_y": 235,
    },
    {
        "name": "Priestess",
        "scale_factor": 3,
        "q_idle": 8,
        "q_hurt": 7,
        "q_death": 16,
        "q_attack": 7,
        "x": 200,
        "y": 150,
        "in_city_x": 280,
        "in_city_y": 220,
    },
    {
        "name": "Mauler",
        "scale_factor": 3,
        "q_idle": 8,
        "q_hurt": 6,
        "q_death": 15,
        "q_attack": 7,
        "x": 200,
        "y": 150,
        "in_city_x": 280,
        "in_city_y": 220,
    },
]


def selectHero(hero_op):
    global hero, hero_in_city

    print("Selecting Hero")

    config = hero_configs[hero_op]

    hero = Fighter(
        config["x"],
        config["y"],
        config["name"],
        max_hp=30,
        strength=10,
        potions=3,
        gold=5,
        scale_factor=config["scale_factor"],
        q_idle=config["q_idle"],
        q_hurt=config["q_hurt"],
        q_death=config["q_death"],
        q_attack=config["q_attack"],
    )

    hero_in_city = create_hero_in_city(hero, config)

    print(f"Heroi selected: {hero.name}")

    return hero, hero_in_city


def create_hero_in_city(hero, config):
    return Fighter(
        x=config["in_city_x"],
        y=config["in_city_y"],
        name=hero.name,
        scale_factor=2,
        q_idle=hero.q_idle,
    )


def handle_hero_selection():
    mouse_pos = pygame.mouse.get_pos()
    for i, button in enumerate(hero_buttons):
        if button.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (255, 0, 0), button.rect, 3)
        if button.draw():
            return i
    return None
