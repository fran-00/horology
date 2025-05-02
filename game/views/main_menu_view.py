from arcade import View, draw_text, set_background_color
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIFlatButton, UIManager
from arcade.color import BLACK, RED, WHITE
from arcade.key import ESCAPE

from ..core.setup import setup
from ..constants import Constants as c


class MainMenuView(View):

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
        if key == ESCAPE:
            self.window.close()
