import arcade

from .entity import Entity
from shared_constants import *


mouse_left_pressed = False


def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__("player", "player")
        
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

        if not mouse_left_pressed:
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
