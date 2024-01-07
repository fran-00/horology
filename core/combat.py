import arcade

from shared_constants import *


class Combat:
    def __init__(self, view):
        self.game_view = view

    def handle_bullets_animation(self, delta_time):
        """Handle bullets animation"""
        for bullet in self.game_view.scene[LAYER_NAME_BULLETS]:
            bullet.update_animation(delta_time)

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