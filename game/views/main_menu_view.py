import arcade
from arcade.gui import UIAnchorLayout, UIFlatButton, UIGridLayout, UIView

from ..core.setup import setup


class MainMenuView(UIView):

    def __init__(self):
        super().__init__()
        self.background_color = arcade.uicolor.BLACK

        self.grid = UIGridLayout(
            column_count=1,
            row_count=4,
            size_hint=(0, 0),
            vertical_spacing=10,
            horizontal_spacing=10,
        )

        self.ui.add(UIAnchorLayout(children=[self.grid]))
        self.add_buttons()

    def add_buttons(self):
        # NEW GAME button
        new_game_button = UIFlatButton(
            text="New Game",
            width=200,
        )
        new_game_button.on_click = self.on_click_new_game
        self.grid.add(new_game_button, row=0, column=0)

        # LOAD Button
        load_button = UIFlatButton(
            text="Load Game",
            width=200,
        )
        self.grid.add(load_button, row=1, column=0)

        # SETTINGS button
        settings_button = UIFlatButton(
            text="Settings",
            width=200,
        )
        self.grid.add(settings_button, row=2, column=0)
        settings_button.on_click = self.on_click_settings

        # QUIT button
        quit_button = UIFlatButton(
            text="Quit",
            width=200,
        )
        self.grid.add(quit_button, row=3, column=0)
        quit_button.on_click = self.on_click_quit

    # Call back methods for buttons:
    def on_click_new_game(self, event):
        self.window.show_view(self.window.views["game"])
        setup(self.window.views["game"])

    def on_click_load(self, event):
        pass

    def on_click_settings(self, event):
        self.window.show_view(self.window.views["settings"])

    def on_click_quit(self, event):
        self.window.close()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.close()
