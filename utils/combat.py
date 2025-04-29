from pygame.locals import *
import pygame

from utils.loop import handle_events
from utils.variables import *

pygame.init()


class BattleState:
    def __init__(self):
        self.game_over = 0
        self.current_fighter = 1
        self.action_cooldown = 0


# Reset battle to initial state
def reset_battle(hero, enemies, battle_state):
    hero.reset()
    for enemy in enemies:
        enemy.reset()
    battle_state.current_fighter = 1
    battle_state.action_cooldown = 0
    battle_state.game_over = 0


# Class DamageText for damage an heal
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(damage), True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()


# Hides the mouse icon when hovering over a living enemy
def hide_mouse(pos, enemies):
    if (
        enemies[0].hitbox.collidepoint(pos)
        and enemies[0].alive == True
        or enemies[1].hitbox.collidepoint(pos)
        and enemies[1].alive == True
    ):
        pygame.mouse.set_visible(False)
        screen.blit(sword_img, pos)
    else:
        pygame.mouse.set_visible(True)


def getTarget(enemies, pos):
    attack = False
    target = None
    clicked = handle_events()
    for count, enemy in enumerate(enemies):
        if enemy.hitbox.collidepoint(pos):
            if clicked == True and enemy.alive == True:
                attack = True
                target = enemies[count]

    return attack, target


def playerTurn(
    hero, hero_turn, target, damage_text_group, battle_state, attack, potion
):
    if hero.alive:
        if battle_state.current_fighter == 1:
            battle_state.action_cooldown += 1
            if battle_state.action_cooldown >= action_wait_time:
                hero_turn += 1
                if hero_turn == 1:
                    print("Hero Turn")

                if attack and target is not None:
                    hero.attack(target, damage_text_group)
                    battle_state.current_fighter += 1
                    battle_state.action_cooldown = 0
                    hero_turn = 0

                if potion:
                    if hero.potions > 0:
                        heal_amount = min(potion_effect, hero.max_hp - hero.hp)
                        hero.hp += heal_amount
                        hero.potions -= 1
                        damage_text = DamageText(
                            hero.hitbox.centerx, hero.hitbox.y, str(heal_amount), green
                        )
                        damage_text_group.add(damage_text)
                        battle_state.current_fighter += 1
                        battle_state.action_cooldown = 0
                        hero_turn = 0
    else:
        battle_state.game_over = -1

    return hero_turn, battle_state


def enemyTurn(enemy, enemy_turn, hero, damage_text_group, battle_state, count):
    if battle_state.current_fighter == 2 + count and hero.alive:
        if enemy.alive:
            battle_state.action_cooldown += 1
            enemy_turn += 1
            if enemy_turn == 1:
                print(f"Enemy {count + 1} Turn")

            if battle_state.action_cooldown >= action_wait_time:
                if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potions > 0:
                    heal_amount = min(potion_effect, enemy.max_hp - enemy.hp)
                    enemy.hp += heal_amount
                    damage_text = DamageText(
                        enemy.hitbox.centerx, enemy.hitbox.y, str(heal_amount), green
                    )
                    damage_text_group.add(damage_text)
                    enemy.potions -= 1
                else:
                    enemy.attack(hero, damage_text_group)

                battle_state.current_fighter += 1
                battle_state.action_cooldown = 0
                enemy_turn = 0
        else:
            battle_state.current_fighter += 1

    return enemy_turn, battle_state


def gameOver(hero, enemies, place, battle_state):
    alive_enemies = sum(enemy.alive for enemy in enemies)

    if alive_enemies == 0:
        battle_state.game_over = 1

    if not hero.alive:
        battle_state.game_over = -1

    if battle_state.game_over != 0:
        if battle_state.game_over == 1:
            screen.blit(victory_img, (250, 50))
        elif battle_state.game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            reset_battle(hero, enemies, battle_state)
            place()
        battle_state.current_fighter = 1

    return battle_state
