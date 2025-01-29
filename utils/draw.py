import pygame

from utils.variables import *


pygame.init()


# # Draw Background
def draw_bg(place, size=None):
    background = pygame.image.load(
        f"assets/Background/background_{place}.png"
    ).convert_alpha()
    if size:
        background = pygame.transform.scale(background, size)
    screen.blit(background, (0, 0))


# Draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Draw Panel
def draw_panel(hero, enemies):
    screen.blit(panel_img, (0, screen_height - bottom_pannel))
    draw_text(
        f"{hero.name} HP: {hero.hp}", font, red, 100, screen_height - bottom_pannel + 10
    )

    if enemies != None:
        for count, enemy in enumerate(enemies):
            draw_text(
                f"{enemy.name} HP: {enemy.hp}",
                font,
                red,
                550,
                (screen_height - bottom_pannel + 10) + count * 60,
            )


# Draw gold coins
def draw_gold(hero):
    gold_icon = screen.blit(gold_img, (0, 0))
    gold_text = GoldText(32, 0, str(hero.gold), white)
    gold_text.draw()


# Gold Text
class GoldText(pygame.sprite.Sprite):

    def __init__(self, x, y, amount, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(amount, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)


# Draw Hero name and health bar
def draw_hero_hud(hero):
    draw_text(str(hero.potions), font, red, 150, screen_height - bottom_pannel + 70)
    hero.health_bar.draw(hero.hp)


# Draw and update a list of NPCs
def draw_update(npcs):
    if isinstance(npcs, list):
        for npc in npcs:
            npc.update()
            npc.draw()
    else:
        npcs.update()
        npcs.draw()


def handle_cursor(npc, image, cursor_hidden, clicked, action=None):
    if not cursor_hidden:
        pygame.mouse.set_visible(False)
        cursor_hidden = True
    screen.blit(image, pygame.mouse.get_pos())
    if clicked and action:
        action()


def draw_turn_indicator(name):
    turn_text = font.render(f"{name} Turn", True, white)
    screen.blit(turn_text, (screen_width // 2 - turn_text.get_width() // 2, 20))


def draw_mission_panel(missions):
    y_offset = 50  # screen_height - bottom_pannel - 35

    aux = missions

    mission_qtd = 3

    if len(aux) > mission_qtd:
        aux = aux[:mission_qtd]

    for mission in aux:
        status = (
            "Completed"
            if mission.completed
            else f"{mission.current_count}/{mission.objective_count}"
        )
        draw_text("Quest:", font, yellow, 625, 10)
        draw_text(f"{mission.name} - {status}", font, yellow, 550, y_offset)
        y_offset += 30
