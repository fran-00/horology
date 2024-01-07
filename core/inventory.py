import arcade

import stuff
from shared_constants import *


class Inventory:
    def __init__(self, view):
        self.game_view = view

    def pick_up_items(self):
        """Handle pick up items: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH"""
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.game_view.player,
                                                              self.game_view.scene[LAYER_NAME_ITEMS])

        for item in items_hit_list:
            # If player's health isn't full, loop through each colliding sprite,
            # add hp_restored propriety value (int) to hp and remove item sprite from list.
            if 'hp_restore' in item.properties and self.game_view.player.cur_health < self.game_view.player.max_health:
                hp_restored = int(item.properties['hp_restore'])
                self.game_view.player.cur_health += hp_restored
                item.remove_from_sprite_lists()
            elif 'hp_restore' in item.properties and self.game_view.player.cur_health == self.game_view.player.max_health:
                print("your health is full")
            elif 'weapon' in item.properties:
                my_weapon = int(item.properties['weapon'])
                if my_weapon == 1:
                    self.game_view.player.inventory.append(stuff.Sep())
                    item.remove_from_sprite_lists()