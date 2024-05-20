# constants.py - Global constants
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : constants.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.


import pygame

# The first number of lives
# If it's 4, a very first player + 3 more lives, total 4. 3 heads will be displayed
FIRST_LIVES = 4

# Additional time to be added when player died
EXTRA_TIME_AFTER_DEAD = 15000  # ms

# Camera tracking speed. The smaller the faster.
CAMERA_SPEED = 10

# Frame rate - lower the better performance, higher for smoother motion
FRAME_RATE = 60

# Fireball spawning rate. Increase for more fireballs.
FIREBALL_PROB = 0.002

# Velocity of objcets
VELOCITY = {
    "entity_falling_max": 7,
    "entity_falling_delta": 0.1,
    "enemy_x_delta/squarrel1": 0.5,
    "enemy_x_delta/squarrel2": 0.6,
    "enemy_x_delta/cat": 2,
    "player_x_delta_walk": 1,
    "player_x_delta_run": 2,
    "player_slidedown_max": 0.5,
    "player_dash_mulfactor": 6,  # If mulfactor is large, dash faster, and longer
}

# Player bounce back when damaged?
PLAYER_BOUNCE_BACK = True

# If air_time is larger, player will die
MAX_AIR_TIME_TO_DEAD = 140

# Actual pixel resolution of the game = (512, 288)
DISPLAY_SIZE_MIN = (512, 288)

# Path image base
BASE_IMG_PATH = "data/images/"

# Season for each level
LEVELS = {
    "-1": {
        "map": "../dev_resource/maps/testmap.json",
        "season": "autumn",
        "time_limit": 60000,
    },
    "1": {"map": "data/maps/1.json", "season": "summer", "time_limit": 80000},
    "2": {"map": "data/maps/2.json", "season": "summer", "time_limit": 100000},
    "3": {"map": "data/maps/3.json", "season": "summer", "time_limit": 120000},
    "4": {"map": "data/maps/4.json", "season": "autumn", "time_limit": 120000},
    "5": {"map": "data/maps/5.json", "season": "autumn", "time_limit": 150000},
    "6": {"map": "data/maps/6.json", "season": "winter", "time_limit": 150000},
    "7": {"map": "data/maps/7.json", "season": "winter", "time_limit": 180000},
    "8": {"map": "data/maps/8.json", "season": "tropic", "time_limit": 180000},
    "9": {"map": "data/maps/9.json", "season": "tropic", "time_limit": 180000},
}
LAST_LEVEL_ID = max([int(level) for level in LEVELS])

# Music files for each season
MUSIC = {
    "summer": {"file": "data/music/POL-silly-encounter-short.wav", "volume": 0.5},
    "autumn": {"file": "data/music/POL-follow-me-short.wav", "volume": 0.5},
    "winter": {"file": "data/music/POL-smiley-island-short.wav", "volume": 0.5},
    "tropic": {"file": "data/music/POL-a-sinister-puzzle-short.wav", "volume": 0.5},
    "gameover": {"file": "data/music/POL-foggy-forest-short.wav", "volume": 0.5},
    "finale": {"file": "data/music/POL-pet-park-short.wav", "volume": 0.5},
}

# Energy change
ENERGY = {
    "squarrel1": -0.4,
    "squarrel2": -0.6,
    "cat": -0.8,
    "projectile": -5,
    "fireball": -3,
    "fruit": 1,
    "fireswing": -0.5,
}

# Score change
SCORE = {"squarrel1": 30, "squarrel2": 50, "cat": 70, "fruit": 5}

# Path of the file storing the highest score
PATH_HIGHEST_SCORE = "data/score_highest.dat"

# Colors
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "summer": (14, 219, 248),
    "autumn": (177, 91, 120),
    "tropic": (14, 219, 248),
}

# Volume setting
VOLUME = {
    "jump": 0.6,
    "dash": 0.15,
    "shoot": 0.15,
    "score": 0.3,
    "levelclear": 0.4,
    "dead": 0.5,
    "fireball": 1,
    "hit_by_fire": 0.3,
    "hit_by_enemy": 1,
    "hit_on_enemy": 0.3,
}

# Visual effects.
VISUAL_EFFECT = {
    "leaf": False,
    "cloud": False,
    "boostgas": True,
    "hit": True,
    "spark": True,
}

# Physics check down below (number of pixels) - must be larger than the tallest entity's height
PHYSICS_CHECK_PIXELS_DOWN_BELOW = 25

# Fireswing length (number of fireballs)
FIRESWING_LENGTH = 8

# Fireswing unit length (center to center distance between adjacent balls)
FIRESWING_UNIT_LENGTH = 6
