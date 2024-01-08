import arcade

from core.game import GameView
from core.setup import setup
from shared_constants import *


class MainMenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Is this a GAME?", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Yes, it is!!!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                         arcade.color.RED, font_size=20, anchor_x="center")
        arcade.draw_text("Click to start the game!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        setup(game_view)
        self.window.show_view(game_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()
