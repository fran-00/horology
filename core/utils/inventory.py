import arcade

from entities.weapons import Melee, Ranged
from shared_constants import *


class Inventory:
    def __init__(self, view):
        self.game_view = view

    def pick_up_items(self):
        """Handle pick up items: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH"""
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.game_view.player,
                                                              self.game_view.scene[LAYER_ITEMS])

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
                self.pick_up_weapon(item)

    def pick_up_weapon(self, weapon):
        weapon_name = str(weapon.properties['name'])
        weapon_damage = int(weapon.properties['damage'])
        if str(weapon.properties['weapon']) == "melee":
            new_weapon = Melee(weapon_name, weapon_damage)
        else:
            new_weapon = Ranged(weapon_name, weapon_damage)
        self.game_view.player.inventory.append(new_weapon)
        if not self.game_view.player.equipped_ranged_weapon:
            self.game_view.player.equipped_ranged_weapon = new_weapon
        else:
            print("You changed your weapon")
            self.game_view.player.equipped_ranged_weapon = new_weapon
        weapon.remove_from_sprite_lists()
