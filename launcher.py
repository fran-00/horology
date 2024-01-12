import arcade

from game.gui.start_view import StartView
from game.constants import Constants as c


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE, resizable=True)
        self.views = {}


def main():
    window = GameWindow()
    menu_view = StartView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
