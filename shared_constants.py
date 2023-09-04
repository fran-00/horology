import arcade

# Self explenatory
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Giuoco"

# Constant used to resize the screen dragging window (dividing the map with those blue dots you see).
START = 0
END = 2000
STEP = 50


# Constants used to scale our sprites from their original size
SPRITE_SCALING = 1
TILE_SCALING = 1
SPRITE_NATIVE_SIZE = 64
GRID_PIXEL_SIZE = int(SPRITE_NATIVE_SIZE * TILE_SCALING)

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
PLAYER_START_X = 64
PLAYER_START_Y = 225

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Constant for bullet that player shoots.
BULLET_SPEED = 10
SPRITE_SCALING_CURSE = 0.5


HEALTHBAR_WIDTH = 300
HEALTHBAR_HEIGHT = 50
HEALTHBAR_OFFSET_Y = -10

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

ENEMY_COUNT = 2

