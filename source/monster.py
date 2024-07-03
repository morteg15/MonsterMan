import random
import pygame
from sprite_loader import SpriteLoader

class Monster:
    def __init__(self, monster_data, level=5):
        self.id = monster_data['id']
        self.name = monster_data['name']
        self.type = monster_data['type']
        self.level = level
        self.xp = 0
        self.base_stats = monster_data['baseStats']
        self.stat_growth = monster_data['statGrowth']
        self.stats = self.calculate_stats()
        self.moves = self.get_moves_for_level(monster_data['moves'])
        self.evolution = monster_data.get('evolution')
        self.sprite = SpriteLoader.load_monster_sprite(self.name.lower(), (80, 80))
        if self.sprite is None:
            self.sprite = pygame.Surface((80, 80))
            self.sprite.fill((128, 0, 128))  # Purple square as fallback

    def calculate_stats(self):
        stats = {}
        for stat, base_value in self.base_stats.items():
            growth = self.stat_growth[stat]
            stats[stat] = base_value + (growth * (self.level - 1))
        return stats

    def get_moves_for_level(self, all_moves):
        return [move for move in all_moves if move['levelLearned'] <= self.level]

    def select_move(self):
        return random.choice(self.moves)

    def use_move(self, move):
        damage = move['power']
        # You could add more complex damage calculation here
        return damage

    def take_damage(self, damage):
        self.stats['hp'] -= damage
        if self.stats['hp'] < 0:
            self.stats['hp'] = 0

    def is_fainted(self):
        return self.stats['hp'] <= 0

    def heal(self, amount):
        max_hp = self.base_stats['hp'] + (self.stat_growth['hp'] * (self.level - 1))
        self.stats['hp'] = min(self.stats['hp'] + amount, max_hp)

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.calculate_xp_for_next_level():
            self.level_up()

    def calculate_xp_for_next_level(self):
        # This is a simple formula, you might want to use a more complex one
        return self.level ** 3

    def level_up(self):
        self.level += 1
        old_stats = self.stats.copy()
        self.stats = self.calculate_stats()
        for stat in self.stats:
            gain = self.stats[stat] - old_stats[stat]
            print(f"{self.name} gained {gain} {stat}!")
        
        # Check for new moves
        new_moves = [move for move in self.moves if move['levelLearned'] == self.level]
        for move in new_moves:
            print(f"{self.name} learned {move['name']}!")
        
        # Check for evolution
        if self.evolution and self.level >= self.evolution['level']:
            print(f"{self.name} is evolving!")
            # You would typically trigger an evolution event here

    def __str__(self):
        return f"{self.name} (Lv. {self.level})"