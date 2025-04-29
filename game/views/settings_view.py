from arcade import View, draw_text, set_viewport
from arcade.color import WHITE
from arcade.key import ESCAPE

from .main_menu_view import MainMenuView


class SettingsView(View):

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            WHITE,
            44,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == ESCAPE:
            self.window.show_view(MainMenuView())
