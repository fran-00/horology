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

    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.game_view.hotbar_sprite_list = arcade.load_spritesheet(file_name="resources/tilesets/input_prompts.png",
                                                                    sprite_width=16,
                                                                    sprite_height=16,
                                                                    columns=34,
                                                                    count=816,
                                                                    margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def draw_inventory(self):
        capacity = 10
        vertical_hotbar_location = self.game_view.view_bottom + 70
        hotbar_height = 80
        sprite_height = c.SPRITE_IMAGE_SIZE

        field_width = self.game_view.window.width / (capacity + 1)

        x = self.game_view.window.width / 2
        y = vertical_hotbar_location

        arcade.draw_rectangle_filled(
            center_x=self.game_view.view_left + 600,
            center_y=self.game_view.view_bottom + 70,
            width=self.game_view.window.width,
            height=hotbar_height,
            color=arcade.color.CHARCOAL
        )
        for i in range(capacity):
            y = vertical_hotbar_location
            x = i * field_width + 5
            if i == self.game_view.selected_item - 1:
                arcade.draw_lrtb_rectangle_outline(
                    left=x - 6,
                    right=x + field_width - 15,
                    top=y + 25,
                    bottom=y - 10,
                    color=arcade.color.WHITE,
                    border_width =2
                )

            if len(self.game_view.player.inventory) > i:
                item_name = self.game_view.player.inventory[i].name
            else:
                item_name = ""

            hotkey_sprite = self.game_view.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(x + sprite_height / 2,
                                      y + sprite_height / 2,
                                      2.0)
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"      {item_name}"
            arcade.draw_text(text,
                             x,
                             y,
                             arcade.color.WHITE,
                             25,
                             font_name="Kenney Pixel"
            )
