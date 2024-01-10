import arcade

from .entity import Entity
from ..constants import *


class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        super().__init__("hooded")

        self.mouse_right_pressed = False
        self.mouse_left_pressed = False
        self.hp = 100
        self.max_health = self.hp
        self.cur_health = 100
        self.inventory = []
        self.score = 0
        self.equipped_ranged_weapon = None
        self.equipped_melee_weapon = None

        self.set_sprite()
        self.set_animations()

    def set_sprite(self):
        self.sprites_path = f"resources/player/hooded/hooded"

        self.idle_texture_pair = self.load_texture_pair(f"{self.sprites_path}_idle.png")
        self.melee_attack_texture_pair = self.load_texture_pair(f"{self.sprites_path}_melee.png")
        self.ranged_attack_texture_pair = self.load_texture_pair(f"{self.sprites_path}_ranged.png")

    def set_animations(self):
        self.walk_textures = []
        for i in range(8):
            texture = self.load_texture_pair(f"{self.sprites_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for walking south
        self.walkfront_textures = []
        for i in range(8):
            texture = self.load_texture_pair(f"{self.sprites_path}_walkfront{i}.png")
            self.walkfront_textures.append(texture)

        # Load textures for walking north
        self.walkback_textures = []
        for i in range(8):
            texture = self.load_texture_pair(f"{self.sprites_path}_walkback{i}.png")
            self.walkback_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        if not self.mouse_right_pressed and not self.mouse_left_pressed:
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

        elif self.mouse_left_pressed:
            # FIXME Fighting animation
            self.texture = self.melee_attack_texture_pair[self.facing_direction]
            return

        elif self.mouse_right_pressed:
            # FIXME Fighting animation
            self.texture = self.ranged_attack_texture_pair[self.facing_direction]
            return

    def manage_equipped_weapon(self):
        pass
