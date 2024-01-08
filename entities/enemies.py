import math

import arcade

from .entity import Entity
from shared_constants import *


class EnemySprite(Entity):
    def __init__(self, name):

        super().__init__(name)
        self.name = name
        self.set_sprite()
        self.set_animations()

    def set_sprite(self):
        self.sprites_path = f"sprite_pack/enemies/{self.name}/{self.name}"

        self.idle_texture_pair = self.load_texture_pair(f"{self.sprites_path}_idle.png")
        self.fight_texture_pair = self.load_texture_pair(f"{self.sprites_path}_fight.png")

    def set_animations(self):
        self.walk_textures = []
        for i in range(5):
            texture = self.load_texture_pair(f"{self.sprites_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for walking south
        self.walkfront_textures = []
        for i in range(5):
            texture = self.load_texture_pair(f"{self.sprites_path}_walkfront{i}.png")
            self.walkfront_textures.append(texture)

        # Load textures for walking north
        self.walkback_textures = []
        for i in range(5):
            texture = self.load_texture_pair(f"{self.sprites_path}_walkback{i}.png")
            self.walkback_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0 or UPDATES_PER_FRAME == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        else:
            self.cur_texture += 1
            if self.cur_texture > 4 * UPDATES_PER_FRAME:
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


class EnemyCharacter(EnemySprite):
    def __init__(self, name, hp, damage, player, wall_list):

        super().__init__(name)

        self.player = player
        self.name = name
        self.hp = hp
        self.damage = damage
        self.wall_list = wall_list
        self.path = None
        self.frame_count = 0
        
        playing_field_left_boundary = -SPRITE_SIZE * 50
        playing_field_right_boundary = SPRITE_SIZE * 50
        playing_field_top_boundary = SPRITE_SIZE * 50
        playing_field_bottom_boundary = -SPRITE_SIZE * 50
        
        self.barrier_list = arcade.AStarBarrierList(self,
                                                    self.wall_list,
                                                    SPRITE_SIZE,
                                                    playing_field_left_boundary,
                                                    playing_field_right_boundary,
                                                    playing_field_bottom_boundary,
                                                    playing_field_top_boundary)

    def update_path(self, delta_time):
        self.path = arcade.astar_calculate_path(self.position,
                                                self.player.position,
                                                self.barrier_list,
                                                diagonal_movement=True)
        if self.path:
            arcade.draw_line_strip(self.path, arcade.color.BLUE, 2)
        
        if self.path and len(self.path) > 1:
            if self.center_x < self.path[1][0]:
                self.center_x += min(ENEMY_SPEED, self.path[1][0] - self.center_x)
                self.change_x = -ENEMY_SPEED
            elif self.center_x > self.path[1][0]:
                self.center_x -= min(ENEMY_SPEED, self.center_x - self.path[1][0])
                self.change_x = ENEMY_SPEED

            if self.center_y < self.path[1][1]:
                self.center_y += min(ENEMY_SPEED, self.path[1][1] - self.center_y)
                self.change_y = -ENEMY_SPEED
            elif self.center_y > self.path[1][1]:
                self.center_y -= min(ENEMY_SPEED, self.center_y - self.path[1][1])
                self.change_y = ENEMY_SPEED
        else:
            self.change_x = 0
            self.change_y = 0
