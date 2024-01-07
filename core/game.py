import math
import random

import arcade

import stuff
from entities.enemies import EnemyCharacter
from .setup import setup
from .hud import Hud
from .enemy_ai import EnemyAI
from shared_constants import *


class GameView(arcade.View):
    """Main application class"""

    def __init__(self):

        super().__init__()

        # Show or don't the mouse cursor
        self.window.set_mouse_visible(True)
        # Used for text on screen (dialogues, not score)
        self.text_angle = 0
        self.time_elapsed = 0.0
        self.hud = Hud(self)
        self.enemy_ai = EnemyAI(self)

    def on_resize(self, width, height):
        """Handle window resizing"""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def on_draw(self):
        """Render the screen"""
        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()
        
        # Draw other stuff
        self.hud.draw_health_number()
        self.hud.draw_health_bar()
        self.hud.draw_inventory()
        self.draw_A_star_paths()

    def draw_A_star_paths(self):
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            if enemy.path:
                arcade.draw_line_strip(enemy.path, arcade.color.BLUE, 2)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse buttons pressed"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            # TODO: Melee attack
            pass

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player.mouse_left_pressed = True
            bullet = self.player.create_bullet(self, x, y)
            self.scene[LAYER_NAME_BULLETS].append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        self.player.mouse_left_pressed = False

    def on_key_press(self, key, modifiers):
        """Handle Keys Pressed"""
        if key == arcade.key.W:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Handle Keys Released """
        if key in [arcade.key.W, arcade.key.S]:
            self.player.change_y = 0
        elif key in [arcade.key.A, arcade.key.D]:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Handle movements and game logic"""
        self.physics_engine.update()
        self.player_list.update_animation()

        # USED FOR TEXT IN SCREEN (generic, not the score)
        self.text_angle += 1
        self.time_elapsed += delta_time

        # Did the player fall off the map? Now it works only if she goes
        # down under the map, but she can walk up, right and left forever.
        if self.player.center_y < -100:
            self.player.center_x = PLAYER_START_X
            self.player.center_y = PLAYER_START_Y

            # *** SCREEN RENDERING ***
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # Update game state calling other methods
        self.manage_scrolling()
        self.spawn_enemies()
        self.get_damage_from_enemy()
        self.pick_up_items()
        self.update_bullets()
        self.handle_bullets_animation(delta_time)
        self.enemy_ai.handle_enemies_animation(delta_time)
        self.enemy_ai.handle_enemies_following_behaviour(delta_time)
        self.enemy_ai.handle_enemies_shooting(delta_time)

    def handle_bullets_animation(self, delta_time):
        """Handle bullets animation"""
        for bullet in self.scene[LAYER_NAME_BULLETS]:
            bullet.update_animation(delta_time)

    def manage_scrolling(self):
        """Handle viewport scrolling"""

        # Track if we need to change the viewport
        changed_viewport = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen (i think it may be quite interesting...)
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def pick_up_items(self):
        """Handle pick up items: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH"""
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.player,
                                                              self.scene[LAYER_NAME_ITEMS])

        for item in items_hit_list:
            # If player's health isn't full, loop through each colliding sprite,
            # add hp_restored propriety value (int) to hp and remove item sprite from list.
            if 'hp_restore' in item.properties and self.player.cur_health < self.player.max_health:
                hp_restored = int(item.properties['hp_restore'])
                self.player.cur_health += hp_restored
                item.remove_from_sprite_lists()
            elif 'hp_restore' in item.properties and self.player.cur_health == self.player.max_health:
                print("your health is full")
            elif 'weapon' in item.properties:
                my_weapon = int(item.properties['weapon'])
                if my_weapon == 1:
                    self.player.inventory.append(stuff.Sep())
                    item.remove_from_sprite_lists()

    def update_bullets(self):
        """Handle bullets update"""
        self.scene[LAYER_NAME_BULLETS].update()

        for bullet in self.scene[LAYER_NAME_BULLETS]:
            # Check this bullet to see if it hit an enemy or a wall
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, self.scene[LAYER_NAME_ENEMIES])
            wall_hit_list = arcade.check_for_collision_with_list(
                bullet, self.scene[LAYER_NAME_WALLS])
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


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    setup(start_view)
    arcade.run()
