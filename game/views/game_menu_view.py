import arcade
import arcade.gui

from ..core.setup import setup
from ..ui.buttons import ButtonStyle


class GameMenuView(arcade.View):
    """
    Accessed by hitting ESC key.
    """
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        self.add_buttons()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x", anchor_y="center_y", child=self.v_box
            )
        )

    def add_buttons(self):
        # RESUME button
        resume_button = arcade.gui.UIFlatButton(text="Resume Game",
                                                width=200,
                                                style=ButtonStyle().default_style)
        self.v_box.add(resume_button.with_space_around(bottom=20))
        resume_button.on_click = self.on_click_resume

        # SAVE Button
        save_button = arcade.gui.UIFlatButton(text="Save",
                                              width=200,
                                              style=ButtonStyle().default_style)
        self.v_box.add(save_button.with_space_around(bottom=20))
        
        # QUIT button
        quit_button = arcade.gui.UIFlatButton(text="Quit to Main Menu",
                                              width=200,
                                              style=ButtonStyle().default_style)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

    def on_show_view(self):
        arcade.set_viewport(0, self.window.width, 0, self.window.height)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    # call back methods for buttons:
    def on_click_resume(self, event):
        self.window.show_view(self.window.views["game"])

    def on_click_save(self, event):
        pass

    def on_click_quit(self, event):
        self.window.show_view(self.window.views["main_menu"])

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["game"])
