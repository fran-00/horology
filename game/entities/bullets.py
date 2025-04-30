from arcade import Sprite, load_spritesheet

from ..constants import Constants as c


class Bullet(Sprite):

    def __init__(self, name):
        super().__init__()
        self.cur_texture_index = 0
        self.scale = c.CHARACTER_SCALING * 0.65

        tileset_path = f"resources/bullets/{name}.png"
        self.textures = load_spritesheet(
            tileset_path
        )
        # self.texture = self.textures

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture_index += 1
        if self.cur_texture_index > 6:
            self.cur_texture_index = 0
        frame = self.cur_texture_index
        # self.texture = self.textures[frame]
