def reset_battle(hero, enemies):
    global game_over, current_fighter, action_cooldown

    hero.reset()
    for enemy in enemies:
        enemy.reset()
    current_fighter = 1
    action_cooldown = 0
    game_over = 0
    print("Game_over", game_over)

    