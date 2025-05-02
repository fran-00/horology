import arcade
from arcade.gui import UIAnchorLayout, UIFlatButton, UIGridLayout, UIView


class GameMenuView(UIView):
    """Accessed by pressing ESC key."""
    def __init__(self):
        super().__init__()
        self.background_color = arcade.uicolor.BLACK

        self.grid = UIGridLayout(
            column_count=1,
            row_count=3,
            size_hint=(0, 0),
            vertical_spacing=10,
            horizontal_spacing=10,
        )

        self.ui.add(UIAnchorLayout(children=[self.grid]))
        self.add_buttons()

    def add_buttons(self):
        # RESUME button
        resume_button = UIFlatButton(
            text="Resume Game",
            width=200,
        )
        resume_button.on_click = self.on_click_resume
        self.grid.add(resume_button, row=0, column=0)

        # SAVE Button
        save_button = UIFlatButton(
            text="Save",
            width=200,
        )
        self.grid.add(save_button, row=1, column=0)
        
        # QUIT button
        quit_button = UIFlatButton(
            text="Quit to Main Menu",
            width=200,
        )
        quit_button.on_click = self.on_click_quit
        self.grid.add(quit_button, row=2, column=0)

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
