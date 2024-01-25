import arcade

from game.views.start_view import StartView
from game.views.game_view import GameView
from game.views.game_menu_view import GameMenuView
from game.views.settings_view import SettingsView
from game.constants import Constants as c


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE, resizable=True)
        self.views = {}
        self.views["game"] = GameView()
        self.views["main_menu"] = GameMenuView()
        self.views["settings"] = SettingsView()


def main():
    window = GameWindow()
    menu_view = StartView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
