# animation.py - Animation class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : animation.py
# @created     : Saturday May 18, 2024 08:57 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import pygame


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self, flip=(False, False)):
        return pygame.transform.flip(
            self.images[int(self.frame / self.img_duration)], flip[0], flip[1]
        )
