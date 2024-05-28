# spark.py - Spark class
#
# @author      : Chiho Kim (chiho80@gmail.com)
# @file        : spark.py
# @created     : Fridat May 17, 2024 22:42 PT
#
# Copyright (c) 2024 Chiho Kim. All rights reserved.

import math
import random
import pygame


class Spark:
    def __init__(self, pos, angle, speed, size=(1, 3)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.size = list(size)

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        # Once the speed is zero, return True,
        # which is the kill signal. This will remove the spark.
        return not self.speed

    def render(self, surf, offset=(0, 0)):
        # circle(surface, color, center, radius)
        pygame.draw.circle(
            surf,
            (255, 255, 255),
            (self.pos[0] - offset[0], self.pos[1] - offset[1]),
            random.randint(self.size[0], self.size[1]),
        )

        # Define some polygon ... (diamond shape)
        # render_points = {
        #     "diamond": [
        #         (
        #             self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0],
        #             self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1],
        #         ),
        #         (
        #             self.pos[0]
        #             + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5
        #             - offset[0],
        #             self.pos[1]
        #             + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5
        #             - offset[1],
        #         ),
        #         (
        #             self.pos[0]
        #             + math.cos(self.angle + math.pi) * self.speed * 3
        #             - offset[0],
        #             self.pos[1]
        #             + math.sin(self.angle + math.pi) * self.speed * 3
        #             - offset[1],
        #         ),
        #         (
        #             self.pos[0]
        #             + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5
        #             - offset[0],
        #             self.pos[1]
        #             + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5
        #             - offset[1],
        #         ),
        #     ]
        # }
        # pygame.draw.polygon(surf, (255, 255, 255), render_points["diamond"])
