import math


class Particle:
    def __init__(
        self,
        game,
        p_type,
        pos,
        velocity=[0, 0],
        angular_motion_velocity=None,
        angular_motion_offset=0,
        angular_motion_center=None,
        angular_motion_initial_theta=0,
        frame=0,
        freefalling=False,
    ):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.initial_pos = list(pos)
        self.velocity = list(velocity)
        self.angular_motion_velocity = angular_motion_velocity
        self.angular_motion_offset = angular_motion_offset
        self.angular_motion_center = angular_motion_center
        self.angular_motion_theta = angular_motion_initial_theta
        self.animation = self.game.assets["particle/" + p_type].copy()
        self.animation.frame = frame
        self.freefalling = freefalling
        self.xflip = False
        self.yflip = False

    def update(self):
        kill = False
        # If animation of the particle is done, set kill True
        if self.animation.done:
            kill = True

        # If angular_motion_velocity is not None, this particle is in circular motion
        if self.angular_motion_velocity:
            # Update position of the particle
            self.angular_motion_theta += self.angular_motion_velocity
            if self.angular_motion_theta > 2:
                self.angular_motion_theta = 0
            self.pos[0] = (
                self.angular_motion_center[0]
                + math.cos(math.pi * self.angular_motion_theta)
                * self.angular_motion_offset
            )
            self.pos[1] = (
                self.angular_motion_center[1]
                + math.sin(math.pi * self.angular_motion_theta)
                * self.angular_motion_offset
            )
            kill = False

        else:
            # Update position of the particle
            self.pos[0] += self.velocity[0]
            self.pos[1] += self.velocity[1]

            # Update y velociry if freefalling is True
            # Currently, only the fireball is freefalling
            if self.freefalling:
                self.velocity[1] += 0.1

                # Flip y if it is falling
                if self.velocity[1] > 0:
                    self.yflip = True

                # Kill if y velocity is too large, or y position is lower than initial position
                if self.velocity[1] > 10 or (self.pos[1] > self.initial_pos[1]):
                    kill = True

        self.animation.update()

        return kill

    def render(self, surf, offset=(0, 0)):
        img = self.animation.img((self.xflip, self.yflip))
        surf.blit(
            img,
            (
                self.pos[0] - offset[0] - img.get_width() // 2,
                self.pos[1] - offset[1] - img.get_height() // 2,
            ),
        )
