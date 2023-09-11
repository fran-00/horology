import math

import arcade

from .entity import Entity
from shared_constants import *


class EnemySprite(Entity):
    def __init__(self, name_folder, name_file):

        # Setup parent class
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class EnemyCharacter(EnemySprite):
    def __init__(self, name, hp, damage, player, wall_list):

        super().__init__(name, name)

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

    def shoot_at_player(self, delta_time):
        """Spawn a bullet that travels from enemy to player"""
        self.frame_count += 1

        start_x = self.center_x
        start_y = self.center_y

        target_x = self.player.center_x
        target_y = self.player.center_y

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        if self.frame_count % 60 == 0:
            bullet = arcade.Sprite("sprite_pack/4dEuclideanCube.png", SPRITE_SCALING_CURSE)
            bullet.center_x = start_x
            bullet.center_y = start_y

            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED
            
            return bullet

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
            elif self.center_x > self.path[1][0]:
                self.center_x -= min(ENEMY_SPEED, self.center_x - self.path[1][0])

            if self.center_y < self.path[1][1]:
                self.center_y += min(ENEMY_SPEED, self.path[1][1] - self.center_y)
            elif self.center_y > self.path[1][1]:
                self.center_y -= min(ENEMY_SPEED, self.center_y - self.path[1][1])
