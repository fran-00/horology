import arcade
from arcade.gui import UIAnchorLayout, UIFlatButton, UIGridLayout, UIView

from ..core.setup import setup


class MainMenuView(UIView):

    def __init__(self):
        super().__init__()

        self.manager = UIManager()
        self.v_box = UIBoxLayout()
        # self.add_buttons()
        self.manager.add(
            UIAnchorLayout(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def add_buttons(self):
        # NEW GAME button
        new_game_button = UIFlatButton(
            text="New Game",
            width=200,
        )
        self.v_box.add(new_game_button)
        new_game_button.on_click = self.on_click_new_game

        # LOAD Button
        load_button = UIFlatButton(
            text="Load Game",
            width=200,
        )
        self.v_box.add(load_button)

        # SETTINGS button
        settings_button = UIFlatButton(
            text="Settings",
            width=200,
        )
        self.v_box.add(settings_button)
        settings_button.on_click = self.on_click_settings

        # QUIT button
        quit_button = UIFlatButton(
            text="Quit",
            width=200,
        )
        self.v_box.add(quit_button)
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
