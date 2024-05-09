import pygame
from scripts.utils import load_image, load_images, Animation, set_volume


def load_asset_images():
    assets = {
        "intro": load_image("intro.png", scale=0.3),
        "grass": load_images("tiles/grass"),
        "autumn": load_images("tiles/autumn"),
        "ice": load_images("tiles/ice"),
        "finishline": load_images("tiles/finishline"),
        "movingtile": load_images("tiles/movingtile"),
        "decor/tree": load_images("tiles/decor/tree", trans_color=(253, 77, 211)),
        "decor/fence": load_images("tiles/decor/fence", trans_color=(253, 77, 211)),
        "decor/summer_tree": load_images("tiles/decor/summer_tree"),
        "decor/firehole": load_images("tiles/decor/firehole"),
        "reward/food": load_images("tiles/reward/food"),
        "player": load_image("entities/Bailey12x22_1.png"),
        "background": {
            "summer": [
                {
                    "image": load_image("backgrounds/background_summer.png", scale=1),
                    "pos": (0, -999),
                    "depth": 1,
                }
            ],
            "autumn": [
                {
                    "image": load_image("backgrounds/background_autumn0.png", scale=1),
                    "pos": (0, 50),
                    "depth": 1,
                },
                {
                    "image": load_image("backgrounds/background_autumn0.png", scale=1),
                    "pos": (0, 0),
                    "depth": 1,
                },
                {
                    "image": load_image("backgrounds/background_autumn1.png", scale=1),
                    "pos": (0, -30),
                    "depth": 4,
                },
                {
                    "image": load_image("backgrounds/background_autumn1.png", scale=1),
                    "pos": (-16, -999),
                    "depth": 5,
                },
                {
                    "image": load_image("backgrounds/background_autumn2.png", scale=1),
                    "pos": (0, 0),
                    "depth": 3,
                },
                {
                    "image": load_image("backgrounds/background_autumn3.png", scale=1),
                    "pos": (0, 0),
                    "depth": 2,
                },
            ],
            "winter": [
                {
                    "image": load_image("backgrounds/background_winter0.png", scale=1),
                    "pos": (0, 0),
                    "depth": 1,
                },
                {
                    "image": load_image("backgrounds/background_winter1.png", scale=1),
                    "pos": (0, -20),
                    "depth": 2,
                },
                {
                    "image": load_image("backgrounds/background_winter2.png", scale=1),
                    "pos": (0, -999),
                    "depth": 3,
                },
            ],
        },
        "clouds": load_images("clouds"),
        "player/idle": Animation(load_images("entities/player/idle")),
        "player/run": Animation(load_images("entities/player/run"), img_dur=4),
        "player/jump": Animation(load_images("entities/player/jump")),
        "player/fall": Animation(load_images("entities/player/fall")),
        "player/random1": Animation(
            load_images("entities/player/random1"),
        ),
        "player/random2": Animation(
            load_images("entities/player/random2"),
        ),
        "player/random3": Animation(
            load_images("entities/player/random3"),
        ),
        "player/random4": Animation(
            load_images("entities/player/random4"),
        ),
        "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
        "player/winter/idle": Animation(load_images("entities/player_winter/idle")),
        "player/winter/run": Animation(
            load_images("entities/player_winter/run"), img_dur=4
        ),
        "player/winter/jump": Animation(load_images("entities/player_winter/jump")),
        "player/winter/fall": Animation(load_images("entities/player_winter/fall")),
        "player/winter/random1": Animation(
            load_images("entities/player_winter/random1"),
        ),
        "player/winter/random2": Animation(
            load_images("entities/player_winter/random2"),
        ),
        "player/winter/random3": Animation(
            load_images("entities/player_winter/random3"),
        ),
        "player/winter/random4": Animation(
            load_images("entities/player_winter/random4"),
        ),
        "player/winter/wall_slide": Animation(
            load_images("entities/player_winter/wall_slide")
        ),
        "squarrel1/idle": Animation(load_images("entities/squarrel1/idle"), img_dur=6),
        "squarrel1/run": Animation(load_images("entities/squarrel1/run"), img_dur=4),
        "squarrel2/idle": Animation(load_images("entities/squarrel2/idle"), img_dur=6),
        "squarrel2/run": Animation(load_images("entities/squarrel2/run"), img_dur=4),
        "particle/leaf": Animation(
            load_images("particles/leaf", trans_color=(0, 0, 0)),
            img_dur=20,
            loop=False,
        ),
        "particle/boostgas": Animation(
            load_images("particles/boostgas", trans_color=(0, 0, 0)),
            img_dur=6,
            loop=False,
        ),
        "particle/fireball": Animation(
            load_images("particles/fireball"),
            img_dur=3,
        ),
        "particle/particle": Animation(
            load_images("particles/particle", trans_color=(0, 0, 0)),
            img_dur=6,
            loop=False,
        ),
        "projectile": load_image("projectile.png"),
        "small_heads/bailey": load_image("small_heads/bailey.png"),
    }
    return assets


def load_asset_sfx():
    assets = {
        "jump": pygame.mixer.Sound("data/sfx/jump.wav"),
        "dash": pygame.mixer.Sound("data/sfx/dash.wav"),
        "shoot": pygame.mixer.Sound("data/sfx/shoot.wav"),
        "hit": pygame.mixer.Sound("data/sfx/hit.wav"),
        "score": pygame.mixer.Sound("data/sfx/score.wav"),
        "levelclear": pygame.mixer.Sound("data/sfx/levelclear.wav"),
        "dead": pygame.mixer.Sound("data/sfx/dead.wav"),
        "fireball": pygame.mixer.Sound("data/sfx/fireball.wav"),
    }
    set_volume(assets)
    return assets


def load_asset_fonts():
    return {
        "text_size5": pygame.font.Font("data/fonts/Quinquefive-ALoRM.ttf", 5),
        "text_size8": pygame.font.Font("data/fonts/Quinquefive-ALoRM.ttf", 8),
        "text_size14": pygame.font.Font("data/fonts/Quinquefive-ALoRM.ttf", 14),
        "text_size22": pygame.font.Font("data/fonts/Quinquefive-ALoRM.ttf", 22),
    }