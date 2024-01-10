import arcade

from ..entities.player import PlayerCharacter
from shared_constants import *


def setup(game_view):
    # Keep track of our scrolling
    game_view.view_bottom = 0
    game_view.view_left = 0

    # Create the Sprite lists
    game_view.player_list = arcade.SpriteList()

    # Name of map file to load
    map_name = "resources/maps/map_test.tmx"

    # Layer Specific Options for the Tilemap
    layer_options = {
        LAYER_FOREGROUND: {
            "use_spatial_hash": True,
        },
        LAYER_ENEMIES: {
            "use_spatial_hash": True,
        },
        LAYER_ENEMIES_BULLETS: {
            "use_spatial_hash": True,
        },
        LAYER_PLAYER_BULLETS: {
            "use_spatial_hash": True,
        },
        LAYER_SPAWN_TRIGGER: {
            "use_spatial_hash": True,
        },
        LAYER_ITEMS: {
            "use_spatial_hash": True,
        },
        LAYER_WALLS: {
            "use_spatial_hash": True,
        },
        LAYER_STUFF: {
            "use_spatial_hash": True,
        },
        LAYER_GROUND: {
            "use_spatial_hash": True,
        },
        LAYER_BACKGROUND: {
            "use_spatial_hash": True,
        }
    }

    # Read in the tiled map
    game_view.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

    # Initialize Scene with our TileMap, this will automatically add all layers
    # from the map as SpriteLists in the scene in the proper order.
    game_view.scene = arcade.Scene.from_tilemap(game_view.tile_map)

    # Add Player Spritelist before a specific layer. This will make the layer
    # be drawn AFTER the player, making it appear to be in front of the Player.
    # Setting before using scene.add_sprite allows us to define where the SpriteList
    # will be in the draw order. If we just use add_sprite, it will be appended to the
    # end of the order.
    game_view.scene.add_sprite_list_after("Player", LAYER_SPAWN_TRIGGER)

    # Set up the player, specifically placing it at these coordinates.
    game_view.player = PlayerCharacter()
    game_view.player.center_x = PLAYER_START_X
    game_view.player.center_y = PLAYER_START_Y
    game_view.player_list.append(game_view.player)
    game_view.items_hit_list = arcade.check_for_collision_with_list(game_view.player,
                                                               game_view.scene[LAYER_ITEMS])
    game_view.spawn_trigger_hit_list = arcade.check_for_collision_with_list(game_view.player,
                                                                       game_view.scene[LAYER_SPAWN_TRIGGER])
    game_view.scene.add_sprite("Player", game_view.player)

    # PHYSICS ENGINE (very basic)
    game_view.physics_engine = arcade.PhysicsEngineSimple(
        game_view.player, game_view.scene[LAYER_WALLS])
