import pygame
import random

from pygame.locals import *

from utils.combat import (
    reset_battle,
    hide_mouse,
    getTarget,
    playerTurn,
    enemyTurn,
    gameOver,
)

from utils.draw import (
    draw_bg,
    draw_panel,
    draw_text,
    draw_update,
    draw_hero_hud,
    handle_cursor,
    draw_turn_indicator,
    draw_mission_panel,
    draw_menu_screen,
)
from utils.non_combat import buy_upgrade, message, text_update
from utils.selectEnemies import selectEnemies
from utils.selectHero import selectHero, handle_hero_selection
from utils.loop import handle_events, basic
from utils.variables import *
from utils.instances import *
from utils.quest import MissionManager


pygame.init()

mission_manager = MissionManager()


def menu():
    global hero, hero_in_city
    pygame.mouse.set_visible(True)

    while True:
        draw_menu_screen()

        hero_op = handle_hero_selection()
        if hero_op is not None:
            hero, hero_in_city = selectHero(hero_op)
            pygame.time.delay(200)
            city()
            break

        handle_events()
        pygame.display.update()


def map():
    pygame.mouse.set_visible(True)
    clicked = False

    while True:

        basic("map", hero)

        actions = {
            forest_button: "forest",
            city_button: "city",
            cave_button: "cave",
        }

        for button, place in actions.items():
            if button.draw():
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
                if place == "city":
                    city()
                    break
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

        draw_mission_panel(mission_manager.missions)

        pos = pygame.mouse.get_pos()

        mouse_buttons = pygame.mouse.get_pressed()

        if quest_button.draw() and len(mission_manager.missions) < 3:
            print("Botão de missão clicado!")
            mission_manager.get_new_quest()
            print(f"Missões ativas: {[m.name for m in mission_manager.missions]}")

        if (
            any(m.completed for m in mission_manager.missions)
            and quest_complete_button.draw()
        ):
            mission_manager.complete_quest(hero)

        cursor_hidden = False

        npc_actions = {
            merchant: (potion_plus_img, store),
            blacksmith: (forge_img, forge),
        }

        for npc, (img, action) in npc_actions.items():
            if npc.rect.collidepoint(pos):
                handle_cursor(npc, img, cursor_hidden, False, action)
                cursor_hidden = True

                if mouse_buttons[0]:
                    while pygame.mouse.get_pressed()[0]:
                        pygame.event.pump()
                    action()
                    break

        if not cursor_hidden:
            pygame.mouse.set_visible(True)

        clicked = handle_events()

        pygame.display.update()


def combat(place):
    # Globals to control battle state
    global game_over, current_fighter, action_cooldown

    pygame.mouse.set_visible(True)

    # Initial Setup
    enemy_list = enemy_options1 if place == "forest" else enemy_options2
    enemies, health_bars = selectEnemies(enemy_list)

    hero_turn = 0
    enemy_turn = 0
    game_over = 0

    def wait_for_mouse_release():
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()

    while True:
        basic(place, hero)
        draw_panel(hero, enemies)

        # Reset actions variables
        attack = False
        potion = False
        target = None

        pos = pygame.mouse.get_pos()

        # Run is only available on hero turn
        if game_over == 0:
            if run_button.draw() and current_fighter == 1:
                wait_for_mouse_release()
                reset_battle(hero, enemies)
                city()
                break

            if current_fighter == 1:
                draw_turn_indicator("Hero")
            else:
                current_enemy = enemies[current_fighter - 2]
                draw_turn_indicator(current_enemy.name)

            draw_mission_panel(mission_manager.missions)

        if potion_button.draw():
            potion = True

        draw_hero_hud(hero)

        for i, enemy in enumerate(enemies):
            draw_update(enemy)
            health_bars[i].draw(enemy.hp)

        draw_update(hero)

        # Draw damage text
        text_update(damage_text_group, screen)

        # Change mouse icon
        hide_mouse(pos, enemies)

        # Target enemy
        attack, target = getTarget(enemies, pos)

        if game_over == 0:
            # Player
            hero_turn, game_over, current_fighter, action_cooldown = playerTurn(
                hero,
                hero_turn,
                target,
                damage_text_group,
                current_fighter,
                action_cooldown,
                attack,
                potion,
            )

            # Enemy
            for count, enemy in enumerate(enemies):
                enemy_turn, game_over, current_fighter, action_cooldown = enemyTurn(
                    enemy,
                    enemy_turn,
                    hero,
                    damage_text_group,
                    current_fighter,
                    action_cooldown,
                    count,
                )
                mission_manager.check_quests(enemy)

            # If all fighters have had a turn then reset
            if current_fighter > total_fighters:
                current_fighter = 1

        # Check if game is over
        game_over, current_fighter = gameOver(
            hero, enemies, city, game_over, current_fighter
        )

        if game_over:
            # Reset the counted for mission
            for enemy in enemies:
                enemy.counted_for_mission = False

        # Eventos gerais
        clicked = handle_events()

        # Atualiza tela
        pygame.display.update()


def store():
    pygame.mouse.set_visible(True)

    message(merchant_city, "Potions only 5 gold", white, misc_text_group)

    clicked = False

    while True:

        basic("store", hero)

        if return_button.draw():
            while pygame.mouse.get_pressed()[0]:  # Aguarda soltar clique
                pygame.event.pump()
            city()
            return

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

    if random.randint(1, 2) == 1:
        msg = "Improve your armor for 15 gold"
    else:
        msg = "Sharpen your weapon for 10 gold"
    message(blacksmith_city, msg, white, misc_text_group)

    clicked = False

    while True:

        basic("forge", hero)

        if return_button.draw():
            while pygame.mouse.get_pressed()[0]:  # Aguarda soltar clique
                pygame.event.pump()
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

            def increase_max_hp():
                hero.max_hp += 5
                hero.hp = hero.max_hp

            buy_upgrade(
                cost=15,
                stat_increase=increase_max_hp,
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
