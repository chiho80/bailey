import os
import sys
import random
import math
import pygame
from scripts.constants import *
from scripts.utils import save_score_highest
from scripts.banners import (
    display_intro,
    display_gameover,
    display_paused,
    display_level_cleared,
    display_finale,
)
from scripts.game import Game
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.control import check_keyboard_input

# User can specify the level to start by providing an argument.
try:
    FIRST_LEVEL = int(sys.argv[1])
except:
    FIRST_LEVEL = 1

# Change working directory to the location where the executable is at.
# Executable cannot find sub folders (data/ and scripts/) without doing this.
try:
    os.chdir(sys._MEIPASS)
except:
    os.chdir(os.getcwd())

# Set app icon.
if os.name == "nt":
    # Works for MS Windows. Only the file in extension of .ico will work.
    pygame.display.set_icon(pygame.image.load("data/images/ico/favicon.ico"))
else:
    pygame.display.set_icon(pygame.image.load("data/images/ico/macos_512x512x32.png"))


def main():
    """Main game loop happens in this async function.
    Create a game object, update every elements (player, enemy, tiles, background...),
    render them, check key controls, dead check, level check, etc ...
    async is used just in case of using the pygbag, which is not likely happening
    because of the speed issue.
    """

    game = Game(FIRST_LEVEL)
    quit_game = False
    game.reset_game(FIRST_LEVEL)
    game.play_bgm()

    # Infinite game loop begins here ...
    # 'while 1:' is faster than 'while True:'
    while 1:
        # Quit game if any quit conditions meat
        if quit_game:
            pygame.quit()
            sys.exit()

        # If lives remaining is zero (game over) or game finale,
        # wait until user select quit or start a new game.
        if not game.lives or game.finale:
            selection_made = False
            while not selection_made:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_game = True
                        selection_made = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            selection_made = True
                        if event.key == pygame.K_n or event.key == pygame.K_q:
                            quit_game = True
                            selection_made = True
            if not quit_game:
                game.reset_game(FIRST_LEVEL)
                game.sfx["levelclear"].play()
                game.is_game_started = True
            else:
                pygame.quit()
                sys.exit()

        # Cover screen with the default background color
        if game.season in COLORS:
            game.display.fill(COLORS[game.season])

        # Render background
        game.background.update(game.display, game.movement)
        game.background.render(game.display)

        # Shake if needed
        game.screenshake = max(0, game.screenshake - 1)

        # Level cleared? Transition to the next level!
        if game.levelcleared:
            # Play level clear sfx at the zero frame of the transition
            if game.transition == 0:
                game.sfx["levelclear"].play()
            # When it's level clear transition, black out a bit slower (+0.5)
            game.transition += 0.5
            # If transition frame > 40, load the new level.
            if game.transition > 40:
                game.level = min(game.level + 1, LAST_LEVEL_ID)
                # If the level cleared was the last stage, display_finale
                if game.level == LAST_LEVEL_ID:
                    game.finale = True
                    game.is_game_started = False
                    game.play_bgm(music_key="finale")
                else:
                    # Other than that, show level cleared message and continue
                    game.load_level(game.level)
        else:
            # For normal transition, black out will be faster (+1)
            if game.transition < 0:
                game.transition += 1

        # If player is died ... reload the level after 40 frames
        if game.dead:
            game.dead += 1
            if game.dead == 2:
                game.sfx["dead"].play()
            if game.dead >= 10:
                game.transition = min(30, game.transition + 1)
            if game.dead > 40:
                game.lives = max(0, game.lives - 1)
                # Get the closest passed checkpoint to spawn the player there.
                game.load_level(
                    game.level,
                    passed_checkpoint_pos=game.player.get_spawning_position(),
                    reset_time=False,
                )

        # Move camera focusing the center of the player
        game.scroll[0] += (
            game.player.rect().centerx
            - game.display.get_width() / 2
            + 100  # Add some offset
            - game.scroll[0]
        ) / CAMERA_SPEED
        game.scroll[1] += (
            game.player.rect().centery
            - game.display.get_height() / 2
            - 20  # Add some offset
            - game.scroll[1]
        ) / CAMERA_SPEED
        # To avoid screen ziggling, take integer of scroll
        render_scroll = (int(game.scroll[0]), int(game.scroll[1]))

        # Spawn particles - fireball. Spawners are collected in game.py
        for rect in game.fireball_spawners:
            if random.random() > (1 - FIREBALL_PROB):
                # Spawn position should be bound in the rect area
                pos = (
                    rect.centerx,
                    rect.y - 13,
                )
                game.fireballs.append(
                    Particle(
                        game,
                        "fireball",
                        pos,
                        velocity=[0, -6],
                        frame=0,
                        freefalling=True,
                    )
                )
                # Do not play sfx if it's too far away from player
                dis = game.player.pos[0] - pos[0]
                if abs(dis) < 500:
                    game.sfx["fireball"].play()

        # Spawn particles - fireswing. Spawners are collected in game.py
        # fireswing members (small fires) will be appended only one time.
        if not len(game.fireswings):
            for rect in game.fireswing_spawners:
                intial_theta = random.random() * 2
                velocity = (
                    (random.randrange(8, 12))
                    * 0.001
                    * (-1 if random.random() > 0.5 else 1)
                )
                # Length of fireswing
                for l in range(FIRESWING_LENGTH):
                    pos = (rect.centerx, rect.centery)
                    game.fireswings.append(
                        Particle(
                            game,
                            "fireswing",
                            pos,
                            angular_motion_velocity=velocity,
                            angular_motion_center=pos,
                            angular_motion_offset=l * FIRESWING_UNIT_LENGTH,
                            angular_motion_initial_theta=intial_theta,
                            frame=0,
                            freefalling=False,
                        )
                    )

        # Spawn particles - leaf. Spawners are collected in game.py
        if VISUAL_EFFECT["leaf"]:
            for rect in game.leaf_spawners:
                # Make spawn rate (probability) depends on the size of the rect
                # *1 = 100% spawning each frame
                # *49999 = small chance of spawning each frame
                if random.random() * 49999 < rect.width * rect.height:
                    # Spawn position should be bound in the rect area
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    game.particles.append(
                        Particle(
                            game,
                            "leaf",
                            pos,
                            velocity=[-0.1, 0.3],
                            frame=random.randint(0, 3),
                        )
                    )
        # Render cloud, map, and entities (enemy, player)
        if game.is_game_started:
            # Render cloud.
            if VISUAL_EFFECT["cloud"]:
                game.clouds.update()
                game.clouds.render(game.display, offset=render_scroll)

            # Render map
            game.tilemap.render(game.display, offset=render_scroll)

            # Render enemies
            for enemy in game.enemies.copy():
                kill = enemy.update(game.tilemap, (0, 0))
                enemy.render(game.display, offset=render_scroll)
                # If enemy is killed by player by dashing ... remove that enemy
                if kill:
                    game.enemies.remove(enemy)

            # Player can move around only when it's not died.
            # When died, player image won't be rendered.
            if not game.dead:
                # Update and render the player
                # If shift key is pressed (game.running = True), run!
                game.player.update(
                    game.tilemap,
                    (
                        (game.movement[1] - game.movement[0])
                        * (
                            VELOCITY["player_x_delta_run"]
                            if game.running
                            else VELOCITY["player_x_delta_walk"]
                        ),
                        0,
                    ),
                )
                # During demaging (energy is decreasing, blink player)
                if game.player.blink:
                    game.player.set_action("hit")
                    if PLAYER_BOUNCE_BACK:
                        x_dir = 1
                        # Determine the direction of bounce
                        if game.player.bounce_direction > 0:
                            x_dir = 1
                        elif game.player.bounce_direction < 0:
                            x_dir = -1
                        # If bounce_direction = 0, use flip to decide.
                        else:
                            if game.player.flip:
                                x_dir = 1
                            else:
                                x_dir = -1
                        game.player.pos = [
                            game.player.pos[0] + x_dir * (20 - game.player.blink) / 10,
                            game.player.pos[1],
                        ]
                    game.player.blink += 1
                    if int(game.time_remain / 50) % 2 == 1:
                        game.player.render(game.display, offset=render_scroll)
                    if game.player.blink > 20:
                        game.player.blink = 0
                        game.player.bounce_direction = 0
                else:
                    game.player.render(game.display, offset=render_scroll)

        # Render projectiles  [[x, y], direction, timer]
        for projectile in game.projectiles.copy():
            projectile[0][0] += projectile[1]  # Add direction to x position
            projectile[2] += 1  # Update timer
            img = game.assets["projectile"]
            game.display.blit(
                img,
                (
                    projectile[0][0] - img.get_width() / 2 - render_scroll[0],
                    projectile[0][1] - img.get_height() / 2 - render_scroll[1],
                ),
            )
            # Remove prjojectile when ...
            if game.tilemap.solid_check(projectile[0]):
                # when projectile hits walls
                game.projectiles.remove(projectile)
                # Spawn sparks
                for _ in range(4 * VISUAL_EFFECT["spark"]):
                    game.sparks.append(
                        Spark(
                            projectile[0],
                            random.random()
                            - 0.5
                            + (math.pi if projectile[1] > 0 else 0),
                            2 + random.random(),
                            size=(1, 3),
                        )
                    )
            elif projectile[2] > 300:
                # When projectile traveles too long
                game.projectiles.remove(projectile)
            elif abs(game.player.dashing) < 50:
                # when projectile collides with player not in the 10th frame of dashing
                if game.player.rect().collidepoint(projectile[0]):
                    game.projectiles.remove(projectile)
                    # Trigger blinking
                    game.player.blink += 1
                    # Mark player is died
                    # game.dead += 1
                    # Decrease player energy
                    game.player.energy = max(
                        0, game.player.energy + ENERGY["projectile"]
                    )
                    game.sfx["hit_by_fire"].play()

                    # Trigger screen shake effect
                    game.screenshake = max(16, game.screenshake)

                    # Player bounce direction.
                    # After bouncing effect is finished, main.py will update
                    # the bounce_direction with zero (0).
                    if game.player.pos[0] > (projectile[0][0] - projectile[1]):
                        game.player.bounce_direction = 1
                    else:
                        game.player.bounce_direction = -1

                    # If energy is zero, trigger death
                    if game.player.energy == 0:
                        game.dead += 1

                    # Spawn sparks
                    for _ in range(6 * VISUAL_EFFECT["spark"]):
                        angle = random.random() * math.pi * 2
                        game.sparks.append(
                            Spark(
                                game.player.rect().center,
                                angle,
                                1 + random.random(),
                                size=(1, 8),
                            )
                        )

        # Render and remove spark of projectiles
        # Spark is 'object', and the spawn, update and remove will be self managed
        for spark in game.sparks.copy():
            kill = spark.update()
            spark.render(game.display, offset=render_scroll)
            if kill:
                game.sparks.remove(spark)

        # Render particles other than fireballs
        for particle in game.particles.copy():
            kill = particle.update()
            particle.render(game.display, offset=render_scroll)
            # If particle is leaf, make it's movement back and forth in x axis
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                game.particles.remove(particle)

        # Render fireballs and fireswings
        if game.is_game_started:
            # Render fireballs
            for fireball in game.fireballs.copy():
                # If player hit fireball  ...
                if game.player.rect().collidepoint(fireball.pos):
                    game.player.blink += 1
                    # Decrease player energy
                    game.player.energy = max(0, game.player.energy + ENERGY["fireball"])
                    game.sfx["hit_by_fire"].play()
                    # Trigger screen shake effect
                    game.screenshake = max(16, game.screenshake)
                    # If energy is zero, trigger death
                    if game.player.energy == 0:
                        game.dead += 1

                kill = fireball.update()
                fireball.render(game.display, offset=render_scroll)
                # Add additional adjustment to position as needed
                # fireball.pos[0] += math.sin(fireball.animation.frame * 0.035) * 0.3
                if kill:
                    game.fireballs.remove(fireball)

            # Render fireswings
            for fireswing in game.fireswings.copy():
                # If player hit fireswing  ...
                if game.player.rect().collidepoint(fireswing.pos):
                    game.player.blink += 1
                    # Decrease player energy
                    game.player.energy = max(
                        0, game.player.energy + ENERGY["fireswing"]
                    )
                    game.sfx["hit_by_fire"].play()
                    # Trigger screen shake effect
                    game.screenshake = max(16, game.screenshake)
                    # If energy is zero, trigger death
                    if game.player.energy == 0:
                        game.dead += 1

                _ = fireswing.update()
                fireswing.render(game.display, offset=render_scroll)

        # Render textmarks - score numbers when player hit the reward items
        # Textmark is 'object', and the spawn, update and remove will be self managed
        for textmark in game.textmarks.copy():
            kill = textmark.update()
            textmark.render(game.display, offset=render_scroll)
            if kill:
                game.textmarks.remove(textmark)

        # Check key events
        quit_game = check_keyboard_input(game)

        # Transition can be rendered only when the game is ongoing or game finale.
        if (game.is_game_started and game.transition) or (
            game.finale and game.transition
        ):
            transition_surf = pygame.Surface(game.display.get_size())
            pygame.draw.circle(
                transition_surf,
                COLORS["white"],
                (game.display.get_width() // 2, game.display.get_height() // 2),
                (30 - abs(game.transition)) * 10,
            )
            transition_surf.set_colorkey(COLORS["white"])
            game.display.blit(transition_surf, (0, 0))

        # Display game status bar
        if game.is_game_started and game.lives:
            game.statusboard.render(game.display, pos=(5, 5))

        # If lives is zero, display game over screen
        if not game.lives and not game.finale:
            display_gameover(game)
            game.play_bgm(music_key="gameover")

        # If the game is not started, show intro screen
        if not game.is_game_started and not game.finale:
            display_intro(game)

        # If paused is true, pause till any key up
        if game.paused:
            display_paused(game)

        # If level is cleared, and it was not the last stage,  show level clear banner.
        # Cannot use game.finale because it's not updated yet.
        if game.levelcleared and not (game.level == LAST_LEVEL_ID):
            display_level_cleared(game)

        # If game is finished ...
        if game.finale:
            display_finale(game)

        # If shake offset is defined, apply
        screenshake_offset = (
            random.random() * game.screenshake - game.screenshake / 2,
            random.random() * game.screenshake - game.screenshake / 2,
        )
        game.screen.blit(
            pygame.transform.scale(
                game.display, game.display_sizes[game.display_size_id]
            ),
            screenshake_offset,
        )

        # Count down the time
        # Count only if the game is already started
        if game.is_game_started:
            game.time_remain = (
                game.time_limit
                - (pygame.time.get_ticks() - game.time_start)
                + (game.time_paused)
            )

        # If time remaining is -1, trigger dead.
        if game.time_remain <= 0:
            if not game.dead:
                # Trigger screen shake effect
                game.screenshake = max(16, game.screenshake)
            game.dead += 1

        # Update if score is larger than highest score
        if game.score > game.score_highest:
            game.score_highest = game.score
            save_score_highest(PATH_HIGHEST_SCORE, game.score)

        # Display all the objects, images, background, etc...
        pygame.display.update()
        game.clock.tick(FRAME_RATE)

        # If paused is true, hold screen till any key pressed
        while game.paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        quit_game = True
                        game.paused = False
                    else:
                        game.paused = False
                        game.time_paused += (
                            pygame.time.get_ticks() - game.time_right_before_pause
                        )  # ms


# This is the program entry point:
main()
