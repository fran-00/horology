import math
import random

import arcade

import entities.player as player
import stuff

from ai import Enemy
from ai import follow_sprite
from setup_game import setup

from shared_constants import *



# >>>> *** Main APPLICATION CLASS ***
class MyGame(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # questi attributi andrebbero messi su PLAYER ma al momento funzionano solo se li metto qui.
        self.hp = 100
        self.max_health = self.hp
        self.cur_health = 100
        self.inventory = []
        self.score = 0

        # Show or don't the mouse cursor
        self.set_mouse_visible(True)
        # Used for text on screen (dialogues, not score)
        self.text_angle = 0
        self.time_elapsed = 0.0

    # -----> MANAGE WINDOW RESIZING
    # Automatically called when the window is resized.
    def on_resize(self, width, height):

        # Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    # -----> RENDER PLAYER HP NUMBER
    def draw_health_number(self):
        #Draw how many hit points we have
        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x = self.view_left + 750,
                         start_y = self.view_bottom + 0,
                         font_size = 12,
                         color = arcade.color.WHITE)

    # -----> RENDER PLAYER HP BAR
    def draw_health_bar(self):
        # Draw the red background of the bar
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x = self.view_left + 600,
                                         center_y = self.view_bottom + 10,
                                         width = HEALTHBAR_WIDTH,
                                         height = 10,
                                         color = arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)
        # Draw the green foreground of the bar
        arcade.draw_rectangle_filled(center_x = (self.view_left + 600) - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y = self.view_bottom - 10,
                                     width = health_width,
                                     height = HEALTHBAR_HEIGHT,
                                     color = arcade.color.GREEN)

    # -----> RENDER THE SCREEN
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        for y in range(START, END, STEP):
            arcade.draw_point(0, y, arcade.color.BLUE, 5)
            arcade.draw_text(f"{y}", 5, y, arcade.color.BLACK, 12, anchor_x="left", anchor_y="bottom")

        for i, x in enumerate(range(START + STEP, END, STEP), start=1):
            arcade.draw_point(x, 0, arcade.color.BLUE, 5)
            arcade.draw_text(f"{x}", x, 5, arcade.color.BLACK, 12, anchor_x="left", anchor_y="bottom")

        # -----> RENDER ALL SPRITES
        # Draw our sprites ON ORDER! Warning! If you change this order player is renderes BELOW the map. She has to be under the foreground. 
        self.background_list.draw()
        self.wall_list.draw()
        self.items_list.draw()
        self.enemies_list.draw()
        self.spawn_trigger_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.foreground_list.draw()

        self.draw_health_number()
        self.draw_health_bar()

        # Draw our Scene
        self.scene.draw()

        # -----> RENDER THE SCORE
        # Draw our SCORE on the bottom left corner of screen, scrolling it with the viewport ARGHHH
        #score_text = f"SCORE: {self.score}"
        #arcade.draw_text(score_text, 200 + self.view_left, 10 + self.view_bottom,
        #                 arcade.csscolor.WHITE, 10)


        # -----> RENDER THE INVENTORY
        start_x = self.view_left + 30
        start_y = self.view_bottom + 50
        for i, item in enumerate(self.inventory, 1):
            your_stuff = f"{i}: {item.name}\n"
            arcade.draw_text(your_stuff, start_x, start_y, arcade.csscolor.WHITE, 10, anchor_y="top")
            start_y -= 20

    # -----> MANAGE MOUSE BUTTONS PRESSED
    def on_mouse_press(self, x, y, button, modifiers):
        """ Questo serve per far muovere il giocatore al click del mouse (tasto destro)
        # FIXME funziona. Ma una volta arrivata a destinazione non si ferma!
        current_position_x = self.player_sprite.center_x
        current_position_y = self.player_sprite.center_y
        target_position_x = x + self.view_left
        target_position_y = y + self.view_bottom
        x_diff = target_position_x - current_position_x
        y_diff = target_position_y - current_position_y
        rad_angle = math.atan2(y_diff, x_diff)

        if button == arcade.MOUSE_BUTTON_RIGHT and rad_angle != 0:
            self.player_sprite.change_x = math.cos(rad_angle) * MOVEMENT_SPEED
            self.player_sprite.change_y = math.sin(rad_angle) * MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0     FIXME!! come cazzo faccio a farla fermare quando arriva???
            self.player_sprite.change_y = 0     FIXME!!
            return
        """
        # we check if left button is pressed to change player sprite to fighting version
        if button == arcade.MOUSE_BUTTON_LEFT:
            player.mouse_left_pressed = True

            # -----> BULLETS!!!
            # Create a bullet
            bullet = arcade.Sprite("sprite_pack/4dEuclideanCube.png", SPRITE_SCALING_CURSE)

            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            # TODO il proiettile viene fuori dalla mano e cambia mano in base all'orientamento della sprite di lei

  
            # Get from the mouse the destination location for the bullet
            # right now target's coordinates system origin is precisely the bottom left angle of the viewport. Viewport follows the player..
            # IMPORTANT! If you have a scrolling screen, you will also need to add in self.view_bottom and self.view_left. But HOW?
            target_x = x + self.view_left
            target_y = y + self.view_bottom

            # FIXME
            # Calculate how to get the bullet to the destination: the angle in radians between the start points and end points is the one the bullet will travel:
            # 2-argument arctangent is equal the angle between the positive x axis and the ray to the point (x, y) ≠ (0, 0)
            # In our case coordinates x and y is the difference between player position and the point aimed with the mouse cursor in our coordinates system where 0.0 is in the bottom left of the viewport

            x_diff = target_x - start_x
            y_diff = target_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying sideways.
            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            print(f"target_x = {target_x}, target_y = {target_y}")
            # Taking into account the angle, calculate our change_x and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            self.bullet_list.append(bullet)

    # -----> MANAGE MOUSE BUTTON RELEASE
    def on_mouse_release(self, x, y, button, modifiers):
        player.mouse_left_pressed = False

    # -----> MANAGE KEYS PRESSED
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    # -----> MANAGE KEYS RELEASED
    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.S]:
            self.player_sprite.change_y = 0
        elif key in [arcade.key.A, arcade.key.D]:
            self.player_sprite.change_x = 0

    # -----> MOVEMENTS AND GAME LOGIC
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update_animation()

        # USED FOR TEXT IN SCREEN (generic, not the score)
        self.text_angle += 1
        self.time_elapsed += delta_time

        # FIXME: Did the player fall off the map? Now it works only if she goes down under the map, but she can walk up, right and left forever.
        if self.player_sprite.center_y < -100:
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # *** SCREEN RENDERING ***
            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

        # Track if we need to change the viewport
        changed_viewport = False


        # *** MANAGE SCROLLING ***
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
            # Only scroll to integers. Otherwise we end up with pixels that don't line up on the screen (i think it may be quite interesting...)
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


        # ----> FIGHT!!!!

        # *** SPAWN AN ENEMY WHEN A SPAWN POINT IS TRIGGERED
        if arcade.check_for_collision_with_list(self.player_sprite,
                                                self.spawn_trigger_list):
            # for i in range(ENEMY_COUNT):                              # questo ti serve se vuoi che spawni più di un nemico
            enemy = Enemy("sprite_pack/enemy_herman.png")
            # Position the enemy at a random location
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the enemy to the lists spawning it at a random location
            self.enemies_list.append(enemy)

        # remove the spawn point triggered from sprite list
        spawn_point_touched = arcade.check_for_collision_with_list(self.player_sprite,
                                                                   self.spawn_trigger_list)
        for spawn_point in spawn_point_touched:
            spawn_point.kill()
            print("Prepare to fight! Spawn point touched!")


        # manage the following behavior (FIXME funziona male, la sprite si muove ma non segue proprio un cazzo, tende ad andare nell'angolo 
        # inferiore sx dello schermo, che è anche il punto di spawn del giocatore. sospetto che anche questo comportamento abbia a che fare
        # con la necessità di aggiungere lo scrolling ai margini nei movimenti nemici)

        player_sprite = player.PlayerCharacter()
        for enemy in self.enemies_list:
            follow_sprite(enemy, player_sprite)


        # *** BATTLE WITH AN ENEMY ***
        enemies_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.enemies_list)
        # If the player touch an ENEMY, she respawn at starting coordinates AND loses as many hp as is written on damage property (for now is under Enemy parent class).
        if self.cur_health > 0:
            for _ in enemies_hit_list:
                hp_lost = int(Enemy().damage)
                self.cur_health -= hp_lost
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y

        # *** ITEMS TO PICK UP: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH ***
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.items_list)


        for item in items_hit_list:
            # If player's health isn't full, loop through each colliding sprite, add hp_restored propriety value (int) to hp and remove item sprite from list.
            if 'hp_restore' in item.properties and self.cur_health < self.max_health:
                hp_restored = int(item.properties['hp_restore'])
                self.cur_health += hp_restored
                item.remove_from_sprite_lists()
            elif 'hp_restore' in item.properties and self.cur_health == self.max_health:
                print("your health is full")
            elif 'weapon' in item.properties:
                my_weapon = int(item.properties['weapon'])
                if my_weapon == 1:
                    self.inventory.append(stuff.Sep())
                    item.remove_from_sprite_lists()
        # FIXME **** BULLETS UPDATE ****
        self.bullet_list.update()

        for bullet in self.bullet_list:
            # Check this bullet to see if it hit an enemy or a wall
            enemy_hit_list = arcade.check_for_collision_with_list(bullet, self.enemies_list)
            wall_hit_list = arcade.check_for_collision_with_list(bullet, self.wall_list)   #sempre facente parte del FASTIDIO, rimettilo
            # If it did, get rid of the bullet
            if len(enemy_hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # remove enemy tile if a bullet hit him
            for enemy in enemy_hit_list:
                #Enemy.hp -= stuff.dmg
                #if Enemy.hp <= 0:
                enemy.remove_from_sprite_lists()
                self.score += 1

            # AAAAAAAAAAAAAAAAAAARGH, silenziato momentaneamente causa ESTREMO FASTIDIO. Funge perfettamente ma continua a ripetermi che non sto usando "stuff" e ha rotto 3/4 di minchia
            # Remove bullet if it hits an obstacle which is not an enemy:
            for _ in wall_hit_list:
                bullet.remove_from_sprite_lists()

            # Bullet will travel forever and will go out of screen without causing any harm. Let them be whatever they want to be.


# -----> MAIN METHOD
def main():
    window = MyGame()
    setup(window)
    arcade.run()