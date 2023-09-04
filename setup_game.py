import os

import arcade, random
from shared_constants import SPRITE_SCALING, TILE_SCALING, PLAYER_START_X, PLAYER_START_Y, GRID_PIXEL_SIZE, MOVEMENT_SPEED
from shared_constants import SCREEN_WIDTH, SCREEN_HEIGHT

from player import ChosenOne

from ai import Enemy



# *** GAME SETUP ***
def setup(self):
    # Keep track of our scrolling
    self.view_bottom = 0
    self.view_left = 0

    # Create the Sprite lists
    self.player_list = arcade.SpriteList()
    self.bullet_list = arcade.SpriteList()
    self.foreground_list = arcade.SpriteList()
    self.background_list = arcade.SpriteList()
    self.wall_list = arcade.SpriteList()
    self.stuff_list = arcade.SpriteList()
    self.items_list = arcade.SpriteList()
    self.enemies_list = arcade.SpriteList()
    self.spawn_trigger_list = arcade.SpriteList()

    # Set up the player, specifically placing it at these coordinates.
    self.player_sprite = ChosenOne()
    self.player_sprite.center_x = PLAYER_START_X
    self.player_sprite.center_y = PLAYER_START_Y
    self.player_list.append(self.player_sprite)
    self.items_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.items_list)
    self.spawn_trigger_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.spawn_trigger_list)


    # --- Load in a map from Tiled editor ---
    foreground_layer_name = 'Foreground'
    items_layer_name = 'Items'
    spawn_trigger_layer_name = 'Spawn_trigger'
    walls_layer_name = 'Walls'
    decorative_stuff_layer_name = 'Stuff'
    ground_layer_name = 'Ground'
    background_layer_name = 'Background'

    map_name = ":resources:C:/Users/Frances/groi/tiled_game/map.tmx"
    my_map = arcade.tilemap.read_tmx(map_name)


    self.level = 1

    # Calculate the right edge of the my_map in pixels
    self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

    # *** Layers names on map list ***
    # Layer 7 -- Foreground (Environment above player)
    self.foreground_list = arcade.tilemap.process_layer(my_map,
                                                        foreground_layer_name,
                                                        TILE_SCALING)

    # Layer 6 -- Items, layer di oggetti
    self.items_list = arcade.tilemap.process_layer(my_map,
                                                   items_layer_name,
                                                   TILE_SCALING,
                                                   use_spatial_hash=True)


    # Layer 5 -- Spawn Trigger Layer
    self.spawn_trigger_list = arcade.tilemap.process_layer(my_map,
                                                     spawn_trigger_layer_name,
                                                     TILE_SCALING,
                                                     use_spatial_hash=True)
    
    # Layer 4 -- Wall (Obstacles, tiles where player can't walk on)
    self.wall_list = arcade.tilemap.process_layer(map_object=my_map,
                                                  layer_name=walls_layer_name,
                                                  scaling=TILE_SCALING,
                                                  use_spatial_hash=True)

    # Layer 3 -- Decorative stuff on the ground (flowers, rocks...)
    self.stuff_list = arcade.tilemap.process_layer(my_map,
                                                decorative_stuff_layer_name,
                                                TILE_SCALING)

    # Layer 2 -- Ground (Players walks above this ground)
    self.ground_list = arcade.tilemap.process_layer(my_map,
                                                    ground_layer_name,
                                                    TILE_SCALING)

    # Layer 1 -- Background
    self.background_list = arcade.tilemap.process_layer(my_map,
                                                        background_layer_name,
                                                        TILE_SCALING)

    # PHYSICS ENGINE (very basic)
    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


