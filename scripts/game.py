# game.py - Game class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : game.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.


import pygame
from scripts.statusboard import StatusBoard
from scripts.background import Background
from scripts.constants import *
from scripts.entities import Player, Enemy
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.asset import load_asset_images, load_asset_sfx, load_asset_fonts
from scripts.utils import load_score_highest, resize_screen, play_bgm


class Game:
    def __init__(self):
        """Game class initiates the game, declare global attributes related
        to the game operation, setting up stages, play music, and reset the game"""
        # Initiate sound mixer
        pygame.mixer.pre_init(44100, 16, 2, 4096)

        # Initiate pygame
        pygame.init()

        # Hide mouse cursor (TODO: not likely working...!)
        pygame.mouse.set_visible(False)

        # Set the title to display at top bar
        pygame.display.set_caption("Bailey's adventure")

        # Initiate fonts
        pygame.font.init()

        # List up available options for the display sizes
        desktop_size = pygame.display.get_desktop_sizes()[0]
        self.display_sizes = [
            (desktop_size[0] // i, desktop_size[1] // i) for i in [1.25, 1]
        ] + [DISPLAY_SIZE_MIN]
        # Set display
        # When the game is started, it's not a full screen but slightly smaller than the full size.
        self.display_size_id = 0
        resize_screen(self, 0)
        # Original pixel resolution of the game surface is the last
        # element = (512, 288), which is defined in constants.py
        self.display = pygame.Surface(
            self.display_sizes[-1],
            pygame.SRCALPHA,
        )

        # Initiate clock
        self.clock = pygame.time.Clock()

        # Load assets (images, fonts)
        self.assets = load_asset_images()
        self.font = load_asset_fonts()

        # Load sfx
        self.sfx = load_asset_sfx()

        # Set player variables. The postion is random. When the map is loaded,
        # actual position of the player will be determined based on the spawning
        # tile location.
        self.movement = [False, False]
        self.running = False
        self.player = Player(self, (70, 20), (12, 22))

        # If needed, create clouds using Cloud class
        if VISUAL_EFFECT["cloud"]:
            self.clouds = Clouds(self.assets["clouds"], count=8)

        # Initiate tilemap
        self.tilemap = Tilemap(self, tile_size=16)

        # Read the highest score from the file
        self.score_highest = load_score_highest(PATH_HIGHEST_SCORE)

        # Initiate statusboard
        self.statusboard = StatusBoard(self)

        # Parameter to store whether the game is started or not.
        # When the game app is loaded, it should be False as it's not started yet.
        self.is_game_started = False

        # Set sound related parameters
        self.mute = False

        # Key for MUSIC dict in constants.py.
        # For each season, different music will play.
        self.music_key = None

        # Parameter for shaking screen when impact on player is made.
        self.screenshake = 0

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
        self.finale = False
        self.load_level(self.level)

    def load_level(self, map_id, passed_checkpoint_pos=None, reset_time=True):
        """Load level map, spawn all entites,
        and get ready to generate particles, spakrs and projectiles render ready,
        then set the initial camera position
        If specific passed_checkpoint_pos is in args,
        that will be used for the player's position
        when the level is started.
        passed_checkpoint_pos will be one of the checkpoint positions or None.
        """
        # Load level map
        try:
            self.tilemap.load(LEVELS[str(map_id)]["map"])
        except:
            # TODO can do this better
            self.tilemap.load(LEVELS["1"]["map"])

        # Update level and background assets
        self.level = map_id
        self.season = LEVELS[str(self.level)]["season"]
        self.background = Background(
            self.display, self.assets["background"], season=self.season
        )

        # If the music has been already playing, it won't replayed.
        play_bgm(self, music_key=self.season)

        # Update character asset
        if self.season == "winter":
            self.player.type = "player/winter"
        else:
            self.player.type = "player"

        # Collect leaf spawners (trees)
        self.leaf_spawners = []
        if VISUAL_EFFECT["leaf"]:
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
                self.player.pos = (
                    passed_checkpoint_pos if passed_checkpoint_pos else spawner["pos"]
                )
                self.player.pos_at_start = spawner["pos"]
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

        # Collect checkpoint positions
        self.checkpoints = []
        for checkpoint in self.tilemap.extract([("checkpoint", 0)]):
            if checkpoint["variant"] == 0:
                # We need only one variant (value = 0), and we only have that in the tile maps.
                # I left this if clause for later change, which is not likely happening though...
                self.checkpoints.append(checkpoint["pos"])
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

        # (Re)set time parameters only when the level is loading with reset_time is True.
        # (ex, it's True when fresh start of the level)
        # If the level is loaded because the player died,
        # give 30 more seconds for second chance.
        # Cannot be larger than the original time_limit defined in LEVELS
        if reset_time:
            self.time_limit = LEVELS[str(self.level)]["time_limit"]  # ms
            self.time_remain = self.time_limit  #  ms
            self.time_start = pygame.time.get_ticks()  # ms
        else:
            self.time_limit = min(
                self.time_remain + EXTRA_TIME_AFTER_DEAD,
                LEVELS[str(self.level)]["time_limit"],
            )  # ms
            self.time_remain = self.time_limit  #  ms
            self.time_start = pygame.time.get_ticks()  # ms

        self.time_paused = 0  # ms (duration of paused time)
        # To be updated when pause requested, then subtracted when resumed the game
        self.time_right_before_pause = 0
        self.paused = False
        self.levelcleared = (
            False  # To be converted to True when player hits the finishline tile
        )
        # Finishline tiles (variant 0 is the top left corner tile of the finishline sigh)
        self.finishline_tiles = self.tilemap.extract([("finishline", 0)], keep=True)
