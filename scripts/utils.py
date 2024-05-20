# utils.py - Helper functions
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : utils.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import os
import pygame
from scripts.constants import *


def play_bgm(game, music_key="summer"):
    # Background music starts if the music being played is different from requested music
    if game.music_key != music_key:
        pygame.mixer.music.load(MUSIC[music_key]["file"])
        pygame.mixer.music.set_volume(
            MUSIC[music_key]["volume"] if not game.mute else 0
        )
        pygame.mixer.music.play(-1, 0.0)  # -1=infinite loop, 0.0=from the begining
        # Update music_key with curent music
        game.music_key = music_key


def set_volume(assets, mute=False):
    """Set volume of SFX and music. Mute if mute is True"""
    # SFX volume
    for asset_key in assets:
        assets[asset_key].set_volume(0 if mute else VOLUME[asset_key])
    # Music volume
    if mute:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.5)


def set_mute(game):
    """Mute / unmute music and sfx"""
    # Update mute
    game.mute = not game.mute
    set_volume(game.sfx, game.mute)


def resize_screen(game, step):
    """Resize the display window. Step can be any integer."""
    # Get a list of full size of user's desktops.
    # It's always a list of sizes for single or multiple desktops.
    desktop_size = pygame.display.get_desktop_sizes()[0]
    game.display_size_id = (game.display_size_id + step) % len(game.display_sizes)
    # while True:
    #     # If selected screen size is too large, this one cannot be used.
    #     game.display_size_id = (game.display_size_id + step) % len(game.display_sizes)
    #     if (
    #         game.display_sizes[game.display_size_id][0] <= desktop_size[0]
    #         and game.display_sizes[game.display_size_id][1] <= desktop_size[1]
    #     ):
    #         break

    if game.display_sizes[game.display_size_id][0] == desktop_size[0]:
        # Full screen
        game.screen = pygame.display.set_mode(
            game.display_sizes[game.display_size_id],
            pygame.FULLSCREEN,
        )
    else:
        # Not full screen? call twice.  When it's escaping from the full screen,
        # a known bug prevents the display rendered correctly.
        game.screen = pygame.display.set_mode(game.display_sizes[game.display_size_id])
        game.screen = pygame.display.set_mode(game.display_sizes[game.display_size_id])

    # The positioning will work only at the first time.
    # When this function is recalled, the position won't be changed.
    window_position = (
        (desktop_size[0] - game.display_sizes[game.display_size_id][0]) / 2,
        (desktop_size[1] - game.display_sizes[game.display_size_id][1]) / 2,
    )
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % window_position


def draw_text(
    surf,
    text,
    text_font,
    pos,
    text_col=COLORS["white"],
    align=("left", "top"),
    antialias=False,
    border_col=None,
    blink=(10, 0),
):
    """blink = (time to show in ms, time to hide in ms)
    Default (10, 0) = show constantly"""
    text_img = text_font.render(text, antialias, text_col)

    if align[0] == "center":
        x = pos[0] - text_img.get_width() / 2
    elif align[0] == "right":
        x = pos[0] - text_img.get_width()
    else:
        x = pos[0]
    if align[1] == "middle":
        y = pos[1] - text_img.get_height() / 2
    elif align[1] == "bottom":
        y = pos[1] - text_img.get_height()
    else:
        y = pos[1]

    total_cycle = blink[0] + blink[1]

    if blink and pygame.time.get_ticks() % total_cycle > blink[0]:
        pass
    else:
        if border_col:
            text_img_border = text_font.render(text, antialias, border_col)
            surf.blit(text_img_border, (x - 1, y))
            surf.blit(text_img_border, (x + 1, y))
            surf.blit(text_img_border, (x, y - 1))
            surf.blit(text_img_border, (x, y + 1))

        surf.blit(text_img, (x, y))

    # Return position for any use...
    return (x, y)


def load_score_highest(path):
    """Load a single line from the file (path)
    Possibly the file does not exist. Set as zero in the case."""
    try:
        f = open(path, "r")
        score_highest = int(f.readline())
        f.close()
    except:
        score_highest = 0
    return score_highest


def save_score_highest(path, score):
    """Save the highest score to the file (path)
    File may not exist, but that is fine because the directory 'data'
    always exist as it's a part of the program."""
    f = open(path, "w")
    f.write(f"{score}")
    f.close()


def load_image(path, trans_color=None, scale=1):
    if trans_color:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey(trans_color)
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    if scale != 1:
        img = pygame.transform.scale_by(img, scale)
    return img


def load_images(path, trans_color=None, scale=1):
    images = []
    files = [x for x in os.listdir(BASE_IMG_PATH + path) if x != ".DS_Store"]
    files = list(sorted(files))
    for img_name in files:
        images.append(load_image(path + "/" + img_name, trans_color, scale))
    return images
