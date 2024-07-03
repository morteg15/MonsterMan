import pygame
from sprite_loader import SpriteLoader

class MonsterViewer:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.current_page = 0
        self.monsters_per_page = 4
        self.viewer_background = SpriteLoader.load_sprite("background", "viewer_background.png", self.screen.get_size())
        if self.viewer_background is None:
            self.viewer_background = pygame.Surface(self.screen.get_size())
            self.viewer_background.fill((200, 200, 200))  # Light gray as fallback

    def draw(self):
        self.screen.blit(self.viewer_background, (0, 0))
        
        title = self.title_font.render("Your Monsters", True, (0, 0, 0))
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 20))

        start_index = self.current_page * self.monsters_per_page
        end_index = min(start_index + self.monsters_per_page, len(self.player.monsters))

        for i, monster in enumerate(self.player.monsters[start_index:end_index]):
            self.draw_monster_card(monster, i)

        self.draw_navigation()

    def draw_monster_card(self, monster, position):
        card_width = 350
        card_height = 200
        padding = 20
        cards_per_row = 2

        row = position // cards_per_row
        col = position % cards_per_row

        x = padding + col * (card_width + padding)
        y = 80 + row * (card_height + padding)

        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, card_width, card_height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, card_width, card_height), 2)

        sprite = SpriteLoader.load_monster_sprite(monster.name.lower(), (100, 100))
        if sprite:
            self.screen.blit(sprite, (x + 10, y + 50))

        name_text = self.font.render(f"Name: {monster.name}", True, (0, 0, 0))
        level_text = self.font.render(f"Level: {monster.level}", True, (0, 0, 0))
        xp_text = self.font.render(f"XP: {monster.xp}", True, (0, 0, 0))
        hp_text = self.font.render(f"HP: {monster.stats['hp']}/{monster.base_stats['hp']}", True, (0, 0, 0))

        self.screen.blit(name_text, (x + 120, y + 10))
        self.screen.blit(level_text, (x + 120, y + 40))
        self.screen.blit(xp_text, (x + 120, y + 70))
        self.screen.blit(hp_text, (x + 120, y + 100))

    def draw_navigation(self):
        if self.current_page > 0:
            prev_text = self.font.render("< Previous (A)", True, (0, 0, 0))
            self.screen.blit(prev_text, (20, self.screen.get_height() - 40))

        if (self.current_page + 1) * self.monsters_per_page < len(self.player.monsters):
            next_text = self.font.render("Next (D) >", True, (0, 0, 0))
            self.screen.blit(next_text, (self.screen.get_width() - 120, self.screen.get_height() - 40))

        exit_text = self.font.render("Exit (E)", True, (0, 0, 0))
        self.screen.blit(exit_text, (self.screen.get_width() // 2 - exit_text.get_width() // 2, self.screen.get_height() - 40))

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and self.current_page > 0:
                self.current_page -= 1
            elif event.key == pygame.K_d and (self.current_page + 1) * self.monsters_per_page < len(self.player.monsters):
                self.current_page += 1
            elif event.key == pygame.K_e:
                return False  # Exit the viewer
        return True  # Continue viewing