import arcade

from entities.player import PlayerCharacter
from shared_constants import *


def setup(game):
    # Keep track of our scrolling
    game.view_bottom = 0
    game.view_left = 0

    # Create the Sprite lists
    game.player_list = arcade.SpriteList()
    game.bullet_list = arcade.SpriteList()
    game.foreground_list = arcade.SpriteList()
    game.background_list = arcade.SpriteList()
    game.wall_list = arcade.SpriteList()
    game.stuff_list = arcade.SpriteList()
    game.items_list = arcade.SpriteList()
    game.enemies_list = arcade.SpriteList()
    game.spawn_trigger_list = arcade.SpriteList()

    # Set up the player, specifically placing it at these coordinates.
    game.player_sprite = PlayerCharacter()
    game.player_sprite.center_x = PLAYER_START_X
    game.player_sprite.center_y = PLAYER_START_Y
    game.player_list.append(game.player_sprite)
    game.items_hit_list = arcade.check_for_collision_with_list(game.player_sprite,
                                                               game.items_list)
    game.spawn_trigger_hit_list = arcade.check_for_collision_with_list(game.player_sprite,
                                                                       game.spawn_trigger_list)

    # Name of map file to load
    map_name = "map.tmx"

    game.level = 1

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
    game.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

    # Initialize Scene with our TileMap, this will automatically add all layers
    # from the map as SpriteLists in the scene in the proper order.
    game.scene = arcade.Scene.from_tilemap(game.tile_map)

    # PHYSICS ENGINE (very basic)
    game.physics_engine = arcade.PhysicsEngineSimple(
        game.player_sprite, game.wall_list)
