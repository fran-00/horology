import arcade
from arcade.gui import UIAnchorLayout, UIFlatButton, UIGridLayout, UIView

from .main_menu_view import MainMenuView


class SettingsView(UIView):

    def __init__(self):
        super().__init__()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MainMenuView())
