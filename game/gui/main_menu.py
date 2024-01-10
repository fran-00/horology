import arcade

from ..core.game_view import GameView
from ..core.setup import setup
from ..constants import Constants as c


class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Is this a GAME?", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Yes, it is!!!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 40,
                         arcade.color.RED, font_size=20, anchor_x="center")
        arcade.draw_text("Click to start the game!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT / 2 - 70,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        setup(game_view)
        self.window.show_view(game_view)
