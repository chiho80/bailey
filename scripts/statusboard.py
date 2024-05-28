# statusboard.py - Top bar displaying game status
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : statusboard.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import pygame
from scripts.utils import draw_text
from scripts.constants import COLORS


class StatusBoard:
    def __init__(self, game):
        self.game = game

    def render(self, surf, pos=(3, 3)):
        # Energy bar - position
        # Energy bar - text
        draw_text(
            self.game.display,
            "ENERGY",
            self.game.font["text_size5"],
            (pos[0], pos[1]),
            text_col=COLORS["white"],
            border_col=COLORS["black"],
        )
        x = 42
        # Energy bar - border and background
        pygame.draw.rect(surf, COLORS["black"], pygame.Rect(x, pos[1] + 2, 31, 3))
        pygame.draw.rect(surf, COLORS["black"], pygame.Rect(x + 1, pos[1] + 1, 29, 5))
        pygame.draw.rect(surf, COLORS["red"], pygame.Rect(x + 1, pos[1] + 2, 29, 3))
        # Energy bar - remaining energy
        color = COLORS["yellow"]
        if self.game.player.energy <= 10:
            if int(self.game.time_remain / 100) % 2 == 1:
                color = COLORS["yellow"]
            else:
                color = COLORS["red"]
        pygame.draw.rect(
            surf,
            color,
            pygame.Rect(x + 1, pos[1] + 2, self.game.player.energy, 3),
        )
        # Energy bar - grid
        for i in range(10):
            pygame.draw.rect(
                surf,
                COLORS["black"],
                pygame.Rect(x + (i + 1) * 3, pos[1] + 2, 1, 3),
            )

        # Bailey lives (head icons)
        for i in range(max(0, self.game.lives - 1)):
            surf.blit(self.game.assets["small_heads/bailey"], (x + 37 + i * 11, pos[1]))

        # Stage number
        x = pos[0] + 135
        draw_text(
            self.game.display,
            f"STAGE {self.game.level}",
            self.game.font["text_size5"],
            (x, pos[1]),
            text_col=COLORS["white"],
            border_col=COLORS["black"],
        )

        # Time
        x = surf.get_width() / 2 - 22
        draw_text(
            self.game.display,
            "TIME",
            self.game.font["text_size5"],
            (x, pos[1]),
            text_col=COLORS["white"],
            border_col=COLORS["black"],
        )

        # Time number
        x = surf.get_width() / 2 + 8
        color = COLORS["white"]
        border_color = COLORS["black"]
        if self.game.time_remain < 30000:
            if int(self.game.time_remain / 100) % 2 == 1:
                color = COLORS["white"]
                border_color = COLORS["black"]
            else:
                color = COLORS["red"]
                border_color = None
        draw_text(
            self.game.display,
            f"{max(0, int(self.game.time_remain / 1000))}",
            self.game.font["text_size5"],
            (x, pos[1]),
            text_col=color,
            border_col=border_color,
        )

        # Highest
        x = surf.get_width() - 5
        draw_text(
            self.game.display,
            f"HIGHEST {self.game.score_highest}",
            self.game.font["text_size5"],
            (x, pos[1]),
            text_col=COLORS["white"],
            border_col=COLORS["black"],
            align=("right", "top"),
        )

        # Score
        x = surf.get_width() - 130
        draw_text(
            self.game.display,
            f"SCORE {self.game.score}",
            self.game.font["text_size5"],
            (x, pos[1]),
            text_col=COLORS["white"],
            border_col=COLORS["black"],
            align=("right", "top"),
        )
