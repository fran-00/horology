import arcade

from .main_menu_view import MainMenuView


class SettingsView(arcade.View):

    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
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
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MainMenuView())
