import pygame
import os

class SpriteLoader:
    @staticmethod
    def load_sprite(folder, filename, size=None):
        path = os.path.join("data", folder, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except pygame.error as e:
            print(f"Unable to load image: {path}")
            print(e)
            return None

    @staticmethod
    def load_hero_sprite(size=(40, 40)):
        return SpriteLoader.load_sprite("hero", "hero.png", size)

    @staticmethod
    def load_monster_sprite(monster_name, size=(200, 200)):
        # Try to load the specific sprite (front or back)
        sprite = SpriteLoader.load_sprite("monsters", f"{monster_name}.png", size)
        
        # If the specific sprite doesn't exist, try to load the default sprite
        if sprite is None:
            default_name = monster_name.split('_')[0]  # Remove '_back' if present
            sprite = SpriteLoader.load_sprite("monsters", f"{default_name}.png", size)
        
        return sprite

    @staticmethod
    def load_background_sprite(size=(400, 400)):
        return SpriteLoader.load_sprite("background", "background.png", size)

    @staticmethod
    def load_grass_sprite(size=(40, 40)):
        return SpriteLoader.load_sprite("background", "grass.png", size)

    @staticmethod
    def load_heal_space_sprite(size=(40, 40)):
        return SpriteLoader.load_sprite("background", "heal_space.png", size)

    @staticmethod
    def load_ui_element(element_name):
        return SpriteLoader.load_sprite("UI", f"{element_name}.png")

    @staticmethod
    def load_music(filename):
        path = os.path.join("data", "music", filename)
        try:
            pygame.mixer.music.load(path)
            return True
        except pygame.error as e:
            print(f"Unable to load music: {path}")
            print(e)
            return False