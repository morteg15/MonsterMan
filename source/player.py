import pygame
from sprite_loader import SpriteLoader

class Player:
    def __init__(self, x, y, monster_manager):
        self.x = x
        self.y = y
        self.monster_manager = monster_manager
        self.monsters = []
        self.active_monster = None
        self.sprite = SpriteLoader.load_hero_sprite((40, 40))
        if self.sprite is None:
            self.sprite = pygame.Surface((40, 40))
            self.sprite.fill((0, 0, 255))  # Blue square as fallback
        
        # Give the player a starter monster
        starter = self.monster_manager.get_starter_monster()
        self.add_monster(starter)

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < world.width and 0 <= new_y < world.height:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def add_monster(self, monster):
        self.monsters.append(monster)
        if not self.active_monster:
            self.active_monster = monster

    def heal_monsters(self):
        for monster in self.monsters:
            monster.heal(monster.base_stats['hp'])

    def get_average_level(self):
        if not self.monsters:
            return 5  # Default level if no monsters
        return sum(monster.level for monster in self.monsters) // len(self.monsters)