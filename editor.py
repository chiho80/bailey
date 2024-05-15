import sys
import pygame
from scripts.utils import load_images
from scripts.tilemap import Tilemap

DISPLAY_SIZE = (800, 452)
RENDER_SCALE = 2

# 0 = summer 1
# 1 = summer 2
# 2 = summer 3
# 3 = autumn 1
# 4 = autumn 2
# 5 = winter 1
# 6 = winter 2
# 7 = tropic 1

try:
    LEVEL = int(sys.argv[1])
except:
    LEVEL = 7


class Editor:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("World Edtor")
        self.screen = pygame.display.set_mode(
            (DISPLAY_SIZE[0] * RENDER_SCALE, DISPLAY_SIZE[1] * RENDER_SCALE)
        )
        self.display = pygame.Surface(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()

        self.assets = {
            "grass": load_images("tiles/grass"),
            "autumn": load_images("tiles/autumn"),
            "ice": load_images("tiles/ice"),
            "tropic": load_images("tiles/tropic"),
            "finishline": load_images("tiles/finishline"),
            "movingtile": load_images("tiles/movingtile"),
            "decor/tree": load_images("tiles/decor/tree", trans_color=(253, 77, 211)),
            "decor/fence": load_images("tiles/decor/fence", trans_color=(253, 77, 211)),
            "decor/summer_tree": load_images("tiles/decor/summer_tree"),
            "decor/tropic_tree": load_images("tiles/decor/tropic_tree"),
            "decor/firehole": load_images("tiles/decor/firehole"),
            "decor/fireswing": load_images("tiles/decor/fireswing"),
            "spawners": load_images("tiles/spawners", trans_color=(0, 0, 0)),
            "reward/food": load_images("tiles/reward/food"),
            "checkpoint": load_images("tiles/checkpoint"),
        }

        self.movement = [False, False, False, False]

        self.tilemap = Tilemap(self, tile_size=16)

        # Load existing map
        try:
            if LEVEL == -1:
                self.tilemap.load(f"../dev_resource/maps/testmap.json")
            else:
                self.tilemap.load(f"data/maps/{LEVEL}.json")
        except FileNotFoundError:
            pass

        # Camera position
        self.scroll = [0, 0]

        # Convert everything of assets into list
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.shift = False

        self.ongrid = True

        self.activate_movingground = False

    def run(self):
        quit_game = False

        # Infinite game loop begins here ...
        while True:
            # Cover screen with the default background color
            self.display.fill((0, 0, 0))

            # Camera movement
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 4
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 4
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(
                self.display,
                offset=render_scroll,
                activate_movingground=self.activate_movingground,
            )

            # Display current tile selected
            current_tile_img = self.assets[self.tile_list[self.tile_group]][
                self.tile_variant
            ].copy()
            # current_tile_img.set_alpha(100)

            # Get mouse position
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (
                int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size),
            )
            tile_loc = f"{tile_pos[0]};{tile_pos[1]}"

            # Preview where the tile will be placed
            if self.ongrid:
                self.display.blit(
                    current_tile_img,
                    (
                        tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                        tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                    ),
                )
            else:
                self.display.blit(current_tile_img, mpos)

            # Place a tile
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[tile_loc] = {
                    "type": self.tile_list[self.tile_group],
                    "variant": self.tile_variant,
                    "pos": tile_pos,
                }

            # Delete a tile
            if self.right_clicking:
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(
                        tile["pos"][0] - self.scroll[0],
                        tile["pos"][1] - self.scroll[1],
                        tile_img.get_width(),
                        tile_img.get_height(),
                    )
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
                for tile in self.tilemap.moving_offgrid_tiles.copy():
                    tile_img = self.assets[tile["type"]][tile["variant"]]
                    tile_r = pygame.Rect(
                        tile["pos"][0] - self.scroll[0],
                        tile["pos"][1] - self.scroll[1],
                        tile_img.get_width(),
                        tile_img.get_height(),
                    )
                    if tile_r.collidepoint(mpos):
                        self.tilemap.moving_offgrid_tiles.remove(tile)

            # Preview current tile selected at top left
            self.display.blit(current_tile_img, (5, 5))

            # Quit game if any quit condition became True
            if quit_game:
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            tiledata = {
                                "type": self.tile_list[self.tile_group],
                                "variant": self.tile_variant,
                                "pos": (
                                    mpos[0] + self.scroll[0],
                                    mpos[1] + self.scroll[1],
                                ),
                            }
                            self.tilemap.offgrid_tiles.append(tiledata)
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(
                                self.assets[self.tile_list[self.tile_group]]
                            )
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(
                                self.tile_list
                            )
                            self.tile_variant = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_game = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_m:
                        self.activate_movingground = not self.activate_movingground
                    if event.key == pygame.K_o:
                        if LEVEL == -1:
                            self.tilemap.save(f"../dev_resource/maps/testmap.json")
                        else:
                            self.tilemap.save(f"data/maps/{LEVEL}.json")
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_z:
                        self.tile_variant = (self.tile_variant - 1) % len(
                            self.assets[self.tile_list[self.tile_group]]
                        )
                    if event.key == pygame.K_x:
                        self.tile_variant = (self.tile_variant + 1) % len(
                            self.assets[self.tile_list[self.tile_group]]
                        )
                    if event.key == pygame.K_c:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_v:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
