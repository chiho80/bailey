# The first lives
# If it's 4, a very first player + 3 more lives, total 4. 3 heads will be displayed
FIRST_LIVES = 4

# Max time for each level
TIME_LIMIT = 200000  # ms

# Camera tracking speed. The smaller the faster.
CAMERA_SPEED = 30

# Frame rate - lower the better performance, higher for smoother motion
FRAME_RATE = 60

# Fireball spawning rate. Increase for more fireballs.
FIREBALL_PROB = 0.005

# Velocity of objcets
VELOCITY = {
    "entity_falling_max": 7,
    "entity_falling_delta": 0.1,
    "enemy_x_delta": 0.5,
    "player_slidedown_max": 0.5,
    "player_dash_mulfactor": 1,
    "player_jump_from_wall_mulfactor": 1,
}

# If air_time is larger, player will die
MAX_AIR_TIME_TO_DEAD = 140

# Available display sizes. Keep every resolutions 16:9 ratio.
# Make sure (512, 288) is always at 8th. (array index = 7)
DISPLAY_SIZE_OPTIONS = [
    (1536, 864),
    (1600, 900),
    (2048, 1152),
    (2560, 1440),
    (2880, 1620),
    (3200, 1800),
    (5120, 2880),
    (512, 288),
    (1024, 576),
]

# Image path base
BASE_IMG_PATH = "data/images/"

# Season for each level
SEASONS = {
    "-1": "autumn",
    "0": "summer",
    "1": "summer",
    "2": "summer",
    "3": "autumn",
    "4": "autumn",
    "5": "winter",
    "6": "winter",
}

# Energy change
ENERGY = {
    "squarrel1": -0.4,
    "squarrel2": -0.6,
    "projectile": -5,
    "fireball": -3,
    "fruit": 1,
}

# Score change
SCORE = {"squarrel1": 30, "squarrel2": 50, "fruit": 5}


# Colors
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "skyblue": (14, 219, 248),
}


# Volume setting
VOLUME = {
    "jump": 0.6,
    "dash": 0.15,
    "shoot": 0.3,
    "score": 0.3,
    "levelclear": 2,
    "dead": 0.5,
    "fireball": 1,
    "hit": 0.3,
}


# Visual effects.
VISUAL_EFFECT = {
    "leaf": True,
    "cloud": True,
    "boostgas": True,
    "hit": True,
    "spark": True,
}
