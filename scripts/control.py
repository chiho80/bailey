# control.py - Key detector
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : control.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import pygame
from scripts.utils import resize_screen, set_mute
from scripts.constants import LEVELS


def check_keyboard_input(game):
    """Check key inputs and set the parameters accordingly
    Return quit_game"""
    quit_game = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.movement[0] = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.movement[1] = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if game.player.jump():
                    game.sfx["jump"].play()
            if event.key == pygame.K_x or event.key == pygame.K_l:
                # Dashing is not allowed for a while if hit.
                if game.player.action != "hit":
                    game.player.dash()
            if event.key == pygame.K_LSHIFT:
                game.running = True
            # If any key has been pressed before the game is started,
            # it triggers the game start!
            if not game.is_game_started:
                game.load_level(game.level)
            game.is_game_started = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                game.movement[0] = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                game.movement[1] = False
            if event.key == pygame.K_LSHIFT:
                game.running = False
            if event.key == pygame.K_m:
                set_mute(game)
            if (
                event.key == pygame.K_p or event.key == pygame.K_ESCAPE
            ) and not game.paused:
                game.time_right_before_pause = pygame.time.get_ticks()  # ms
                game.paused = True
                # When paused, stop moving.
                game.movement[0] = False
                game.movement[1] = False
            if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                resize_screen(game, 1)
                # When resized, stop moving.
                game.movement[0] = False
                game.movement[1] = False
            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                resize_screen(game, -1)
                # When resized, stop moving.
                game.movement[0] = False
                game.movement[1] = False
            if event.key == pygame.K_7:
                game.level = max(game.level - 1, 1)
                game.load_level(game.level)
            if event.key == pygame.K_8:
                game.level = min(game.level + 1, max([int(key) for key in LEVELS]))
                game.load_level(game.level)
    return quit_game
