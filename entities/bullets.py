import arcade

from shared_constants import *


class Bullet(arcade.Sprite):
    def __init__(self, name):
        super().__init__()

        self.cur_texture = 0
        self.scale = CHARACTER_SCALING / 2

        main_path = f"sprite_pack/bullets/{name}/{name}"

        self.bullet_textures = []
        for i in range(7):
            textures = arcade.load_texture(f"{main_path}_{i}.png")
            self.bullet_textures.append(textures)

        # Set the initial texture
        self.texture = self.bullet_textures[0]
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 6 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.bullet_textures[frame]
