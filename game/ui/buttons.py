import arcade


class ButtonStyle:

    def __init__(self):
        
        self.default_style = {
            "font_name": ("Kenney Pixel"),
            "font_size": 25,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.REDWOOD,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
