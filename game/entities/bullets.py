import arcade

from ..constants import Constants as c


class Bullet(arcade.Sprite):
    def __init__(self, name):
        super().__init__()
        self.cur_texture_index = 0
        self.scale = c.CHARACTER_SCALING / 2

        tileset_path = f"resources/bullets/{name}.png"
        self.textures = arcade.load_spritesheet(
            tileset_path,
            sprite_width=c.SPRITE_SIZE,
            sprite_height=c.SPRITE_SIZE,
            columns=7,
            count=7,
        )
        self.texture = self.textures[0]
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1
        if self.cur_texture_index > 6:
            self.cur_texture_index = 0
        frame = self.cur_texture_index
        self.texture = self.textures[frame]
