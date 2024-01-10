import arcade


class Constants:
    # Self explenatory
    SCREEN_WIDTH = 1366
    SCREEN_HEIGHT = 768
    SCREEN_TITLE = "Giuoco"

    # Constant used to resize the screen dragging window (dividing the map with those blue dots you see).
    START = 0
    END = 2000
    STEP = 50

    # Constants used to scale our sprites from their original size
    SPRITE_SCALING = 1
    CHARACTER_SCALING = 1
    TILE_SCALING = 1
    SPRITE_IMAGE_SIZE = 64
    GRID_PIXEL_SIZE = int(SPRITE_IMAGE_SIZE * TILE_SCALING)
    SPRITE_SIZE = int(SPRITE_IMAGE_SIZE * SPRITE_SCALING)

    # Movement speed of player, in pixels per frame
    MOVEMENT_SPEED = 7
    UPDATES_PER_FRAME = 5

    # How many pixels to keep as a minimum margin between the character and the edge of the screen.
    # Now it's always half of screen width and height so the player always stays at the center of the screen.
    LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
    RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
    BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2
    TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2

    # Player starting coordinates
    PLAYER_START_X = 327
    PLAYER_START_Y = 280

    # Constants used to track if the player is facing left or right
    RIGHT_FACING = 0
    LEFT_FACING = 1

    # Constant for bullet that player shoots.
    BULLET_SPEED = 10
    SPRITE_SCALING_CURSE = 0.5

    # Health bar
    HEALTHBAR_WIDTH = 300
    HEALTHBAR_HEIGHT = 50
    HEALTHBAR_OFFSET_Y = -10

    HEALTH_NUMBER_OFFSET_X = -10
    HEALTH_NUMBER_OFFSET_Y = -25

    ENEMY_COUNT = 2
    ENEMY_SPEED = 0.5

    LAYER_FOREGROUND = 'Foreground'
    LAYER_ENEMIES = 'Enemies'
    LAYER_PLAYER_BULLETS = 'Player_Bullets'
    LAYER_ENEMIES_BULLETS = 'Enemies_Bullets'
    LAYER_SPAWN_TRIGGER = 'Spawn_trigger'
    LAYER_ITEMS = 'Items'
    LAYER_WALLS = 'Walls'
    LAYER_STUFF = 'Stuff'
    LAYER_GROUND = 'Ground'
    LAYER_BACKGROUND = 'Background'

    MINIMAP_BACKGROUND_COLOR = arcade.get_four_byte_color(arcade.color.ALMOND)
    MINIMAP_WIDTH = 300
    MINIMAP_HEIGHT = 300
    MAP_WIDTH = 1024
    MAP_HEIGHT = 1024
