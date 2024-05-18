# tilemap.py - Tilemap class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : tilemap.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import pygame
import json
import math

NEIGHBOR_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]
NEIGHBOR_OFFSETS_TALL = NEIGHBOR_OFFSETS + [
    (-1, 2),
    (0, 2),
    (1, 2),
]
PHYSICS_TILES = {"grass", "ice", "autumn", "movingtile", "tropic", "decor/fireswing"}
REWARD_TILES = {"reward/food"}
FINISH_TILES = {"finishline"}
AUTOTILE_TYPES = {"grass", "ice", "autumn", "tropic"}
AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}
MOVINGTILE_SPECS = {
    ("movingtile", 0): {"max_range": (3 * 16, 0), "initial_speed": (0.005, 0)},
    ("movingtile", 1): {"max_range": (3 * 16, 0), "initial_speed": (-0.005, 0)},
    ("movingtile", 2): {"max_range": (3 * 16, 0), "initial_speed": (0.008, 0)},
    ("movingtile", 3): {"max_range": (3 * 16, 0), "initial_speed": (-0.008, 0)},
    ("movingtile", 4): {"max_range": (4 * 16, 0), "initial_speed": (0.005, 0)},
    ("movingtile", 5): {"max_range": (4 * 16, 0), "initial_speed": (-0.005, 0)},
    ("movingtile", 6): {"max_range": (4 * 16, 0), "initial_speed": (0.008, 0)},
    ("movingtile", 7): {"max_range": (4 * 16, 0), "initial_speed": (-0.008, 0)},
}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}  # restricted by physics
        self.offgrid_tiles = []
        self.transport = {}

    def extract(self, id_pairs, keep=False):
        """Extract tiles with id_pairs to spawn something
        id_pairs: list of tile type & variant pairs
        keep = True if want to keep staying in the game,
        keep = False if wanted to remove after the incident
        """
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile["type"], tile["variant"]) in id_pairs:
                matches.append(tile.copy())
                # Update the tile just appended ...
                matches[-1]["pos"] = matches[-1]["pos"].copy()
                matches[-1]["pos"][0] *= self.tile_size
                matches[-1]["pos"][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches

    def tiles_around(self, entity_pos, is_tall):
        """Collect tiles around entity"""
        tiles = []

        # First, collect the tiles around, using the entity_loc.
        # These tiles will be used for collide check.
        # If tile is ("glass", 19), do not add. We will handle this later
        entity_loc = (
            int(entity_pos[0] // self.tile_size),
            int(entity_pos[1] // self.tile_size),
        )
        for offset in NEIGHBOR_OFFSETS_TALL if is_tall else NEIGHBOR_OFFSETS:
            check_loc = f"{entity_loc[0] + offset[0]};{entity_loc[1] + offset[1]}"
            if check_loc in self.tilemap:
                if not self.tilemap[check_loc]["type"] == "movingtile":
                    tiles.append(self.tilemap[check_loc])

        # Tile with type "movingtile" is special one. It's moving thus, check_loc based
        # searching does not work.
        # Use actual pixel position to check if it's around player.
        tiles_to_check = {}
        for tile in self.tilemap:
            if self.tilemap[tile]["type"] == "movingtile":
                tiles_to_check[tile] = self.tilemap[tile]

        for tile in tiles_to_check:
            # If "renderpos" not exist in this tile, set (0,0).
            # This is okay because the tile will be positioned at (0,0)
            # for only the very first one frame.
            tile_pos = tiles_to_check[tile].get("renderpos", (0, 0))
            for offset in NEIGHBOR_OFFSETS_TALL if is_tall else NEIGHBOR_OFFSETS:
                check_pos = (
                    entity_pos[0] + offset[0] * self.tile_size,
                    entity_pos[1] + offset[1] * self.tile_size,
                )  # Player's offseted position
                if (
                    check_pos[0] > tile_pos[0]
                    and check_pos[0] < tile_pos[0] + self.tile_size
                    and check_pos[1] > tile_pos[1]
                    and check_pos[1] < tile_pos[1] + self.tile_size
                ):
                    tiles.append(tiles_to_check[tile])

        return tiles

    def save(self, path):
        f = open(path, "w")
        for tile in self.tilemap:
            tile_to_save = self.tilemap[tile].copy()
            tile_to_save.pop("renderpos", None)
            tile_to_save.pop("renderpos_prev", None)
            tile_to_save.pop("transport", None)
            self.tilemap.update({tile: tile_to_save})

        json.dump(
            {
                "tilemap": self.tilemap,
                "tile_size": self.tile_size,
                "offgrid": self.offgrid_tiles,
            },
            f,
        )
        f.close()

    def load(self, path):
        f = open(path, "r")
        map_data = json.load(f)
        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]

    def solid_check(self, pos):
        """Check if pos is for solid tiles"""
        tile_loc = f"{int(pos[0] // self.tile_size)};{int(pos[1] // self.tile_size)}"
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]["type"] in PHYSICS_TILES:
                return self.tilemap[tile_loc]

    def rects_around(self, entity, tile_types=["physics"]):
        """Return a list of rects around entity
        Important: If the tile_type is movingground (tile type = "movingtile"),
        we need to return the rects for the previous position of each tile too, thus
        the returning a list of dict [{"rect":rect for current pos, "rect_prev": rect for previous pos}, ...]
        Other than the movingground, the returning list will have only one component,
        [{"rect":rect for current pos}, ...]
        """
        # Get position of physics tiles around the entity
        pos = entity.pos

        # Check if entity's height is larger than tile size.
        # If larger, we should check more tiles down below.
        if entity.size[1] > self.tile_size:
            is_tall = True
        else:
            is_tall = False

        # Tiles around the entity will be appended to the list
        rects = []
        for tile_type in tile_types:
            # Tile type to check
            if tile_type == "physics":
                tile_types_to_check = PHYSICS_TILES
            elif tile_type == "finishline":
                tile_types_to_check = FINISH_TILES
            else:
                return []

            tiles_to_check = self.tiles_around(pos, is_tall)
            for tile in tiles_to_check:
                if tile["type"] in tile_types_to_check:
                    if tile["type"] == "movingtile":
                        rect_to_add = {
                            "rect": pygame.Rect(
                                tile.get("renderpos", [0, 0])[0],
                                tile.get("renderpos", [0, 0])[1],
                                self.tile_size,
                                self.tile_size,
                            ),
                            "rect_prev": pygame.Rect(
                                tile.get("renderpos_prev", [0, 0])[0],
                                tile.get("renderpos_prev", [0, 0])[1],
                                self.tile_size,
                                self.tile_size,
                            ),
                            "dx": tile.get("renderpos", [0, 0])[0]
                            - tile.get("renderpos_prev", [0, 0])[0],
                        }
                    else:
                        rect_to_add = {
                            "rect": pygame.Rect(
                                tile["pos"][0] * self.tile_size,
                                tile["pos"][1] * self.tile_size,
                                self.tile_size,
                                self.tile_size,
                            )
                        }

                    rects.append(rect_to_add)
        return rects

    def reward_tiles_around(self, entity):
        # Get id_pairs of reward tiles around
        pos = entity.pos

        # Check if entity's height is larger than tile size.
        # If larger, we should check more tiles down below.
        if entity.size[1] > self.tile_size:
            is_tall = True
        else:
            is_tall = False

        # Tiles around the entity will be appended to the list
        tile_locs = []
        for tile in self.tiles_around(pos, is_tall):
            if tile["type"] in REWARD_TILES:
                tile_locs.append(tile)
        return tile_locs

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = f"{tile['pos'][0] + shift[0]};{tile['pos'][1] + shift[1]}"
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if tile["type"] in AUTOTILE_TYPES and neighbors in AUTOTILE_MAP:
                tile["variant"] = AUTOTILE_MAP[neighbors]

    def update_global_transport(self):
        for movingtile_spec in MOVINGTILE_SPECS:
            # Get old one
            self.transport[movingtile_spec] = self.transport.get(
                movingtile_spec, (0, 0)
            )
            # Update
            self.transport[movingtile_spec] = (
                self.transport[movingtile_spec][0]
                + MOVINGTILE_SPECS[movingtile_spec]["initial_speed"][0],
                self.transport[movingtile_spec][1]
                + MOVINGTILE_SPECS[movingtile_spec]["initial_speed"][1],
            )
            # If it went too much, switch sign to make it bound in -2 ~ +2
            if abs(self.transport[movingtile_spec][0]) > 2:
                self.transport[movingtile_spec] = (
                    self.transport[movingtile_spec][0] * -1,
                    self.transport[movingtile_spec][1],
                )
            if abs(self.transport[movingtile_spec][1]) > 2:
                self.transport[movingtile_spec] = (
                    self.transport[movingtile_spec][0],
                    self.transport[movingtile_spec][1] * -1,
                )

    def render(self, surf, offset=(0, 0), activate_movingground=True):
        # Handle some decorative tiles first ...
        for tile in self.offgrid_tiles:
            (x, y) = (
                tile["pos"][0] - offset[0],
                tile["pos"][1] - offset[1],
            )
            surf.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (x, y),
            )

        # Calculate global transport for moving tiles
        self.update_global_transport()

        # Render ongrid tiles now.
        # If tile in the world is outside the camera, avoid render them for faster operation.
        # Range all the numbers between tile cordinate of top left - 1 and bottom right + 1
        for x in range(
            offset[0] // self.tile_size - 1,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size - 1,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = f"{x};{y}"
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    renderpos = (
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                    )
                    if tile["type"] == "movingtile" and activate_movingground:

                        renderpos_moved = (
                            renderpos[0]
                            + math.sin(
                                self.transport[(tile["type"], tile["variant"])][0]
                                * math.pi
                            )
                            * MOVINGTILE_SPECS[(tile["type"], tile["variant"])][
                                "max_range"
                            ][0],
                            renderpos[1]
                            + math.cos(
                                self.transport[(tile["type"], tile["variant"])][1]
                                * math.pi
                            )
                            * MOVINGTILE_SPECS[(tile["type"], tile["variant"])][
                                "max_range"
                            ][1],
                        )
                        # Update tilemap with movingground tile position
                        self.tilemap[loc] = {
                            "type": tile["type"],
                            "variant": tile["variant"],
                            "pos": tile["pos"],
                            "transport": self.transport[
                                (tile["type"], tile["variant"])
                            ],
                            "renderpos_prev": self.tilemap[loc].get(
                                "renderpos", renderpos
                            ),
                        }
                        self.tilemap[loc]["renderpos"] = renderpos_moved
                    else:
                        self.tilemap[loc]["renderpos"] = renderpos
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            self.tilemap[loc]["renderpos"][0] - offset[0],
                            self.tilemap[loc]["renderpos"][1] - offset[1],
                        ),
                    )
