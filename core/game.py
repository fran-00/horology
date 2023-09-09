import math
import random

import arcade

import stuff
from entities.enemies import EnemyCharacter
from core.setup import setup
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

    def on_resize(self, width, height):
        """Handle window resizing"""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def draw_health_number(self):
        """Render player HP number"""
        # Draw how many hit points we have
        health_string = f"{self.player_sprite.cur_health}/{self.player_sprite.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.view_left + 750,
                         start_y=self.view_bottom + 0,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """Render player HP bar"""
        # Draw the red background of the bar
        if self.player_sprite.cur_health < self.player_sprite.max_health:
            arcade.draw_rectangle_filled(center_x=self.view_left + 600,
                                         center_y=self.view_bottom + 10,
                                         width=HEALTHBAR_WIDTH,
                                         height=10,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.player_sprite.cur_health / self.player_sprite.max_health)
        # Draw the green foreground of the bar
        arcade.draw_rectangle_filled(center_x=(self.view_left + 600) - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.view_bottom - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

    def on_draw(self):
        """Render the screen"""

        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()

        self.draw_health_number()
        self.draw_health_bar()

        # -----> RENDER ENTITIES
        self.enemies_list.draw()
        self.bullet_list.draw()

        # -----> RENDER THE INVENTORY
        start_x = self.view_left + 30
        start_y = self.view_bottom + 50
        for i, item in enumerate(self.player_sprite.inventory, 1):
            your_stuff = f"{i}: {item.name}\n"
            arcade.draw_text(your_stuff, start_x, start_y,
                             arcade.csscolor.WHITE, 10, anchor_y="top")
            start_y -= 20

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse buttons pressed"""
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.move_on_mouse_click(x, y)

        # we check if left button is pressed to change player sprite to fighting version
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.mouse_left_pressed = True
            
            bullet = self.create_bullet(x, y)
            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)
    
    def move_on_mouse_click(self, x, y):
        # Questo serve per far muovere il giocatore al click del mouse (tasto destro)
        # FIXME: Player must stop when target position is reached or when they
        # hit a wall
        current_position_x = self.player_sprite.center_x
        current_position_y = self.player_sprite.center_y
        target_position_x = x + self.view_left
        target_position_y = y + self.view_bottom
        x_diff = target_position_x - current_position_x
        y_diff = target_position_y - current_position_y
        rad_angle = math.atan2(y_diff, x_diff)

        if rad_angle != 0 and x != current_position_x and y != current_position_y:
            self.player_sprite.change_x = math.cos(rad_angle) * MOVEMENT_SPEED
            self.player_sprite.change_y = math.sin(rad_angle) * MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            return

    def create_bullet(self, x, y):
        """Spawn a bullet that travels from player to target"""
        # Create a bullet
        bullet = arcade.Sprite(
            "sprite_pack/4dEuclideanCube.png", SPRITE_SCALING_CURSE)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y
        # TODO il proiettile viene fuori dalla mano e cambia mano in base all'orientamento della sprite di lei

        # Get from the mouse the destination location for the bullet
        # right now target's coordinates system origin is precisely the
        # bottom left angle of the viewport. Viewport follows the player..
        # IMPORTANT! If you have a scrolling screen, you will also need to
        # add in self.view_bottom and self.view_left. But HOW?
        target_x = x + self.view_left
        target_y = y + self.view_bottom

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

    def on_mouse_release(self, x, y, button, modifiers):
        """Handle mouse button release"""
        self.player_sprite.mouse_left_pressed = False

    def on_key_press(self, key, modifiers):
        """Handle Keys Pressed"""
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Handle Keys Released """
        if key in [arcade.key.W, arcade.key.S]:
            self.player_sprite.change_y = 0
        elif key in [arcade.key.A, arcade.key.D]:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Handle movements and game logic"""
        self.physics_engine.update()
        self.player_list.update_animation()

        # USED FOR TEXT IN SCREEN (generic, not the score)
        self.text_angle += 1
        self.time_elapsed += delta_time

        # Did the player fall off the map? Now it works only if she goes
        # down under the map, but she can walk up, right and left forever.
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # *** SCREEN RENDERING ***
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        self.manage_scrolling()
        self.spawn_enemies()
        self.get_damage_from_enemy()
        self.pick_up_items()
        self.update_bullets()

    def manage_scrolling(self):
        """Handle viewport scrolling"""

        # Track if we need to change the viewport
        changed_viewport = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
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

    def spawn_enemies(self):
        """Spawn an enemy when a spawn point is triggered"""
        spawn_points_touched_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                         self.scene[LAYER_NAME_SPAWN_TRIGGER])
        if spawn_points_touched_list != []:
            for spawn_point in spawn_points_touched_list:
                enemy_name = spawn_point.properties["name"]
                enemy_hp = spawn_point.properties["hp"]
                enemy_damage = spawn_point.properties["damage"]
                # remove the spawn point triggered from sprite list
                spawn_point.kill()
                print("Prepare to fight! Spawn point touched!")

            enemy = EnemyCharacter(enemy_name, enemy_hp, enemy_damage, self.player_sprite, self.scene[LAYER_NAME_WALLS])
            # Position the enemy 100 pixels away horizontally
            enemy.center_x = spawn_point.center_x + 100
            enemy.center_y = spawn_point.center_y

            # Add the enemy to the lists spawning it at a random location
            self.enemies_list.append(enemy)

        # manage the following behavior
        for enemy in self.enemies_list:
            enemy.follow_sprite(self.player_sprite)

    def get_damage_from_enemy(self):
        """Handle fights with enemies"""
        enemies_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                self.enemies_list)
        # If the player touch an ENEMY, she respawn at starting coordinates AND
        # loses as many hp as is written on damage property (for now is under Enemy parent class).
        if self.player_sprite.cur_health > 0:
            for enemy in enemies_hit_list:
                hp_lost = int(enemy.damage)
                self.player_sprite.cur_health -= hp_lost
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

    def pick_up_items(self):
        """Handle pick up items: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH"""
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.scene[LAYER_NAME_ITEMS])

        for item in items_hit_list:
            # If player's health isn't full, loop through each colliding sprite,
            # add hp_restored propriety value (int) to hp and remove item sprite from list.
            if 'hp_restore' in item.properties and self.player_sprite.cur_health < self.player_sprite.max_health:
                hp_restored = int(item.properties['hp_restore'])
                self.player_sprite.cur_health += hp_restored
                item.remove_from_sprite_lists()
            elif 'hp_restore' in item.properties and self.player_sprite.cur_health == self.player_sprite.max_health:
                print("your health is full")
            elif 'weapon' in item.properties:
                my_weapon = int(item.properties['weapon'])
                if my_weapon == 1:
                    self.player_sprite.inventory.append(stuff.Sep())
                    item.remove_from_sprite_lists()

    def update_bullets(self):
        """Handle bullets update"""
        self.bullet_list.update()

        for bullet in self.bullet_list:
            # Check this bullet to see if it hit an enemy or a wall
            enemy_hit_list = arcade.check_for_collision_with_list(
                bullet, self.enemies_list)
            wall_hit_list = arcade.check_for_collision_with_list(
                bullet, self.scene[LAYER_NAME_WALLS])
            # If it did, get rid of the bullet
            if len(enemy_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # remove enemy tile if a bullet hit him
            for enemy in enemy_hit_list:
                # Enemy.hp -= stuff.dmg
                # if Enemy.hp <= 0:
                enemy.remove_from_sprite_lists()
                self.score += 1

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
