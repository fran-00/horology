import arcade

from ..core.setup import setup
from ..ui.buttons import ButtonStyle
from ..constants import Constants as c


class StartView(arcade.View):

    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        self.add_buttons()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def add_buttons(self):
        # NEW GAME button
        new_game_button = arcade.gui.UIFlatButton(text="New Game",
                                                  width=200,
                                                  style=ButtonStyle().default_style)
        self.v_box.add(new_game_button.with_space_around(bottom=20))
        new_game_button.on_click = self.on_click_new_game

        # SETTINGS button
        settings_button = arcade.gui.UIFlatButton(text="Settings",
                                                  width=200,
                                                  style=ButtonStyle().default_style)
        self.v_box.add(settings_button.with_space_around(bottom=20))
        settings_button.on_click = self.on_click_settings

        # QUIT button
        quit_button = arcade.gui.UIFlatButton(text="Quit",
                                              width=200,
                                              style=ButtonStyle().default_style)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_text("Is this a GAME?", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 100,
                         arcade.color.WHITE, font_size=70, font_name="Kenney Pixel", anchor_x="center")
        arcade.draw_text("Yes, it is!!!", c.SCREEN_WIDTH / 2, c.SCREEN_HEIGHT - 150,
                         arcade.color.RED, font_size=50, font_name="Kenney Pixel", anchor_x="center")

    # Call back methods for buttons:
    def on_click_new_game(self, event):
        self.window.show_view(self.window.views["game"])
        setup(self.window.views["game"])

    def on_click_settings(self, event):
        self.window.show_view(self.window.views["settings"])

    def on_click_quit(self, event):
        self.window.close()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.close()
