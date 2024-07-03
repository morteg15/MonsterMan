import json
import random
from monster import Monster

class MonsterManager:
    def __init__(self):
        with open('data/monster_data.json', 'r') as file:
            self.monster_data = json.load(file)['monsters']

    def get_monster_by_id(self, monster_id):
        monster_data = next((m for m in self.monster_data if m['id'] == monster_id), None)
        if monster_data:
            return Monster(monster_data)
        return None

    def get_random_monster(self, level_range):
        monster_data = random.choice(self.monster_data)
        monster = Monster(monster_data)
        monster.level = random.randint(max(1, level_range - 2), level_range + 2)
        monster.stats = monster.calculate_stats()
        return monster

    def get_starter_monster(self):
        starter_data = next((m for m in self.monster_data if m['id'] == 1), None)
        if starter_data:
            return Monster(starter_data, level=5)
        return None

    def evolve_monster(self, monster):
        if monster.evolution:
            evolved_monster_data = self.get_monster_by_id(monster.evolution['evolvesTo'])
            if evolved_monster_data:
                evolved_monster = Monster(evolved_monster_data, level=monster.level)
                evolved_monster.stats = evolved_monster.calculate_stats()
                return evolved_monster
        return monster