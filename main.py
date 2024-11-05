from pygame.locals import *
import pygame

from utils.button import Button
from utils.combat import reset_battle
from utils.draw import draw_bg, draw_panel, draw_text, DamageText
from utils.loop import handle_events
from utils.loop import basic
from utils.selectEnemies import selectEnemies
from utils.selectHero import selectHero

from characters.fighter import Fighter
from characters.npc import Npc

pygame.init()

# ======== Game Window ========
bottom_pannel = 150
screen_width = 800
screen_height = 400 + bottom_pannel

screen = pygame.display.set_mode((screen_width, screen_height))
programIcon = pygame.image.load("assets/Icons/espadas.png").convert_alpha()

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
panel_img = pygame.image.load("assets/Icons/panel.png").convert_alpha()

# Sword
sword_img = pygame.image.load("assets/Icons/sword.png").convert_alpha()

# Potion
potion_img = pygame.image.load("assets/Icons/potion.png").convert_alpha()

# City
city_img = pygame.image.load("assets/Icons/city.png").convert_alpha()

# Forest
forest_img = pygame.image.load("assets/Icons/forest.png").convert_alpha()

# Map
map_img = pygame.image.load("assets/Icons/map.png").convert_alpha()

# Cave
cave_img = pygame.image.load("assets/Icons/cave.png").convert_alpha()

# Potion Store
potion_plus_img = pygame.image.load("assets/Icons/potion_plus.png").convert_alpha()

# Potion buy
potion_plus_b_img = pygame.image.load("assets/Icons/potion_plus2.png").convert_alpha()

# Forge
forge_img = pygame.image.load("assets/Icons/forge.png").convert_alpha()

# Return
return_img = pygame.image.load("assets/Icons/return.png").convert_alpha()

# Run Away
run_img = pygame.image.load("assets/Icons/run.png").convert_alpha()

# Strength
strength_img = pygame.image.load("assets/Icons/strength_plus.png").convert_alpha()

# Restart
restart_img = pygame.image.load("assets/Icons/restart.png").convert_alpha()

# Victory
victory_img = pygame.image.load("assets/Icons/victory.png").convert_alpha()

# Defeat
defeat_img = pygame.image.load("assets/Icons/defeat.png").convert_alpha()

# ======== Load Character Images ========
knight_img = pygame.image.load("assets/Characters/knight.png").convert_alpha()

archer_img = pygame.image.load("assets/Characters/archer.png").convert_alpha()

assasin_img = pygame.image.load("assets/Characters/assasin.png").convert_alpha()

monk_img = pygame.image.load("assets/Characters/monk.png").convert_alpha()

priestess_img = pygame.image.load("assets/Characters/priestess.png").convert_alpha()

mauler_img = pygame.image.load("assets/Characters/mauler.png").convert_alpha()


# ======== Buttons ========
potion_button = Button(
    screen, 100, screen_height - bottom_pannel + 70, potion_img, 64, 64
)
potion_plus_button = Button(
    screen, 600, screen_height - bottom_pannel + 70, potion_plus_b_img, 64, 64
)
strength_plus_button = Button(
    screen, 600, screen_height - bottom_pannel + 70, strength_img, 64, 64
)
restart_button = Button(screen, 330, 120, restart_img, 120, 30)

city_button = Button(screen, 30, 100, city_img, 64, 64)

cave_button = Button(screen, 100, 100, cave_img, 64, 64)

forest_button = Button(screen, 170, 100, forest_img, 64, 64)

map_button = Button(screen, 0, 30, map_img, 64, 64)

return_button = Button(screen, 0, 80, return_img, 64, 64)

run_button = Button(screen, 0, 90, run_img, 64, 64)

# ======== Character selectors ========
knight_button = Button(screen, 100, 50, knight_img, 165, 165)

archer_button = Button(screen, 100, 200, archer_img, 165, 165)

assasin_button = Button(screen, 330, 50, assasin_img, 165, 165)

monk_button = Button(screen, 315, 215, monk_img, 170, 170)

priestess_button = Button(screen, 550, 50, priestess_img, 165, 165)

mauler_button = Button(screen, 550, 200, mauler_img, 165, 165)

# ======== Object Instances ========

damage_text_group = pygame.sprite.Group()

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

# ======== Loops ========


def menu():
    global hero, hero_in_city, hero_health_bar
    pygame.mouse.set_visible(True)
    chosen = False

    while True:

        screen.fill(black)
        pygame.mouse.set_visible(True)
        draw_bg("map")
        screen.blit(panel_img, (0, screen_height - bottom_pannel))
        clock.tick(fps)

        draw_text("RPG Game", font, black, 350, 20)

        if knight_button.draw():
            hero_op = 0
            chosen = True

        if archer_button.draw():
            hero_op = 1
            chosen = True

        if assasin_button.draw():
            hero_op = 2
            chosen = True

        if monk_button.draw():
            hero_op = 3
            chosen = True

        if priestess_button.draw():
            hero_op = 4
            chosen = True

        if mauler_button.draw():
            hero_op = 5
            chosen = True

        if chosen:
            hero, hero_in_city, hero_health_bar = selectHero(hero_op)
            pygame.time.delay(200)
            city()

        clicked = handle_events()

        pygame.display.update()


def map():
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

        clicked = handle_events()

        pygame.display.update()


def city():
    pygame.mouse.set_visible(True)
    cursor_hidden = False
    clicked = False
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

        clicked = handle_events()

        pygame.display.update()


def cave():
    global game_over, current_fighter, action_cooldown
    pygame.mouse.set_visible(True)

    enemies, health_bars = selectEnemies(enemy_options2)
    hero_turn = 0
    enemy_turn = 0

    game_over = 0
    while True:

        basic("cave", hero)
        draw_panel(hero, enemies)
        # Reset actions variables
        attack = False
        potion = False
        target = None

        if run_button.draw() and game_over == 0:
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

        clicked = handle_events()

        pygame.display.update()


def forest():
    global game_over, current_fighter, action_cooldown
    pygame.mouse.set_visible(True)

    enemies, health_bars = selectEnemies(enemy_options1)
    hero_turn = 0
    enemy_turn = 0

    game_over = 0

    while True:

        basic("forest", hero)
        draw_panel(hero, enemies)

        # Reset actions variables
        attack = False
        potion = False
        target = None

        if run_button.draw() and game_over == 0:
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

        clicked = handle_events()

        pygame.display.update()


def store():
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

        clicked = handle_events()

        pygame.display.update()


def forge():
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

        clicked = handle_events()

        pygame.display.update()


menu()
