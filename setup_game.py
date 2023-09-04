import arcade

from shared_constants import TILE_SCALING, PLAYER_START_X, PLAYER_START_Y
from player import ChosenOne


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

    LAYER_NAME_FOREGROUND = 'Foreground'
    LAYER_NAME_ITEMS = 'Items'
    LAYER_NAME_SPAWN_TRIGGER = 'Spawn_trigger'
    LAYER_NAME_WALLS = 'Walls'
    LAYER_NAME_STUFF = 'Stuff'
    LAYER_NAME_GROUND = 'Ground'
    LAYER_NAME_BACKGROUND = 'Background'

    # Name of map file to load
    map_name = "map.json"

    self.level = 1

    # Layer Specific Options for the Tilemap
    layer_options = {
        LAYER_NAME_FOREGROUND: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_ITEMS: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_SPAWN_TRIGGER: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_WALLS: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_STUFF: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_GROUND: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_BACKGROUND: {
            "use_spatial_hash": True,
        }
    }

    # Read in the tiled map
    self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

    # Initialize Scene with our TileMap, this will automatically add all layers
    # from the map as SpriteLists in the scene in the proper order.
    self.scene = arcade.Scene.from_tilemap(self.tile_map)

    # PHYSICS ENGINE (very basic)
    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)
