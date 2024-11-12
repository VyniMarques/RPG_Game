import pygame

from utils.variables import *

from characters.fighter import Fighter

pygame.init()


def selectHero(hero_op):
    global hero, hero_in_city

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

    return hero, hero_in_city
