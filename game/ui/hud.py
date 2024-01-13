import arcade

from ..constants import Constants as c


class Hud:
    def __init__(self, view):
        self.game_view = view

    def draw_health_number(self):
        """Render player HP number"""
        # Draw how many hit points we have
        health_string = f"{self.game_view.player.cur_health}/{self.game_view.player.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.game_view.view_left + 750,
                         start_y=self.game_view.view_bottom + 0,
                         font_size=25,
                         font_name="Kenney Pixel",
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """Render player HP bar"""
        # Draw the red background of the bar
        if self.game_view.player.cur_health < self.game_view.player.max_health:
            arcade.draw_rectangle_filled(center_x=self.game_view.view_left + 600,
                                         center_y=self.game_view.view_bottom + 10,
                                         width=c.HEALTHBAR_WIDTH,
                                         height=10,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = c.HEALTHBAR_WIDTH * (self.game_view.player.cur_health / self.game_view.player.max_health)
        # Draw the green foreground of the bar
        arcade.draw_rectangle_filled(center_x=(self.game_view.view_left + 600) - 0.5 * (c.HEALTHBAR_WIDTH - health_width),
                                     center_y=self.game_view.view_bottom - 10,
                                     width=health_width,
                                     height=c.HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = 40
        hotbar_height = 80
        sprite_height = 16

        field_width = self.game_view.window.width / (capacity + 1)

        x = self.game_view.window.width / 2
        y = vertical_hotbar_location

        arcade.draw_rectangle_filled(
            x, y, self.game_view.window.width, hotbar_height, arcade.color.CHARCOAL
        )
        for i in range(capacity):
            y = vertical_hotbar_location
            x = i * field_width + 5
            if i == self.game_view.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    x - 6, x + field_width - 15, y + 25, y - 10, arcade.color.WHITE, 2
                )

            if len(self.game_view.player.inventory) > i:
                item_name = self.game_view.player.inventory[i].name
            else:
                item_name = ""

            hotkey_sprite = self.game_view.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + sprite_height / 2, y + sprite_height / 2, 2.0)
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"      {item_name}"
            arcade.draw_text(text, x, y, arcade.color.WHITE, 25, font_name="Kenney Pixel")