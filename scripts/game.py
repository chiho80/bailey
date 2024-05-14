import pygame
from scripts.statusboard import StatusBoard
from scripts.background import Background
from scripts.constants import *
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.asset import load_asset_images, load_asset_sfx, load_asset_fonts
from scripts.utils import (
    load_score_highest,
    resize_screen,
)


class Game:
    def __init__(self, first_level):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Bailey's adventure")
        self.display_sizes = DISPLAY_SIZE_OPTIONS
        self.display_size_id = 0
        resize_screen(self, 0)
        self.display = pygame.Surface(
            self.display_sizes[7],  # 7 is (512,288)). Fix this!! Do not change!!
            pygame.SRCALPHA,
        )
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.running = False
        self.assets = load_asset_images()
        self.sfx = load_asset_sfx()
        self.level = first_level
        self.season = LEVELS[str(self.level)]["season"]
        self.clouds = Clouds(self.assets["clouds"], count=8)
        self.player = Player(self, (70, 20), (12, 22))
        self.tilemap = Tilemap(self, tile_size=16)
        self.background = Background(
            self.display, self.assets["background"], season=self.season
        )
        self.screenshake = 0
        self.font = load_asset_fonts()

        # Read the highest score from the file
        self.score_highest = load_score_highest("data/score_highest.dat")

        self.statusboard = StatusBoard(self)
        self.is_game_started = False  # When the game app is loaded, it's not started.
        self.mute = False

    def reset_game(self, first_level):
        """Should be called when the new game is starting.
        ex) very first game, or new game after the previous game is over.
        The parameters related to level, lives, and score will be recovered to the default values
        """
        # level = 0 : First level. Statusboard will display self.level+1
        # Use level = -1 for dev mode.
        self.level = first_level
        self.season = LEVELS[str(self.level)]["season"]
        self.background = Background(
            self.display, self.assets["background"], season=self.season
        )
        self.lives = FIRST_LIVES
        self.score = 0
        self.load_level(self.level)

    def load_level(self, map_id):
        """Load level map, spawn all entites,
        and get ready to generate particles, spakrs and projectiles render ready,
        then set the initial camera position
        """
        # Load level map
        try:
            self.tilemap.load(LEVELS[str(map_id)]["map"])
        except:
            # TODO can do this better
            self.tilemap.load(LEVELS["0"]["map"])

        # Update level and background assets
        self.level = map_id
        self.season = LEVELS[str(map_id)]["season"]
        self.background = Background(
            self.display, self.assets["background"], season=self.season
        )

        # Update character asset
        if self.season == "winter":
            self.player.type = "player/winter"
        else:
            self.player.type = "player"

        # Collect leaf spawners (trees)
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("decor/tree", 1)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            )

        # Collect fireball spawners
        self.fireball_spawners = []
        for firehole in self.tilemap.extract([("decor/firehole", 0)], keep=True):
            self.fireball_spawners.append(
                pygame.Rect(firehole["pos"][0], firehole["pos"][1], 16, 16)
            )

        # Collect fireswing spawners
        self.fireswing_spawners = []
        for fireswing in self.tilemap.extract([("decor/fireswing", 0)], keep=True):
            self.fireswing_spawners.append(
                pygame.Rect(fireswing["pos"][0], fireswing["pos"][1], 16, 16)
            )

        # Create (spawn) entities (player and enemy) at spawners
        self.enemies = []
        for spawner in self.tilemap.extract(
            [("spawners", 0), ("spawners", 1), ("spawners", 2), ("spawners", 3)]
        ):
            if spawner["variant"] == 0:
                # Spawn player. Predefined position for player (70, 20) will be ignored.
                self.player.pos = spawner["pos"]
            else:
                # Spawn enemy
                if spawner["variant"] == 1:
                    enemy_key = "squarrel1"
                    size = (20, 18)
                if spawner["variant"] == 2:
                    enemy_key = "squarrel2"
                    size = (20, 18)
                if spawner["variant"] == 3:
                    enemy_key = "cat"
                    size = (32, 24)
                self.enemies.append(
                    Enemy(self, spawner["pos"], size, enemy_key=enemy_key)
                )

        self.projectiles = []  # Collections for projectiles
        self.fireballs = []  # Collections for fireballs
        self.fireswings = []  # Collections for fires in many fireswings
        self.particles = []  # Collections for particles
        self.sparks = []  # Collections for sparks
        self.textmarks = []  # Collections for floating texts
        self.scroll = [0, 0]  # Initial position of camera
        self.dead = 0  # Is player died?
        self.transition = -30  # For level transitioning effect
        self.player.air_time = 0  # Necessary to avoid infinite reloading the level!
        self.player.energy = 30  # 30 is 100%
        self.player.blink = 0  # Player blinking?
        self.time_limit = TIME_LIMIT  # ms
        self.time_remain = self.time_limit  #  ms
        self.time_start = pygame.time.get_ticks()  # ms
        self.time_paused = 0  # ms (duration of paused time)
        # To be updated when pause requested, then subtracted when resumed the game
        self.time_right_before_pause = 0
        self.paused = False
        self.levelcleared = (
            False  # To be converted to True when player hits the finishline tile
        )
