import pygame
from scripts.utils import draw_text
from scripts.constants import COLORS


class StatusBoard:
    def __init__(self, game):
        self.game = game

    def render(self, surf, pos=(3, 3)):
        # Bailey lives (head icons)
        for i in range(max(0, self.game.lives - 1)):
            surf.blit(self.game.assets["small_heads/bailey"], (pos[0] + i * 11, pos[1]))

        # Energy (bar)
        x = pos[0] + max(0, self.game.lives - 1) * 11 + 2
        pygame.draw.rect(surf, COLORS["black"], pygame.Rect(x, pos[1] + 2, 32, 3))
        pygame.draw.rect(surf, COLORS["black"], pygame.Rect(x + 1, pos[1] + 1, 30, 5))
        pygame.draw.rect(surf, COLORS["red"], pygame.Rect(x + 1, pos[1] + 2, 30, 3))
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

        # Stage number
        x = pos[0] + 120
        draw_text(
            self.game.display,
            f"LEVEL {self.game.level + 1}",
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
