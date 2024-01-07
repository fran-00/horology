import arcade

from .setup import setup
from gui.hud import Hud
from .utils.enemy_ai import EnemyAI
from .utils.combat import Combat
from .utils.inventory import Inventory
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
        self.combat = Combat(self)
        self.inventory = Inventory(self)

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
        self.enemy_ai.draw_A_star_paths()

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse buttons pressed"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.mouse_left_pressed = True
            # TODO: Melee attack
            pass

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.player.mouse_right_pressed = True
            if not self.player.equipped_weapon:
                print("You have no weapons")
                return
            bullet = self.combat.create_bullet_from_player(self.player, x, y)
            self.scene[LAYER_PLAYER_BULLETS].append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        self.player.mouse_right_pressed = False
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
        self.enemy_ai.spawn_enemies()
        self.enemy_ai.get_damage_from_enemy()
        self.inventory.pick_up_items()
        self.combat.update_bullets()
        self.combat.handle_bullets_animation(delta_time)
        self.enemy_ai.handle_enemies_animation(delta_time)
        self.enemy_ai.handle_enemies_following_behaviour(delta_time)
        self.enemy_ai.handle_enemies_shooting(delta_time)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    setup(start_view)
    arcade.run()
