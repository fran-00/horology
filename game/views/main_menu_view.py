from arcade import View, draw_text, set_background_color
from arcade.gui import UIAnchorLayout, UIBoxLayout, UIFlatButton, UIManager
from arcade.color import BLACK, RED, WHITE
from arcade.key import ESCAPE

from ..core.setup import setup
from ..ui.buttons import ButtonStyle
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
            style=ButtonStyle().default_style
        )
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        # LOAD Button
        load_button = UIFlatButton(
            text="Load Game",
            width=200,
            style=ButtonStyle().default_style
        )
        self.v_box.add(load_button.with_space_around(bottom=20))

        # SETTINGS button
        settings_button = UIFlatButton(
            text="Settings",
            width=200,
            style=ButtonStyle().default_style
        )
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        # QUIT button
        quit_button = UIFlatButton(
            text="Quit",
            width=200,
            style=ButtonStyle().default_style
        )
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

    def on_show_view(self):
        set_background_color(BLACK)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        draw_text(
            "Is this a GAME?",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT - 100,
            WHITE,
            font_size=70,
            font_name="Kenney Pixel",
            anchor_x="center"
        )
        draw_text(
            "Yes, it is!!!",
            c.SCREEN_WIDTH / 2,
            c.SCREEN_HEIGHT - 150,
            RED,
            font_size=50,
            font_name="Kenney Pixel",
            anchor_x="center"
        )

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
