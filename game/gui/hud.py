import arcade

from shared_constants import *


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
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """Render player HP bar"""
        # Draw the red background of the bar
        if self.game_view.player.cur_health < self.game_view.player.max_health:
            arcade.draw_rectangle_filled(center_x=self.game_view.view_left + 600,
                                         center_y=self.game_view.view_bottom + 10,
                                         width=HEALTHBAR_WIDTH,
                                         height=10,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.game_view.player.cur_health / self.game_view.player.max_health)
        # Draw the green foreground of the bar
        arcade.draw_rectangle_filled(center_x=(self.game_view.view_left + 600) - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.game_view.view_bottom - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

    def draw_inventory(self):
        """Render the Inventory"""
        start_x = self.game_view.view_left + 30
        start_y = self.game_view.view_bottom + 50
        for i, item in enumerate(self.game_view.player.inventory, 1):
            your_stuff = f"{i}: {item.name}"
            arcade.draw_text(your_stuff, start_x, start_y,
                             arcade.csscolor.WHITE, 10, anchor_y="top")
            start_y -= 20
