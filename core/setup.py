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

    # Name of map file to load
    map_name = "map_test.tmx"

    # Layer Specific Options for the Tilemap
    layer_options = {
        LAYER_NAME_FOREGROUND: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_ENEMIES: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_SPAWN_TRIGGER: {
            "use_spatial_hash": True,
        },
        LAYER_NAME_ITEMS: {
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

    # Add Player Spritelist before a specific layer. This will make the layer
    # be drawn AFTER the player, making it appear to be in front of the Player.
    # Setting before using scene.add_sprite allows us to define where the SpriteList
    # will be in the draw order. If we just use add_sprite, it will be appended to the
    # end of the order.
    game.scene.add_sprite_list_after("Player", LAYER_NAME_SPAWN_TRIGGER)

    # Set up the player, specifically placing it at these coordinates.
    game.player = PlayerCharacter()
    game.player.center_x = PLAYER_START_X
    game.player.center_y = PLAYER_START_Y
    game.player_list.append(game.player)
    game.items_hit_list = arcade.check_for_collision_with_list(game.player,
                                                               game.scene[LAYER_NAME_ITEMS])
    game.spawn_trigger_hit_list = arcade.check_for_collision_with_list(game.player,
                                                                       game.scene[LAYER_NAME_SPAWN_TRIGGER])
    game.scene.add_sprite("Player", game.player)

    # PHYSICS ENGINE (very basic)
    game.physics_engine = arcade.PhysicsEngineSimple(
        game.player, game.scene[LAYER_NAME_WALLS])
