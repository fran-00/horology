import arcade

from game.views.start_view import StartView
from game.views.main_menu import MainMenuView
from game.constants import Constants as c


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE, resizable=True)
        self.views = {}
        self.views["main_menu"] = MainMenuView()


def main():
    window = GameWindow()
    menu_view = StartView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
