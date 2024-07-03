import pygame
import random
import time
from sprite_loader import SpriteLoader

class World:
    def __init__(self, width, height, tile_size, monster_manager):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.monster_manager = monster_manager
        self.grass_patches = []
        self.healing_point = (20, 20)
        self.create_grass_patches()
        self.last_battle_time = 0
        self.battle_cooldown = 5  # 5 seconds cooldown
        self.player_moved = False
        
        self.background_sprite = SpriteLoader.load_background_sprite((width, height))
        self.grass_sprite = SpriteLoader.load_grass_sprite((tile_size, tile_size))
        self.heal_space_sprite = SpriteLoader.load_heal_space_sprite((tile_size, tile_size))

    def create_grass_patches(self):
        for _ in range(5):
            x = random.randint(0, (self.width // self.tile_size) - 1) * self.tile_size
            y = random.randint(0, (self.height // self.tile_size) - 1) * self.tile_size
            self.grass_patches.append((x, y))

    def draw(self, screen):
        if self.background_sprite:
            screen.blit(self.background_sprite, (0, 0))
        else:
            screen.fill((200, 200, 200))  # Light gray as fallback

        for grass in self.grass_patches:
            if self.grass_sprite:
                screen.blit(self.grass_sprite, grass)
            else:
                pygame.draw.rect(screen, (0, 100, 0), (*grass, self.tile_size, self.tile_size))

        if self.heal_space_sprite:
            screen.blit(self.heal_space_sprite, self.healing_point)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (*self.healing_point, self.tile_size, self.tile_size))

    def check_for_encounter(self, player):
        current_time = time.time()
        if not self.player_moved or current_time - self.last_battle_time < self.battle_cooldown:
            return False

        player_rect = pygame.Rect(player.x, player.y, self.tile_size, self.tile_size)
        for grass_pos in self.grass_patches:
            grass_rect = pygame.Rect(*grass_pos, self.tile_size, self.tile_size)
            if player_rect.colliderect(grass_rect):
                if random.random() < 0.3:  # 30% chance of encounter
                    self.last_battle_time = current_time
                    self.player_moved = False
                    return True
        return False

    def is_healing_point(self, x, y):
        return (x, y) == self.healing_point

    def player_has_moved(self):
        self.player_moved = True