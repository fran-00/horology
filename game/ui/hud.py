import arcade

from ..constants import Constants as c


class Hud:
    def __init__(self, view):
        self.game_view = view

    def draw_health_number(self):
        """Render player HP number"""
        # Draw how many hit points we have
        health_string = f"{self.game_view.player.cur_health}/{self.game_view.player.max_health}"
        arcade.draw_text(
                text=health_string,
                start_x=self.game_view.view_left + (c.SCREEN_WIDTH / 2) + 155,
                start_y=self.game_view.view_bottom + 51,
                font_size=30,
                font_name="Kenney Pixel",
                color=arcade.color.WHITE
        )

    def draw_health_bar(self):
        """Render player HP bar"""
        
        # Draw the red background of the bar
        if self.game_view.player.cur_health < self.game_view.player.max_health:
            arcade.draw_rectangle_filled(
                    center_x=self.game_view.view_left + (c.SCREEN_WIDTH / 2),
                    center_y=self.game_view.view_bottom + 60,
                    width=300,
                    height=20,
                    color=arcade.color.RED
            )

        # Calculate width based on health
        health_width = 300 * (self.game_view.player.cur_health / self.game_view.player.max_health)
        # Draw the green foreground of the bar
        arcade.draw_rectangle_filled(
                center_x=(self.game_view.view_left + (c.SCREEN_WIDTH / 2)) - 0.5 * (300 - health_width),
                center_y=self.game_view.view_bottom + 60,
                width=health_width,
                height=20,
                color=arcade.color.GREEN
        )

    def load_hotbar_sprites(self):
        """Load the sprites for the hotbar at the bottom of the screen.

        Loads the controls sprite tileset and selects only the number pad button sprites.
        These will be visual representations of number keypads (1️⃣, 2️⃣, 3️⃣, ..., 0️⃣)
        to clarify that the hotkey bar can be accessed through these keypresses.
        """

        first_number_pad_sprite_index = 51
        last_number_pad_sprite_index = 61

        self.game_view.hotbar_sprite_list = arcade.load_spritesheet(
                file_name="resources/tilesets/input_prompts.png",
                sprite_width=16,
                sprite_height=16,
                columns=34,
                count=816,
                margin=1,
        )[first_number_pad_sprite_index:last_number_pad_sprite_index]

    def draw_inventory_hotbar(self):
        capacity = 10
        hotbar_height = 40
        sprite_height = c.SPRITE_IMAGE_SIZE

        field_width = self.game_view.window.width / capacity

        arcade.draw_xywh_rectangle_filled(
                bottom_left_x=self.game_view.view_left,
                bottom_left_y=self.game_view.view_bottom,
                width=self.game_view.window.width,
                height=hotbar_height,
                color=arcade.color.CHARCOAL
        )
        for i in range(capacity):
            if i == self.game_view.selected_item - 1:
                arcade.draw_xywh_rectangle_outline(
                        bottom_left_x=(i * field_width) + self.game_view.view_left,
                        bottom_left_y=self.game_view.view_bottom,
                        width=self.game_view.window.width / capacity,
                        height=hotbar_height,
                        color=arcade.color.WHITE,
                        border_width =2
                )

            if len(self.game_view.player.inventory) > i:
                item_name = self.game_view.player.inventory[i].name
            else:
                item_name = ""

            hotkey_sprite = self.game_view.hotbar_sprite_list[i]
            hotkey_sprite.draw_scaled(
                    center_x=((i * field_width) + self.game_view.view_left) + sprite_height / 2,
                    center_y=self.game_view.view_bottom + 20,
                    scale=2.0
            )
            # Add whitespace so the item text doesn't hide behind the number pad sprite
            text = f"      {item_name}"
            arcade.draw_text(
                    text=text,
                    start_x=((i * field_width) + self.game_view.view_left) + sprite_height / 2,
                    start_y=self.game_view.view_bottom + 12,
                    color=arcade.color.WHITE,
                    font_size=25,
                    font_name="Kenney Pixel"
            )

    def draw_equipped_weapons(self):
        if self.game_view.player.equipped_melee_weapon:
            weapon_name = f"Melee weapon: {self.game_view.player.equipped_melee_weapon.name}"
            arcade.draw_text(
                    text=weapon_name,
                    start_x=self.game_view.view_left + 10,
                    start_y=self.game_view.view_bottom + c.SCREEN_HEIGHT - 30,
                    color=arcade.color.WHITE,
                    font_size=25,
                    font_name="Kenney Pixel"
            )
        if self.game_view.player.equipped_ranged_weapon:
            weapon_name = f"Ranged weapon: {self.game_view.player.equipped_ranged_weapon.name}"
            arcade.draw_text(
                    text=weapon_name,
                    start_x=self.game_view.view_left + 10,
                    start_y=self.game_view.view_bottom + c.SCREEN_HEIGHT - 60,
                    color=arcade.color.WHITE,
                    font_size=25,
                    font_name="Kenney Pixel"
            )
