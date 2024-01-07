import arcade

from shared_constants import *


class EnemyAI:
    def __init__(self, view):
        self.game_view = view

    def handle_enemies_animation(self, delta_time):
        """Handle enemies animation"""
        for enemy in self.game_view.scene[LAYER_NAME_ENEMIES]:
            enemy.update_animation(delta_time)

    def handle_enemies_following_behaviour(self, delta_time):
        """Handle enemies following behaviour"""
        for enemy in self.game_view.scene[LAYER_NAME_ENEMIES]:
            enemy.update_path(delta_time)

    def handle_enemies_shooting(self, delta_time):
        """Handle enemies shooting"""
        for enemy in self.game_view.scene[LAYER_NAME_ENEMIES]:
            bullet = enemy.shoot_at_player(delta_time)
            if bullet:
                self.game_view.scene[LAYER_NAME_BULLETS].append(bullet)
