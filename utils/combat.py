from pygame.locals import *
import pygame

from utils.loop import handle_events
from utils.variables import *

pygame.init()


# Reset battle to initial state
def reset_battle(hero, enemies):
    global game_over, current_fighter, action_cooldown

    hero.reset()
    for enemy in enemies:
        enemy.reset()
    current_fighter = 1
    action_cooldown = 0
    game_over = 0


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
    hero,
    hero_turn,
    target,
    damage_text_group,
    current_fighter,
    action_cooldown,
    attack,
    potion,
):
    game_over = 0
    if hero.alive == True:

        if current_fighter == 1:
            action_cooldown += 1

            if action_cooldown >= action_wait_time:
                hero_turn += 1
                if hero_turn == 1:
                    print("Hero Turn")
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
    return hero_turn, game_over, current_fighter, action_cooldown


def enemyTurn(
    enemy,
    enemy_turn,
    hero,
    damage_text_group,
    current_fighter,
    action_cooldown,
    count,
):

    if current_fighter == 2 + count:
        if enemy.alive:
            action_cooldown += 1
            enemy_turn += 1
            if enemy_turn == 1:
                print(f"Enemy {count+1} Turn")
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
    return enemy_turn, game_over, current_fighter, action_cooldown


def gameOver(hero, enemies, place, game_over):
    alive_enemies = 0
    for enemy in enemies:
        if enemy.alive == True:
            alive_enemies += 1
    if alive_enemies == 0:
        game_over = 1

    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            reset_battle(hero, enemies)
            place()
