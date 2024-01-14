import math

import arcade

from ..entities.bullets import Bullet
from ..constants import Constants as c


class Combat:
    def __init__(self, view):
        self.game_view = view

    def handle_bullets_animation(self, delta_time):
        """Handle bullets animation"""
        for player_bullet in self.game_view.scene[c.LAYER_PLAYER_BULLETS]:
            player_bullet.update_animation(delta_time)

        for enemies_bullet in self.game_view.scene[c.LAYER_ENEMIES_BULLETS]:
            enemies_bullet.update_animation(delta_time)

    def create_bullet_from_player(self, player, x, y):
        """Spawn a bullet that travels from player to target"""
        # Create a bullet
        bullet = Bullet(player.equipped_ranged_weapon.name)

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
        bullet.change_x = math.cos(angle) * c.BULLET_SPEED
        bullet.change_y = math.sin(angle) * c.BULLET_SPEED

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
            bullet = arcade.Sprite(
                    filename="resources/4dEuclideanCube.png",
                    scale=0.5)
            bullet.center_x = start_x
            bullet.center_y = start_y

            bullet.angle = math.degrees(angle)
            bullet.change_x = math.cos(angle) * c.BULLET_SPEED
            bullet.change_y = math.sin(angle) * c.BULLET_SPEED

            return bullet

    def update_bullets(self):
        """Handle bullets update"""
        self.game_view.scene[c.LAYER_PLAYER_BULLETS].update()
        self.game_view.scene[c.LAYER_ENEMIES_BULLETS].update()

        for bullet in self.game_view.scene[c.LAYER_PLAYER_BULLETS]:
            # Check this bullet to see if it hit an enemy or a wall
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, self.game_view.scene[c.LAYER_ENEMIES])
            wall_hit_list = arcade.check_for_collision_with_list(
                bullet, self.game_view.scene[c.LAYER_WALLS])
            # If it did, get rid of the bullet
            if len(enemy_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            self.damage_enemy(enemy_hit_list, self.game_view.player.equipped_ranged_weapon)

            # Remove bullet if it hits an obstacle which is not an enemy:
            for _ in wall_hit_list:
                bullet.remove_from_sprite_lists()
            
            self.remove_far_bullets(bullet)

    def remove_far_bullets(self, bullet):
        """Delete bullets to prevent them from travelling forever and go out of screen"""
        if ((bullet.center_y > self.game_view.player.center_y + 400)
                or (bullet.center_y < self.game_view.player.center_y - 400)
                or (bullet.center_x > self.game_view.player.center_x + 400)
                or (bullet.center_x < self.game_view.player.center_x - 400)):
            bullet.remove_from_sprite_lists()

    def update_melee_attacks(self):
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.game_view.player, self.game_view.scene[c.LAYER_ENEMIES])
        self.damage_enemy(enemy_hit_list, self.game_view.player.equipped_melee_weapon)

    def damage_enemy(self, enemy_hit_list, weapon):
        for enemy in enemy_hit_list:
            enemy.hp -= weapon.damage
            if enemy.hp <= 0:
                enemy.kill()
            else:
                print(f"Enemy has {enemy.hp} remaining.")
