# banner.py - Functions to display screen covering banners
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : banner.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import pygame
from scripts.utils import draw_text
from scripts.constants import COLORS


def display_intro(game):
    width = game.display.get_width()
    height = game.display.get_height()
    game.display.blit(
        game.assets["intro"],
        (
            width / 2 - game.assets["intro"].get_width() / 2,
            height / 2 - game.assets["intro"].get_height() / 2 - 30,
        ),
    )
    (_, y) = draw_text(
        game.display,
        "PRESS ANY KEY TO START",
        game.font["text_size8"],
        (
            width / 2,
            height / 2 + 45,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
        blink=(500, 500),
    )
    (_, y) = draw_text(
        game.display,
        "Developer Bailey's Dad",
        game.font["text_size5"],
        (
            width / 2,
            y + 35,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    (_, y) = draw_text(
        game.display,
        "Ground Tile images from grafxkid.itch.io, House images from twitter@Vryell",
        game.font["text_size5"],
        (
            width / 2,
            y + 8,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    (_, y) = draw_text(
        game.display,
        "Original squirrel sprites from moose-stache.itch.io, cat sprites from craftix.net",
        game.font["text_size5"],
        (
            width / 2,
            y + 8,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    (_, y) = draw_text(
        game.display,
        "SFX from pixabay.com, mixkit.co",
        game.font["text_size5"],
        (
            width / 2,
            y + 8,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    (_, y) = draw_text(
        game.display,
        "Background music from PlayOnLoop.com",
        game.font["text_size5"],
        (
            width / 2,
            y + 8,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    draw_text(
        game.display,
        "Music Licensed under Creative Commons by Attribution 4.0",
        game.font["text_size5"],
        (
            width / 2,
            y + 8,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )


def display_gameover(game):
    width = game.display.get_width()
    height = game.display.get_height()
    (_, y) = draw_text(
        game.display,
        "GAME OVER",
        game.font["text_size22"],
        (
            width / 2,
            height / 2 - 30,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"SCORE {'.'*(10-len(str(game.score)))} {game.score}",
        game.font["text_size8"],
        (
            width / 2,
            y + 45,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"HIGHEST {'.'*(10-len(str(game.score_highest)))} {game.score_highest}  ",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"STAGE {'.'*(10-len(str(game.level)))} {game.level}",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        "PRESS Y TO START A NEW GAME",
        game.font["text_size8"],
        (
            width / 2,
            y + 30,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        "OR PRESS N/Q TO QUIT",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )


def display_finale(game):
    width = game.display.get_width()
    height = game.display.get_height()
    (_, y) = draw_text(
        game.display,
        "CONGRATULATIONS",
        game.font["text_size22"],
        (
            width / 2,
            height / 2 - 30,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"SCORE {'.'*(10-len(str(game.score)))} {game.score}",
        game.font["text_size8"],
        (
            width / 2,
            y + 45,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"HIGHEST {'.'*(10-len(str(game.score_highest)))} {game.score_highest}  ",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        f"STAGE {'.'*(10-len(str(game.level)))} {game.level}",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        "PRESS Y TO START A NEW GAME",
        game.font["text_size8"],
        (
            width / 2,
            y + 30,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )
    (_, y) = draw_text(
        game.display,
        "OR PRESS N/Q TO QUIT",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
    )


def display_paused(game):
    width = game.display.get_width()
    height = game.display.get_height()
    pygame.draw.rect(game.display, (0, 0, 0, 180), pygame.Rect(0, 0, width, height))
    (_, y) = draw_text(
        game.display,
        "PAUSED",
        game.font["text_size14"],
        (
            width / 2,
            height / 2 - 90,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
        border_col=COLORS["black"],
    )
    (_, y) = draw_text(
        game.display,
        "PRESS ANY KEY TO CONTINUE",
        game.font["text_size8"],
        (
            width / 2,
            y + 30,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "OR PRESS Q TO QUIT",
        game.font["text_size8"],
        (
            width / 2,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
        border_col=COLORS["black"],
    )

    (x, y) = draw_text(
        game.display,
        "     LEFT OR A - MOVE TO THE LEFT   ",
        game.font["text_size8"],
        (
            width / 2,
            y + 42,
        ),
        text_col=COLORS["white"],
        align=("center", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "    RIGHT OR D - MOVE TO THE RIGHT",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "       UP OR W - JUMP",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        " LSHIFT + LEFT - RUN TO THE LEFT",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "LSHIFT + RIGHT - RUN TO THE RIGHT",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "        X OR L - DASH AND KILL ENEMY",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "      ESC OR P - PAUSE",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    (x, y) = draw_text(
        game.display,
        "             M - MUTE OR UNMUTE",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )
    draw_text(
        game.display,
        " PLUS OR MINUS - ADJUST DISPLAY SIZE",
        game.font["text_size8"],
        (
            x,
            y + 17,
        ),
        text_col=COLORS["white"],
        align=("left", "middle"),
        border_col=COLORS["black"],
    )


def display_level_cleared(game):
    width = game.display.get_width()
    height = game.display.get_height()
    draw_text(
        game.display,
        "STAGE CLEARED",
        game.font["text_size8"],
        (
            width / 2,
            height / 2 - 80,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
    draw_text(
        game.display,
        "MOVING TO THE NEXT STAGE",
        game.font["text_size8"],
        (
            width / 2,
            height / 2 - 60,
        ),
        text_col=COLORS["white"],
        align=("center", "top"),
        border_col=COLORS["black"],
    )
