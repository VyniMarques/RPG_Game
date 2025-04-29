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
    BattleState,
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
    pygame.mouse.set_visible(True)

    while True:
        draw_menu_screen()

        hero_op = handle_hero_selection()
        if hero_op is not None:
            hero, hero_in_city = selectHero(hero_op)
            pygame.time.delay(200)
            return hero, hero_in_city
        handle_events()
        pygame.display.update()


def map(hero, hero_in_city):
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
                    city(hero, hero_in_city)
                    break
                else:
                    combat(place, hero, hero_in_city)
                    break

        if potion_button.draw():
            potion = True

        draw_hero_hud(hero)

        clicked = handle_events()

        pygame.display.update()


def city(hero, hero_in_city):
    pygame.mouse.set_visible(True)
    cursor_hidden = False
    clicked = False
    click_released = True

    npcs = [hero_in_city, blacksmith, merchant, beggar, dog]

    while True:
        basic("city", hero)

        actions = {
            map_button: lambda: map(hero, hero_in_city),
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

        if not mouse_buttons[0]:
            click_released = True

        if not clicked and click_released:
            if quest_button.draw() and len(mission_manager.missions) < 3:
                print("Botão de missão clicado!")
                mission_manager.get_new_quest()
                print(f"Missões ativas: {[m.name for m in mission_manager.missions]}")
                clicked = True
                click_released = False

        if (
            any(m.completed for m in mission_manager.missions)
            and quest_complete_button.draw()
        ):
            mission_manager.complete_quest(hero)
            click_released = False

        # NPC mouse icon and click logic
        npc_actions = {
            merchant: (potion_plus_img, store),
            blacksmith: (forge_img, forge),
        }

        collided = False

        for npc, (img, action) in npc_actions.items():
            if npc.rect.collidepoint(pos):
                handle_cursor(npc, img, cursor_hidden, clicked, action)
                cursor_hidden = True
                collided = True

                if mouse_buttons[0] and click_released:
                    while pygame.mouse.get_pressed()[0]:
                        pygame.event.pump()
                    action()
                    clicked = True
                    click_released = False
                    break

        if not collided:
            pygame.mouse.set_visible(True)
            cursor_hidden = False

        clicked = handle_events()

        pygame.display.update()


def combat(place, hero, hero_in_city):
    pygame.mouse.set_visible(True)

    enemy_list = enemy_options1 if place == "forest" else enemy_options2
    enemies, health_bars = selectEnemies(enemy_list)

    hero_turn = 0
    enemy_turn = 0
    battle_state = BattleState()

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

        if battle_state.game_over == 0:
            if run_button.draw() and battle_state.current_fighter == 1:
                wait_for_mouse_release()
                reset_battle(hero, enemies, battle_state)
                city(hero, hero_in_city)
                break

            if battle_state.current_fighter == 1:
                draw_turn_indicator("Hero")
            else:
                current_enemy = enemies[battle_state.current_fighter - 2]
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

        # Change the mouse icon
        hide_mouse(pos, enemies)

        # Target enemy
        attack, target = getTarget(enemies, pos)

        if battle_state.game_over == 0:
            # Player Turn
            hero_turn, battle_state = playerTurn(
                hero,
                hero_turn,
                target,
                damage_text_group,
                battle_state,
                attack,
                potion,
            )

            # Enemies Turn
            for count, enemy in enumerate(enemies):
                enemy_turn, battle_state = enemyTurn(
                    enemy,
                    enemy_turn,
                    hero,
                    damage_text_group,
                    battle_state,
                    count,
                )
                mission_manager.check_quests(enemy)

            # If all fighters have had a turn then reset
            if battle_state.current_fighter > total_fighters:
                battle_state.current_fighter = 1

        # Check if game is over
        battle_state = gameOver(
            hero, enemies, lambda: city(hero, hero_in_city), battle_state
        )

        if battle_state.game_over:
            for enemy in enemies:
                enemy.counted_for_mission = False

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
            city(hero, hero_in_city)
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
            city(hero, hero_in_city)

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


if __name__ == "__main__":
    hero, hero_in_city = menu()
    city(hero, hero_in_city)
