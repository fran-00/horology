import arcade


class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "Settings",
            self.window.width / 2,
            self.window.height - 50,
            arcade.color.WHITE,
            44,
            anchor_x="center",
            anchor_y="center",
            align="center",
            width=self.window.width,
        )

    def setup(self):
        pass

    def on_show_view(self):
        arcade.set_background_color(arcade.color.PURPLE)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.views["main_menu"])
