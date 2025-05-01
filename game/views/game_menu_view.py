from arcade import View
from arcade.gui import UIAnchorLayout, UIManager, UIBoxLayout, UIFlatButton
from arcade.key import ESCAPE


class GameMenuView(View):
    """
    Accessed by hitting ESC key.
    """
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element, a UIManager to handle the UI.
        self.manager = UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = UIBoxLayout()

        self.add_buttons()

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            UIAnchorLayout(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def add_buttons(self):
        # RESUME button
        resume_button = UIFlatButton(
            text="Resume Game",
            width=200,
        )
        self.v_box.add(resume_button)
        resume_button.on_click = self.on_click_resume

        # SAVE Button
        save_button = UIFlatButton(
            text="Save",
            width=200,
        )
        self.v_box.add(save_button)
        
        # QUIT button
        quit_button = UIFlatButton(
            text="Quit to Main Menu",
            width=200,
        )
        self.v_box.add(quit_button)
        quit_button.on_click = self.on_click_quit

    def on_show_view(self):
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
        if key == ESCAPE:
            self.window.show_view(self.window.views["game"])
