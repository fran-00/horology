from arcade.color import BLACK, BULGARIAN_ROSE, WHITE


class ButtonStyle:

    def __init__(self):
        
        self.default_style = {
            "font_name": ("Kenney Pixel"),
            "font_size": 25,
            "font_color": WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": BULGARIAN_ROSE,

            # used if button is pressed
            "bg_color_pressed": WHITE,
            "border_color_pressed": WHITE,  # also used when hovered
            "font_color_pressed": BLACK,
        }
