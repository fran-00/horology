import arcade

from game.gui.start_view import StartView
from game.constants import Constants as c


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE, resizable=True)
        self.views = {}


def main():
    window = arcade.Window(c.SCREEN_WIDTH, c.SCREEN_HEIGHT, c.SCREEN_TITLE)
    menu_view = StartView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()
