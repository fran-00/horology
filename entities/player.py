import math

import arcade

from .entity import Entity
from .bullets import Bullet
from shared_constants import *


def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        super().__init__("player")

        self.mouse_left_pressed = False
        self.hp = 100
        self.max_health = self.hp
        self.cur_health = 100
        self.inventory = []
        self.score = 0

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        if not self.mouse_left_pressed:
            # Idle animation
            if self.change_x == 0 and self.change_y == 0 or UPDATES_PER_FRAME == 0:
                self.texture = self.idle_texture_pair[self.facing_direction]
                return

            else:
                self.cur_texture += 1
                if self.cur_texture > 7 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                direction = self.facing_direction

                # Walking to SOUTH
                if self.change_x == 0 and self.change_y < 0:
                    self.texture = self.walkfront_textures[frame][direction]
                # Walking to NORTH
                elif self.change_x == 0 and self.change_y > 0:
                    self.texture = self.walkback_textures[frame][direction]
                # Walking to E, W, NE, NW, SW or SE
                elif self.change_x != 0:
                    self.texture = self.walk_textures[frame][direction]
                else:
                    return

        else:
            # FIXME Fighting animation
            self.texture = self.fight_texture_pair[self.facing_direction]
            return

    def create_bullet(self, game, x, y):
        """Spawn a bullet that travels from player to target"""
        # Create a bullet
        bullet = Bullet("green")

        # Position the bullet at the player's current location
        start_x = self.center_x
        start_y = self.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # right now target's coordinates system origin is precisely the
        # bottom left angle of the viewport. Viewport follows the player..
        # IMPORTANT! If you have a scrolling screen, you will also need to
        # add in self.view_bottom and self.view_left. But HOW?
        target_x = x + game.view_left
        target_y = y + game.view_bottom

        # Calculate how to get the bullet to the destination: the angle in
        # radians between the start points and end points is the one the
        # bullet will travel: 2-argument arctangent is equal the angle
        # between the positive x axis and the ray to the point (x, y) ≠ (0, 0)
        # In our case coordinates x and y is the difference between player
        # position and the point aimed with the mouse cursor in our
        # coordinates system where 0.0 is in the bottom left of the viewport

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying sideways.
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        print(f"target_x = {target_x}, target_y = {target_y}")
        # Taking into account the angle, calculate our change_x and change_y.
        # Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        return bullet
