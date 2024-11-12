from pygame.locals import *
import pygame

from utils.combat import reset_battle, hide_mouse, DamageText
from utils.non_combat import buy_upgrade, message, text_update
from utils.draw import (
    draw_bg,
    draw_panel,
    draw_text,
    draw_update,
    draw_hero_hud,
    handle_cursor,
)
from utils.loop import handle_events
from utils.loop import basic
from utils.selectEnemies import selectEnemies
from utils.selectHero import selectHero
from utils.variables import *
from utils.instances import *

pygame.init()


def menu():
    global hero, hero_in_city
    pygame.mouse.set_visible(True)
    chosen = False

    while True:

        screen.fill(black)
        pygame.mouse.set_visible(True)
        draw_bg("map")
        screen.blit(panel_img, (0, screen_height - bottom_pannel))
        clock.tick(fps)

        draw_text("RPG Game", font, black, 350, 20)

        buttons = [
            knight_button,
            archer_button,
            assasin_button,
            monk_button,
            priestess_button,
            mauler_button,
        ]

        for i, button in enumerate(buttons):
            if button.draw():
                hero_op = i
                chosen = True
                break

        if chosen:
            hero, hero_in_city = selectHero(hero_op)
            pygame.time.delay(200)
            city()

        clicked = handle_events()

        pygame.display.update()


def map():
    pygame.mouse.set_visible(True)

    while True:

        basic("map", hero)

        actions = {
            forest_button: "forest",
            city_button: city,
            cave_button: "cave",
        }

        for button, place in actions.items():
            if button.draw():
                if place == "city":
                    city()
                else:
                    combat(place)
                break

        if potion_button.draw():
            potion = True

        draw_hero_hud(hero)

        clicked = handle_events()

        pygame.display.update()


def city():
    pygame.mouse.set_visible(True)
    cursor_hidden = False
    clicked = False

    npcs = [hero_in_city, blacksmith, merchant, beggar, dog]

    while True:
        basic("city", hero)

        actions = {
            map_button: map,
        }

        for button, action in actions.items():
            if button.draw():
                action()
                break

        if potion_button.draw():
            potion = True

        draw_hero_hud(hero)
        draw_update(npcs)

        pos = pygame.mouse.get_pos()

        if merchant.rect.collidepoint(pos):
            handle_cursor(merchant, potion_plus_img, cursor_hidden, clicked, store)
        elif blacksmith.rect.collidepoint(pos):
            handle_cursor(blacksmith, forge_img, cursor_hidden, clicked, forge)
        else:
            pygame.mouse.set_visible(True)
            cursor_hidden = False

        clicked = handle_events()

        pygame.display.update()

#from utils.combat import

def combat(place):
    global game_over, current_fighter, action_cooldown
    pygame.mouse.set_visible(True)

    if place == "forest":
        list = enemy_options1
    elif place == "cave":
        list = enemy_options2

    enemies, health_bars = selectEnemies(list)

    hero_turn = 0
    enemy_turn = 0
    game_over = 0

    while True:

        basic(place, hero)
        draw_panel(hero, enemies)

        # Reset actions variables
        attack = False
        potion = False
        target = None

        if game_over == 0:
            if run_button.draw() and current_fighter == 1:
                reset_battle(hero, enemies)
                city()

        if potion_button.draw():
            potion = True

        draw_hero_hud(hero)

        for i, enemy in enumerate(enemies):
            draw_update(enemy)
            health_bars[i].draw(enemy.hp)

        draw_update(hero)

        # Draw damage text
        text_update(damage_text_group, screen)

        pos = pygame.mouse.get_pos()

        # Change mouse icon
        hide_mouse(pos, enemies)

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

                            hero.attack(target, damage_text_group)
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
                                    hero.hitbox.centerx,
                                    hero.hitbox.y,
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
                                    enemy.hitbox.centerx,
                                    enemy.hitbox.y,
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
                                enemy.attack(hero, damage_text_group)
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

    message(merchant_city, "Potions only 5 gold", white, misc_text_group)

    while True:

        basic("store", hero)

        if return_button.draw():
            city()

        if potion_button.draw():

            potion = True

        if potion_plus_button.draw():
            buy_upgrade(
                cost=5,
                stat_increase=lambda: setattr(hero, "potions", hero.potions + 1),
                stat_name="potions",
                hero=hero,
                max=9,
                npc=merchant_city,
                group=misc_text_group,
            )

        text_update(misc_text_group, screen)

        draw_hero_hud(hero)

        draw_update(merchant_city)

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
            buy_upgrade(
                cost=10,
                stat_increase=lambda: setattr(hero, "strength", hero.strength + 1),
                stat_name="strength",
                hero=hero,
                max=15,
                npc=blacksmith_city,
                group=misc_text_group,
            )

        if defense_plus_button.draw():
            buy_upgrade(
                cost=15,
                stat_increase=lambda: setattr(hero, "max_hp", hero.max_hp + 5),
                stat_name="max_hp",
                hero=hero,
                max=50,
                npc=blacksmith_city,
                group=misc_text_group,
            )

        text_update(misc_text_group, screen)

        draw_hero_hud(hero)

        draw_update(blacksmith_city)

        clicked = handle_events()

        pygame.display.update()


menu()
