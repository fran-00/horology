import arcade

from ..ui.buttons import ButtonStyle
from ..constants import Constants as c


class StartView(arcade.View):

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        self.add_buttons()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.draw_text("Is this a GAME?", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, font_name="Kenney Pixel", anchor_x="center")
        arcade.draw_text("Yes, it is!!!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 40,
                         arcade.color.RED, font_size=20, font_name="Kenney Pixel", anchor_x="center")
        arcade.draw_text("Click to start the game!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 70,
                         arcade.color.GRAY, font_size=20, font_name="Kenney Pixel", anchor_x="center")
