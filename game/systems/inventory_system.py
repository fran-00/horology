import arcade

from ..entities.weapons import Melee, Ranged
from ..constants import Constants as c


class InventorySystem:
    def __init__(self, view):
        self.game_view = view

    def pick_up_items(self):
        """Handle pick up items: WEAPONS AND CONSUMABLES THAT RESTORE HEALTH"""
        # Generate a list of all sprites from the item layer of the map that collided with the player.
        items_hit_list = arcade.check_for_collision_with_list(self.game_view.player,
                                                              self.game_view.scene[c.LAYER_ITEMS])

        for item in items_hit_list:
            # If player's health isn't full, loop through each colliding sprite,
            # add hp_restored propriety value (int) to hp and remove item sprite from list.
            if 'hp_restore' in item.properties and self.game_view.player.cur_health < self.game_view.player.max_health:
                hp_restored = int(item.properties['hp_restore'])
                self.game_view.player.cur_health += hp_restored
                if self.game_view.player.cur_health > self.game_view.player.max_health:
                    self.game_view.player.cur_health = self.game_view.player.max_health
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
            if not self.game_view.player.equipped_melee_weapon:
                self.game_view.player.equipped_melee_weapon = new_weapon
        else:
            new_weapon = Ranged(weapon_name, weapon_damage)
            if not self.game_view.player.equipped_ranged_weapon:
                self.game_view.player.equipped_ranged_weapon = new_weapon

        self.game_view.player.inventory.append(new_weapon)
        weapon.remove_from_sprite_lists()

    def change_equipped_weapon(self, number):
        for i, weapon in enumerate(self.game_view.player.inventory):
            if number == i + 1:
                print(f"Weapon {weapon.name} equipped")
                if weapon.weapon_type() == "melee":
                    self.game_view.player.equipped_melee_weapon = weapon
                elif weapon.weapon_type() == "ranged":
                    self.game_view.player.equipped_ranged_weapon = weapon
