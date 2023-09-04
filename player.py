import os

import arcade
from shared_constants import SPRITE_SCALING, RIGHT_FACING, LEFT_FACING, UPDATES_PER_FRAME



mouse_left_pressed = False


def load_texture_pair(filename):
    # Load a texture pair, with the second being a mirror image.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]

class ChosenOne(arcade.Sprite):
    def __init__(self):             # TODO add max_health as argument
        # Set up parent class
        super().__init__()



        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        self.scale = SPRITE_SCALING

        # Adjust the collision box. Box is centered at sprite center, (0, 0)
        #Quadranti:      III          IV         I          II
        self.points = [[-22, -52], [22, -52], [22, 28], [-22, 28]]

        # --- Load Textures ---
        main_path = os.path.join(os.getcwd(), "sprite_pack/pg")

        # Load textures for idle and fighting standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idlefront.png")

        self.fight_texture_pair = load_texture_pair(f"{main_path}_fight_front.png")


        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        self.walkfront_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walkfront{i}.png")
            self.walkfront_textures.append(texture)

        self.walkback_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walkback{i}.png")
            self.walkback_textures.append(texture)


    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING


        if mouse_left_pressed == False:
            # Idle animation
            if self.change_x == 0 and self.change_y == 0 or UPDATES_PER_FRAME == 0:
                self.texture = self.idle_texture_pair[self.character_face_direction]
                return

            else:
                self.cur_texture += 1
                if self.cur_texture > 7 * UPDATES_PER_FRAME:
                    self.cur_texture = 0
                frame = self.cur_texture // UPDATES_PER_FRAME
                direction = self.character_face_direction

                # Walking to SOUTH
                if self.change_x == 0 and self.change_y < 0:
                    self.texture = self.walkfront_textures[frame][direction]
                # Walking to NORTH
                elif self.change_x == 0 and self.change_y > 0:
                    self.texture = self.walkback_textures[frame][direction]
                # Walking to E, W, NE, NW, SW or SE
                elif self.change_x != 0: 
                    self.texture = self.walk_textures[frame][direction]
                else:
                    return

        elif mouse_left_pressed == True:
            # FIXME Fighting animation
            self.texture = self.fight_texture_pair[self.character_face_direction]
            return
