import arcade

from .combat import Combat
from ..entities.enemies import EnemyCharacter
from ..constants import Constants as c


class EnemyAI:

    def __init__(self, view):
        self.game_view = view
        self.combat = Combat(self.game_view)

    def handle_enemies_animation(self, delta_time):
        """Handle enemies animation"""
        for enemy in self.game_view.scene[c.LAYER_ENEMIES]:
            enemy.update_animation(delta_time)

    def handle_enemies_following_behaviour(self, delta_time):
        """Handle enemies following behaviour"""
        for enemy in self.game_view.scene[c.LAYER_ENEMIES]:
            enemy.update_path(delta_time)

    def handle_enemies_shooting(self, delta_time):
        """Handle enemies shooting"""
        for enemy in self.game_view.scene[c.LAYER_ENEMIES]:
            bullet = self.combat.create_bullet_from_enemy(enemy, delta_time)
            if bullet:
                self.game_view.scene[c.LAYER_ENEMIES_BULLETS].append(bullet)

    def draw_A_star_paths(self):
        for enemy in self.game_view.scene[c.LAYER_ENEMIES]:
            if enemy.path:
                arcade.draw_line_strip(enemy.path, arcade.color.BLUE, 2)

    def spawn_enemies(self):
        """Spawn an enemy when a spawn point is triggered"""
        spawn_points_touched_list = arcade.check_for_collision_with_list(self.game_view.player,
                                                                         self.game_view.scene[c.LAYER_SPAWN_TRIGGER])
        if spawn_points_touched_list != []:
            for spawn_point in spawn_points_touched_list:
                enemy_name = spawn_point.properties["name"]
                enemy_hp = spawn_point.properties["hp"]
                enemy_damage = spawn_point.properties["damage"]
                # remove the spawn point triggered from sprite list
                spawn_point.kill()
                print("Prepare to fight! Spawn point touched!")

            enemy = EnemyCharacter(enemy_name, enemy_hp, enemy_damage, self.game_view.player, self.game_view.scene[c.LAYER_WALLS])
            # Position the enemy 100 pixels away horizontally
            enemy.center_x = spawn_point.center_x + 100
            enemy.center_y = spawn_point.center_y

            # Add the enemy to the lists spawning it at a random location
            self.game_view.scene[c.LAYER_ENEMIES].append(enemy)

    def get_damage_from_enemy(self):
        """Handle fights with enemies"""
        enemies_hit_list = arcade.check_for_collision_with_list(self.game_view.player,
                                                                self.game_view.scene[c.LAYER_ENEMIES])
        # If player touch an ENEMY, she loses as many hp as is written on damage property
        if self.game_view.player.cur_health > 0:
            for enemy in enemies_hit_list:
                hp_lost = int(enemy.damage)
                self.game_view.player.cur_health -= hp_lost
        # If player's health reaches 0, she respawns at starting coordinates with full health (for now)
        else:
            self.game_view.player.change_x = 0
            self.game_view.player.change_y = 0
            self.game_view.player.center_x = c.PLAYER_START_X
            self.game_view.player.center_y = c.PLAYER_START_Y
            self.game_view.player.cur_health = self.game_view.player.max_health
