import pygame
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
)
from utils.non_combat import buy_upgrade, message, text_update
from utils.selectEnemies import selectEnemies
from utils.selectHero import selectHero
from utils.loop import handle_events, basic
from utils.variables import *
from utils.instances import *
from utils.quest import MissionManager

pygame.init()
mission_manager = MissionManager()


def menu():
    global hero, hero_in_city
    pygame.mouse.set_visible(True)
    chosen = False

    while True:

        screen.fill(black)
        draw_bg("map", (800, 550))
        clock.tick(fps)

        draw_text("RPG Game", title, black, 350, 20)
        draw_text("Select your hero:", font, black, 325, 65)

        buttons = [
            knight_button,
            archer_button,
            assasin_button,
            monk_button,
            priestess_button,
            mauler_button,
        ]

        mouse_pos = pygame.mouse.get_pos()

        for i, button in enumerate(buttons):
            if button.rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 0, 0), button.rect, 3)
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
            city_button: "city",
            cave_button: "cave",
        }

        for button, place in actions.items():
            if button.draw():
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
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

    click_released = True

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

        if not mouse_buttons[0]:  # Botão esquerdo solto
            click_released = True

        if not clicked and click_released and quest_button.draw():
            print("Botão de missão clicado!")
            if len(mission_manager.missions) < 3:
                mission_manager.get_new_quest()
            print(f"Missões ativas: {[m.name for m in mission_manager.missions]}")
            clicked = True  # Marcamos que o clique já foi usado
            click_released = False

        if any(m.completed for m in mission_manager.missions):
            if quest_complete_button.draw():
                mission_manager.complete_quest(hero)
                clicked = True
                click_released = False

        if merchant.rect.collidepoint(pos):
            handle_cursor(merchant, potion_plus_img, cursor_hidden, clicked, store)
        elif blacksmith.rect.collidepoint(pos):
            handle_cursor(blacksmith, forge_img, cursor_hidden, clicked, forge)
        else:
            pygame.mouse.set_visible(True)
            cursor_hidden = False

        clicked = handle_events()

        pygame.display.update()


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

        pos = pygame.mouse.get_pos()
        if game_over == 0:
            if run_button.draw() and current_fighter == 1 and game_over == 0:
                while pygame.mouse.get_pressed()[0]:
                    pygame.event.pump()
                reset_battle(hero, enemies)
                city()

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
            # Player action
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

            # Enemy action
            for count, enemy in enumerate(enemies):
                enemy_turn, game_over, current_fighter, action_cooldown = enemyTurn(
                    enemy,
                    enemy_turn,
                    hero,
                    damage_text_group,
                    current_fighter,
                    action_cooldown,
                    count,
                    # missions,
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
            for enemy in enemies:
                enemy.counted_for_mission = (
                    False  # Permite que novos combates contem para as missões
                )

        clicked = handle_events()

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
