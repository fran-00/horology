import arcade

from shared_constants import *


def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class Entity(arcade.Sprite):
    def __init__(self, name):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f"sprite_pack/animated_entities/{name}/{name}"

        # Load textures for idle and fighting standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idlefront.png")
        
        self.fight_texture_pair = load_texture_pair(f"{main_path}_fightfront.png")

        # Load textures for walking east/west
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for walking south
        self.walkfront_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walkfront{i}.png")
            self.walkfront_textures.append(texture)

        # Load textures for walking north
        self.walkback_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walkback{i}.png")
            self.walkback_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)
