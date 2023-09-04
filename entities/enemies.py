import math
import arcade


ENEMY_SPEED = 0.5


class Enemy(arcade.Sprite):
    damage = 5
    hp = 10


"""
def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]



class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.damage = 5
        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SPRITE_SCALING

        # Adjust the collision box. Box is centered at sprite center, (0, 0)
        #Quadranti:      III          IV         I          II
        self.points = [[-22, -52], [22, -52], [22, 28], [-22, 28]]

        # --- Load Textures ---
        main_path = ":resources:C:/Users/Frances/groi/tiled_game/sprite_pack/enemy"

        # Load textures for idle and fighting standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_missingidle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(3):
            texture = load_texture_pair(f"{main_path}_missingwalk{i}.png")
            self.walk_textures.append(texture)



    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

"""


def follow_sprite(self, player_sprite):
    # This function will move the current sprite towards whatever other sprite is specified as a parameter.
    # We use the 'min' function here to get the sprite to line up with the target sprite, and not jump around if the sprite is not off
    # an exact multiple of SPRITE_SPEED.

    self.center_x += self.change_x
    self.center_y += self.change_y

    start_x = self.center_x
    start_y = self.center_y

    # Get the destination location for the bullet
    # probabilmente devi dirgli dove sta questa roba
    dest_x = player_sprite.center_x
    dest_y = player_sprite.center_y

    # Do math to calculate how to get the bullet to the destination. CHE CAZZO C'ENTRANO LE PALLOTTOLE???????? mmmh....
    # Calculation the angle in radians between the start points and end points. This is the angle the bullet will travel.
    x_diff = dest_x - start_x
    y_diff = dest_y - start_y
    angle = math.atan2(y_diff, x_diff)

    # Taking into account the angle, calculate our change_x and change_y. Velocity is how fast the bullet travels.
    self.change_x = math.cos(angle) * ENEMY_SPEED
    self.change_y = math.sin(angle) * ENEMY_SPEED
