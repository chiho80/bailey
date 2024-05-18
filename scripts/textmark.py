# textmark.py - Textmark class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : textmark.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.


class TextMark:
    def __init__(self, pos, text_surf, speed):
        self.text_surf = text_surf
        self.pos = list(pos)
        self.text_surf = text_surf
        self.speed = speed

    def update(self):
        self.pos[1] -= self.speed
        self.speed = max(0, self.speed - 0.1)

        # Once the speed is zero, return True,
        # This will remove the textmark.
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            self.text_surf,
            (self.pos[0] - offset[0], self.pos[1] - offset[1]),
        )
