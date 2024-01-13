import arcade

from ..ui.hud import Hud
from ..systems.enemy_ai import EnemyAI
from ..systems.combat import Combat
from ..systems.inventory_system import InventorySystem
from ..constants import Constants as c


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
        self.inventory_system = InventorySystem(self)
        self.selected_item = 1

    def on_resize(self, width, height):
        """Handle window resizing"""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def on_draw(self):
        """Render the screen"""
        # Clear the screen to the background color and draw scene
        self.clear()
        self.scene.draw()

        # Draw other stuff
        self.hud.draw_health_number()
        self.hud.draw_health_bar()
        self.hud.draw_inventory()
        self.enemy_ai.draw_A_star_paths()

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse buttons pressed"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            if not self.player.equipped_melee_weapon:
                print("You have no melee weapons")
                return
            self.player.mouse_left_pressed = True
            self.combat.update_melee_attacks()

        if button == arcade.MOUSE_BUTTON_RIGHT:
            if not self.player.equipped_ranged_weapon:
                print("You have no ranged weapons")
                return
            self.player.mouse_right_pressed = True
            bullet = self.combat.create_bullet_from_player(self.player, x, y)
            self.scene[c.LAYER_PLAYER_BULLETS].append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        self.player.mouse_right_pressed = False
        self.player.mouse_left_pressed = False

    def on_key_press(self, key, modifiers):
        """Handle Keys Pressed"""
        if key == arcade.key.W:
            self.player.change_y = c.MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -c.MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -c.MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player.change_x = c.MOVEMENT_SPEED
        elif key == arcade.key.E:
            self.inventory_system.pick_up_items()
        elif key == arcade.key.I:
            # TODO: show inventory modal
            pass
        elif key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
        elif key == arcade.key.KEY_1:
            self.selected_item = 1
            self.inventory_system.change_equipped_weapon(1)
        elif key == arcade.key.KEY_2:
            self.selected_item = 2
            self.inventory_system.change_equipped_weapon(2)
        elif key == arcade.key.KEY_3:
            self.selected_item = 3
            self.inventory_system.change_equipped_weapon(3)
        elif key == arcade.key.KEY_4:
            self.selected_item = 4
            self.inventory_system.change_equipped_weapon(4)
        elif key == arcade.key.KEY_5:
            self.selected_item = 5
            self.inventory_system.change_equipped_weapon(5)
        elif key == arcade.key.KEY_6:
            self.selected_item = 6
            self.inventory_system.change_equipped_weapon(6)
        elif key == arcade.key.KEY_7:
            self.selected_item = 7
            self.inventory_system.change_equipped_weapon(7)
        elif key == arcade.key.KEY_8:
            self.selected_item = 8
            self.inventory_system.change_equipped_weapon(8)
        elif key == arcade.key.KEY_9:
            self.selected_item = 9
            self.inventory_system.change_equipped_weapon(9)
        elif key == arcade.key.KEY_0:
            self.selected_item = 10
            self.inventory_system.change_equipped_weapon(10)

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
        left_boundary = self.view_left + c.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + c.SCREEN_WIDTH - c.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + c.SCREEN_HEIGHT - c.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + c.BOTTOM_VIEWPORT_MARGIN
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
                                c.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                c.SCREEN_HEIGHT + self.view_bottom)

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
            self.player.center_x = c.PLAYER_START_X
            self.player.center_y = c.PLAYER_START_Y

            # *** SCREEN RENDERING ***
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # Update game state calling other methods
        self.manage_scrolling()
        self.enemy_ai.spawn_enemies()
        self.enemy_ai.get_damage_from_enemy()
        self.combat.update_bullets()
        self.combat.handle_bullets_animation(delta_time)
        self.enemy_ai.handle_enemies_animation(delta_time)
        self.enemy_ai.handle_enemies_following_behaviour(delta_time)
        self.enemy_ai.handle_enemies_shooting(delta_time)
