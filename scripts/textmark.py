# textmark.py - Textmark class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : textmark.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

from scripts.utils import draw_text


class TextMark:
    def __init__(self, pos, text, font, color, border_col, speed):
        self.text = text
        self.font = font
        self.pos = list(pos)
        self.color = color
        self.border_col = border_col
        self.speed = speed

    def update(self):
        self.pos[1] -= self.speed
        self.speed = max(0, self.speed - 0.1)

        # Once the speed is zero, return True,
        # This will remove the textmark.
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        draw_text(
            surf,
            self.text,
            self.font,
            (self.pos[0] - offset[0], self.pos[1] - offset[1]),
            text_col=self.color,
            align=("center", "middle"),
            antialias=False,
            border_col=self.border_col,
        )
