import arcade

from ..constants import *


class Entity(arcade.Sprite):
    def __init__(self, name):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

    def load_texture_pair(self, filename):
        # Load a texture pair, with the second being a mirror image.
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True)
        ]
