import math

import arcade

from entities.bullets import Bullet
from shared_constants import *


class Combat:
    def __init__(self, view):
        self.game_view = view

    def handle_bullets_animation(self, delta_time):
        """Handle bullets animation"""
        for bullet in self.game_view.scene[LAYER_NAME_BULLETS]:
            bullet.update_animation(delta_time)

    def create_bullet_from_player(self, player, x, y):
        """Spawn a bullet that travels from player to target"""
        # Create a bullet
        bullet = Bullet("red")

        # Position the bullet at the player's current location
        start_x = player.center_x
        start_y = player.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        # right now target's coordinates system origin is precisely the
        # bottom left angle of the viewport. Viewport follows the player..
        # IMPORTANT! If you have a scrolling screen, you will also need to
        # add in self.view_bottom and self.view_left. But HOW?
        target_x = x + self.game_view.view_left
        target_y = y + self.game_view.view_bottom

        # Calculate how to get the bullet to the destination: the angle in
        # radians between the start points and end points is the one the
        # bullet will travel: 2-argument arctangent is equal the angle
        # between the positive x axis and the ray to the point (x, y) ≠ (0, 0)
        # In our case coordinates x and y is the difference between player
        # position and the point aimed with the mouse cursor in our
        # coordinates system where 0.0 is in the bottom left of the viewport

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying sideways.
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        print(f"target_x = {target_x}, target_y = {target_y}")
        # Taking into account the angle, calculate our change_x and change_y.
        # Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        return bullet

    def create_bullet_from_enemy(self, enemy, delta_time):
        """Spawn a bullet that travels from enemy to player"""
        enemy.frame_count += 1

        start_x = enemy.center_x
        start_y = enemy.center_y

        target_x = self.game_view.player.center_x
        target_y = self.game_view.player.center_y

        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)

        if enemy.frame_count % 60 == 0:
            bullet = arcade.Sprite("sprite_pack/4dEuclideanCube.png", SPRITE_SCALING_CURSE)
            bullet.center_x = start_x
            bullet.center_y = start_y

            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            return bullet

    def update_bullets(self):
        """Handle bullets update"""
        self.game_view.scene[LAYER_NAME_BULLETS].update()

        for bullet in self.game_view.scene[LAYER_NAME_BULLETS]:
            # Check this bullet to see if it hit an enemy or a wall
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, self.game_view.scene[LAYER_NAME_ENEMIES])
            wall_hit_list = arcade.check_for_collision_with_list(
                bullet, self.game_view.scene[LAYER_NAME_WALLS])
            # If it did, get rid of the bullet
            # if len(enemy_hit_list) > 0:
            #     bullet.remove_from_sprite_lists()

            # # remove enemy tile if a bullet hit him
            # for enemy in enemy_hit_list:
            #     # Enemy.hp -= stuff.dmg
            #     # if Enemy.hp <= 0:
            #     enemy.remove_from_sprite_lists()

            # Remove bullet if it hits an obstacle which is not an enemy:
            for _ in wall_hit_list:
                bullet.remove_from_sprite_lists()
            # Now bullet will travel forever and will go out of screen