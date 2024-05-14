import math
import pygame
import random
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.textmark import TextMark
from scripts.constants import (
    ENERGY,
    SCORE,
    COLORS,
    VISUAL_EFFECT,
    VELOCITY,
    MAX_AIR_TIME_TO_DEAD,
    PHYSICS_CHECK_PIXELS_DOWN_BELOW,
)


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        self.action = ""
        self.anim_offset = (
            0,
            0,
        )  # Needed because the images have different size and paddings
        self.flip = False
        self.set_action("idle")
        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()

    def drawrect(self, color, rect):
        pygame.draw.rect(
            self.game.display,
            color,
            pygame.Rect(
                rect.x - self.game.scroll[0],
                rect.y - self.game.scroll[1],
                16,
                16,
            ),
        )

    def collide_check_physics(self, tilemap, frame_movement):
        # Check with ongrid physics tiles
        rects_physics = list(tilemap.rects_around(self, tile_types=["physics"]))

        # Update pos in x axis
        self.pos[0] += frame_movement[0]
        # Check collides with ongrid tiles & adjust position (x)
        entity_rect = self.rect()
        for rects in rects_physics:
            rect = rects["rect"]
            # For debugging, draw rect around
            # self.drawrect(COLORS["red"], rect)
            if entity_rect.colliderect(rect):
                # For debuggin , draw rect around which is in collide
                # self.drawrect(COLORS["yellow"], rect)
                # If collide during moving right ...
                if frame_movement[0] > 0:
                    # push back player rect's right to tile rect's left.
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                # If collide during moving left ...
                if frame_movement[0] < 0:
                    # push back player rect's left to tile rect's right.
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                # If collide during idle, it means that the tile approached to player!
                if frame_movement[0] == 0:
                    if entity_rect.right > rect.left and entity_rect.left < rect.left:
                        entity_rect.right = rect.left
                        self.collisions["right"] = True
                    if entity_rect.left < rect.right and entity_rect.right > rect.right:
                        entity_rect.left = rect.right
                        self.collisions["left"] = True
                # Now, update player's position
                self.pos[0] = entity_rect.x

        # Update pos in y axis
        self.pos[1] += frame_movement[1]
        # Check collides with ongrid tiles & adjust position (x)
        entity_rect = self.rect()
        for rects in rects_physics:
            rect = rects["rect"]
            # For debugging, draw rect around
            # self.drawrect(COLORS["red"], rect)
            if entity_rect.colliderect(rect):
                # For debuggin , draw rect around which is in collide
                # self.drawrect(COLORS["yellow"], rect)
                # If collide during moving down ...
                if frame_movement[1] > 0:
                    # push back player rect's bottom to tile rect's top.
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                    # Adjust x if player is on the bottom tile which touching is moving....
                    dx = rects.get("dx", 0)
                    self.pos[0] += dx
                # If collide during moving up ...
                if frame_movement[1] < 0:
                    # push back player rect's top to tile rect's bottom.
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                # Now, update player's position
                self.pos[1] = entity_rect.y

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        # Check collides with ongrid tiles
        self.collide_check_physics(tilemap, frame_movement)

        # Update flip if necessary
        if movement[0] > 0:
            # To use right facing images
            self.flip = False
        if movement[0] < 0:
            # To use left facing images
            self.flip = True

        self.last_movement = movement

        # Free falling speed does not exeed the terminal velocity (entity_falling_max)
        self.velocity[1] = min(
            VELOCITY["entity_falling_max"],
            self.velocity[1] + VELOCITY["entity_falling_delta"],
        )

        # If hitting tiles above or below, set falling velocity zero
        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - offset[0] + self.anim_offset[0],
                self.pos[1] - offset[1] + self.anim_offset[1],
            ),
        )


class Enemy(PhysicsEntity):
    """Enemy can move horizontly, turn around, and shot randomly"""

    def __init__(self, game, pos, size, enemy_key="squarrel1"):
        super().__init__(game, enemy_key, pos, size)

        # Timer
        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            # Check tile in front (7 or -7 pixels) and down below (25 pixels)
            # Careful to use numbers other than 7. Entity may keep flipping back and forth.
            if tilemap.solid_check(
                (
                    self.rect().centerx + (-7 if self.flip else 7),
                    self.pos[1] + PHYSICS_CHECK_PIXELS_DOWN_BELOW,
                )
            ):
                # Entity is on the solid tile, and position to move is also solid.
                if self.collisions["right"] or self.collisions["left"]:
                    # If hit the wall, flip
                    self.flip = not self.flip
                else:
                    # Else, just move to that position
                    # TODO is this equation correct???
                    movement = (
                        (
                            movement[0] - VELOCITY[f"enemy_x_delta/{self.type}"]
                            if self.flip
                            else VELOCITY[f"enemy_x_delta/{self.type}"]
                        ),
                        movement[1],
                    )
            else:
                # Tile where entity will move is not the solid. Flip now.
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)

            # Only for squarrels.
            # Spawn projectile
            # When enemy is not walking,
            # shot or not depending on the distance between enemy and player
            # Also, spawn only if the game is ongoing.
            if self.type in ["squarrel1", "squarrel2"]:
                if not self.walking and self.game.is_game_started:
                    # Shot if y distance is less than 16 pixels
                    dis = (
                        self.game.player.pos[0] - self.pos[0],
                        self.game.player.pos[1] - self.pos[1],
                    )
                    if abs(dis[1]) < 16:
                        # If player is looking left, and is left to the enemy, shot!
                        if self.flip and dis[0] < 0:
                            self.game.sfx["shoot"].play()
                            self.game.projectiles.append(
                                [
                                    [self.rect().centerx - 7, self.rect().centery],
                                    -1.5,
                                    0,
                                ]
                            )
                            for _ in range(4 * VISUAL_EFFECT["spark"]):
                                # Genenrate (spawn) the spark for the latest projectile
                                self.game.sparks.append(
                                    Spark(
                                        self.game.projectiles[-1][0],
                                        random.random() - 0.5 + math.pi,
                                        2 + random.random(),
                                        size=(1, 2),
                                    )
                                )

                        # If player is looking right, and is right to the enemy, shot!
                        if not self.flip and dis[0] > 0:
                            self.game.sfx["shoot"].play()
                            self.game.projectiles.append(
                                [[self.rect().centerx + 7, self.rect().centery], 1.5, 0]
                            )
                            for _ in range(4 * VISUAL_EFFECT["spark"]):
                                # Genenrate (spawn) the spark for the latest projectile
                                self.game.sparks.append(
                                    Spark(
                                        self.game.projectiles[-1][0],
                                        random.random() - 0.5,
                                        2 + random.random(),
                                        size=(1, 2),
                                    )
                                )

        elif random.random() < 0.01:
            # 1% chance at each frame, can be triggered to walk
            if self.type in ["squarrel1", "squarrel2"]:
                self.walking = random.randint(30, 120)
            else:
                # cat
                self.walking = random.randint(60, 180)

        super().update(tilemap, movement=movement)

        # Set enemy's current action
        if movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

        # If this enemy hits player not during dashing, reduce energy of player
        # and make player's speed reduced & move backward
        if self.rect().colliderect(self.game.player.rect()):
            if not self.game.player.dashing:
                # Trigger blinking
                self.game.player.blink += 1
                self.game.player.energy = max(
                    0, self.game.player.energy + ENERGY[self.type]
                )
                # TODO show any animation when energy is reducing?
                # self.game.player.set_action("hit")
            if self.game.player.energy == 0:
                if not self.game.dead:
                    # Trigger screen shake effect
                    self.game.screenshake = max(16, self.game.screenshake)
                self.game.dead += 1

        # If enemy got attack (dash) by player...
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                # Trigger screen shake effect
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx["hit"].play()

                # Update score and spawn textmark
                self.game.score += SCORE[self.type]
                self.game.textmarks.append(
                    TextMark(
                        self.game.player.rect(),
                        self.game.font["text_size5"].render(
                            str(SCORE[self.type]), False, COLORS["black"]
                        ),
                        3,
                    )
                )

                # Spawn sparks
                for _ in range(8 * VISUAL_EFFECT["spark"]):
                    angle = random.random() * math.pi * 2
                    self.game.sparks.append(
                        Spark(
                            self.rect().center,
                            angle,
                            1 + random.random(),
                        )
                    )
                return True

    def render(self, surf, offset=(0, 0)):
        """Enemy may has weapon such as gun. Render the weapon when needed"""
        super().render(surf, offset=offset)

        # Render gun with enemy
        # X position of the gun is different when the enemy is flipped.

        # We currently do not have gun.
        # assets["gur"] is also not loaded for now.
        render_gun = False
        if render_gun:
            if self.flip:
                surf.blit(
                    pygame.transform.flip(self.game.assets["gun"], True, False),
                    (
                        self.rect().centerx
                        - 4
                        - self.game.assets["gun"].get_width()
                        - offset[0],
                        self.rect().centery - offset[1],
                    ),
                )
            else:
                surf.blit(
                    self.game.assets["gun"],
                    (
                        self.rect().centerx + 4 - offset[0],
                        self.rect().centery - offset[1],
                    ),
                )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0

        # Max number of jumps
        self.jumps = 1

        # Can/cannot slide up & down with walls
        self.wall_slide = False

        # To keep tracking how much dashed and its direction
        self.dashing = 0

        # During idle time, occasionally render some random actions
        self.idle_time = 0
        self.next_frame_for_random = [0, 0]
        self.random_action = "random1"

    def set_random_frames(self):
        random_frame_s = random.randint(200, 600)
        random_frame_f = random_frame_s + random.randint(50, 100)
        self.next_frame_for_random = [random_frame_s, random_frame_f]
        self.random_action = random.choice(["random1", "random2", "random3", "random4"])

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        entity_rect = self.rect()

        # If player hit reward, add +10 to score, generate textmark and increase energy +0.5
        for reward_tile in tilemap.reward_tiles_around(self):
            tile_loc = f"{reward_tile['pos'][0]};{reward_tile['pos'][1]}"
            tile = tilemap.tilemap[tile_loc]
            rect = pygame.Rect(
                tile["pos"][0] * tilemap.tile_size + 3,
                tile["pos"][1] * tilemap.tile_size + 3,
                tilemap.tile_size - 6,
                tilemap.tile_size - 6,
            )

            if entity_rect.colliderect(rect):
                # Update score and spawn textmark
                self.game.sfx["score"].play()
                self.game.score += SCORE["fruit"]
                self.game.player.energy = min(
                    30, self.game.player.energy + ENERGY["fruit"]
                )
                self.game.textmarks.append(
                    TextMark(
                        self.game.player.rect(),
                        self.game.font["text_size5"].render(
                            "5", False, COLORS["black"]
                        ),
                        3,
                    )
                )
                del tilemap.tilemap[tile_loc]

        # If player hit finishline tile, update now!
        for rects in tilemap.rects_around(self, tile_types=["finishline"]):
            if entity_rect.colliderect(rects["rect"]):
                self.game.levelcleared = True

        # If player is falling to long time, it means the player is died ...
        if self.air_time > MAX_AIR_TIME_TO_DEAD:
            if not self.game.dead:
                # Trigger screen shake effect
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1

        if self.collisions["down"]:
            # Reset air time and max jump limit when player is on ground
            self.air_time = 0
            self.jumps = 1

        # Check possibility of wall slide at every frame
        self.wall_slide = False
        # If player is hitting wall and is in the air ...
        if (self.collisions["right"] or self.collisions["left"]) and self.air_time > 4:
            self.wall_slide = True
            # Set max downward velocity to 0.5
            self.velocity[1] = min(self.velocity[1], VELOCITY["player_slidedown_max"])
            if self.collisions["right"]:
                self.flip = False
            else:
                self.flip = True
            self.set_action("wall_slide")
            # If player is wall sliding, air_time should not be increased
            # This is necessary to avoid to be killed right after long wall sliding
            self.air_time -= 1

        # Animations other than wall slides should be taken care unless wall sliding now
        if not self.wall_slide:
            if self.air_time > 4:
                self.set_action("jump")
                self.set_random_frames()
            elif movement[0] != 0:
                self.set_action("run")
                self.set_random_frames()
            elif (
                self.idle_time > self.next_frame_for_random[0]
                and self.idle_time < self.next_frame_for_random[1]
            ):
                self.set_action(self.random_action)
                self.idle_time += 1
            else:
                # Idle status.
                self.set_action("idle")
                self.idle_time += 1
                self.set_random_frames()

        # Spawn boostgas bubbles
        if VISUAL_EFFECT["boostgas"]:
            show_radial_gas_at_end = True
            if abs(self.dashing) in {60, 50} and show_radial_gas_at_end:
                for _ in range(1):
                    # Spawn some boosting gas behind player
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                    self.game.particles.append(
                        Particle(
                            self.game,
                            "boostgas",
                            self.rect().center,
                            velocity=pvelocity,
                            frame=random.randint(0, 2),
                        )
                    )

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            # Initial 10 frames of dashing, velocity should be fast!
            # (direction) * 6 * mulfactor.   If mulfactor is large, dash faster, and stop faster too.
            self.velocity[0] = (
                abs(self.dashing) / self.dashing * 6 * VELOCITY["player_dash_mulfactor"]
            )
            if abs(self.dashing) == 51:
                # Remainder of the frames of the dashing animation, velocity will be diminished.
                self.velocity[0] *= 0.1 * VELOCITY["player_dash_mulfactor"]

            # Leave boosting gas behind each frame if P>0.5
            if VISUAL_EFFECT["boostgas"]:
                if random.random() > 0.5:
                    pvelocity = [
                        -abs(self.dashing) / self.dashing * random.random() * 1,
                        0,
                    ]
                    self.game.particles.append(
                        Particle(
                            self.game,
                            "boostgas",
                            self.rect().center,
                            velocity=pvelocity,
                            frame=random.randint(0, 7),
                        )
                    )

        # Avoid to get the variable too large number.
        if self.idle_time > 2500:
            self.idle_time = 0

        # If the action taken was the jump from wall during wall sliding,
        # bring it linearly toward zero to avoid infinite traveling on x axis.
        if self.velocity[0] > 0:
            self.velocity[0] = max(
                self.velocity[0] - 0.1 * VELOCITY["player_jump_from_wall_mulfactor"], 0
            )
        else:
            self.velocity[0] = min(
                self.velocity[0] + 0.1 * VELOCITY["player_jump_from_wall_mulfactor"], 0
            )

    def render(self, surf, offset=(0, 0)):
        # Use this to hide the palyer for the first 10 frames
        # if abs(self.dashing) <= 50:
        #     super().render(surf, offset=offset)
        # If this effect is not needed, just render it.
        super().render(surf, offset=offset)

    def jump(self):
        """Handle all the cases of jumping action including
        jump during wall sliding, from left to right, and opposit,
        as well as normal jump from ground.
        Return True when the jump action successufully occurs."""

        # We prioritize jump from wall slide, then handle normal jump
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                # If player was sliding at the left wall,
                # this jump should have direction of velocity toward right side.
                # Put y velocity a bit smaller than normal jump.
                self.velocity[0] = 3.5 * VELOCITY["player_jump_from_wall_mulfactor"]
                self.velocity[1] = -2.5 * VELOCITY["player_jump_from_wall_mulfactor"]
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif (not self.flip) and self.last_movement[0] > 0:
                self.velocity[0] = -3.5 * VELOCITY["player_jump_from_wall_mulfactor"]
                self.velocity[1] = -2.5 * VELOCITY["player_jump_from_wall_mulfactor"]
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        if self.jumps:
            self.velocity[1] = -3.2 * VELOCITY["player_jump_from_wall_mulfactor"]
            self.jumps -= 1
            self.air_time = 5
            return True

    def dash(self):
        if not self.dashing:
            self.game.sfx["dash"].play()
            # Total & max of 60 frames are allocated for dashing action.
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
