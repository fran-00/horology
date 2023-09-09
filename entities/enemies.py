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

    def follow_sprite(self):
        # This function will move the current sprite towards whatever other sprite is specified as a parameter.
        # We use the 'min' function here to get the sprite to line up with the target sprite, and not jump around if the sprite is not off
        # an exact multiple of SPRITE_SPEED.

        self.center_x += self.change_x
        self.center_y += self.change_y

        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        # probabilmente devi dirgli dove sta questa roba
        dest_x = self.player.center_x
        dest_y = self.player.center_y

        # Do math to calculate how to get the bullet to the destination. CHE CAZZO C'ENTRANO LE PALLOTTOLE???????? mmmh....
        # Calculation the angle in radians between the start points and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * ENEMY_SPEED
        self.change_y = math.sin(angle) * ENEMY_SPEED
