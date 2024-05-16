def position_initialize(pos, img_size, surf_size):
    render_pos = [0, 0]
    for i, val in enumerate(pos):
        if val >= 0:
            render_pos[i] = val
        elif val == -999:
            # -999 is the contract for bottom (or right) aligh
            render_pos[i] = surf_size[i] - img_size[i]
        else:
            # val < 0 : val is the distance from bottom (or right)
            render_pos[i] = surf_size[i] - img_size[i] + val
    return render_pos


class BackgroundLayer:
    def __init__(self, surf, image_dict):
        self.img = image_dict["image"]
        self.depth = image_dict["depth"]
        self.surf_size = surf.get_size()
        self.img_size = self.img.get_size()
        self.pos_original = position_initialize(
            list(image_dict["pos"]), self.img_size, self.surf_size
        )
        self.pos = [
            [self.pos_original[0] - self.img_size[0], self.pos_original[1]],
            [self.pos_original[0], self.pos_original[1]],
            [self.pos_original[0] + self.img_size[0], self.pos_original[1]],
        ]

    def update(self, movement):
        # Background y position won't be changed.
        for i in range(len(self.pos)):
            self.pos[i] = [
                self.pos[i][0] - self.depth * 0.1 * (movement[1] - movement[0]),
                self.pos[i][1],
            ]
            if self.pos[i][0] < -self.img_size[0]:
                self.pos[i][0] += 3 * self.img_size[0]

            if self.pos[i][0] > 2 * self.img_size[0]:
                self.pos[i][0] -= 3 * self.img_size[0]

    def render(self, surf):
        # Adjust the position if there are gaps.
        render_pos = []
        for pos in self.pos:
            render_pos.append([(pos[0]), (pos[1])])

        if (render_pos[1][0] - render_pos[0][0]) % self.img_size[0]:
            if render_pos[1][0] > render_pos[0][0]:
                render_pos[1][0] -= 1
            else:
                render_pos[0][0] -= 1
        if (render_pos[2][0] - render_pos[1][0]) % self.img_size[0]:
            if render_pos[2][0] > render_pos[1][0]:
                render_pos[2][0] -= 1
            else:
                render_pos[1][0] -= 1
        if (render_pos[0][0] - render_pos[2][0]) % self.img_size[0]:
            if render_pos[0][0] > render_pos[2][0]:
                render_pos[0][0] -= 1
            else:
                render_pos[2][0] -= 1

        for pos in render_pos:
            surf.blit(self.img, pos)


class Background:
    def __init__(self, surf, background_images, season="summer"):
        self.background_layers = []

        # Spawn background images...
        for i, image_dict in enumerate(background_images[season]):
            self.background_layers.append(BackgroundLayer(surf, image_dict))

        # Sort background objects by depth
        # By this, far background will move slower ...
        self.background_layers.sort(key=lambda x: x.depth)

    def update(self, surf, movement):
        for background_image in self.background_layers:
            background_image.update(movement)

    def render(self, surf):
        for background_image in self.background_layers:
            background_image.render(surf)
