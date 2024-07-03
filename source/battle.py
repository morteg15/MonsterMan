import pygame
import random
from sprite_loader import SpriteLoader

class Battle:
    def __init__(self, player, wild_monster, screen):
        self.player = player
        self.player_monster = player.active_monster
        self.wild_monster = wild_monster
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.battle_log = []
        self.battle_over = False

        # Load battle background
        self.background = SpriteLoader.load_sprite("background", "battle_background.png", self.screen.get_size())
        if self.background is None:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((200, 200, 200))  # Light gray as fallback

        # Load UI elements
        self.log_box = SpriteLoader.load_ui_element("log_box")
        self.action_box = SpriteLoader.load_ui_element("action_box")
        self.health_bar = SpriteLoader.load_ui_element("health_bar")

        # Load monster sprites with increased size
        self.player_monster_sprite = SpriteLoader.load_monster_sprite(f"{self.player_monster.name.lower()}_back", (160, 160))
        self.wild_monster_sprite = SpriteLoader.load_monster_sprite(self.wild_monster.name.lower(), (160, 160))

        # Load battle music
        SpriteLoader.load_music("battle_music.mp3")
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def player_action(self, action):
        if action == "attack":
            move = self.player_monster.select_move()
            damage = self.player_monster.use_move(move)
            self.wild_monster.take_damage(damage)
            self.battle_log.append(f"{self.player_monster.name} uses {move['name']} for {damage} damage!")
            if self.wild_monster.is_fainted():
                self.battle_log.append(f"Wild {self.wild_monster.name} fainted!")
                xp_gain = self.calculate_xp_gain(self.wild_monster)
                self.player_monster.gain_xp(xp_gain)
                self.battle_log.append(f"{self.player_monster.name} gained {xp_gain} XP!")
                self.battle_over = True
            else:
                self.wild_monster_turn()
        elif action == "heal":
            heal_amount = 20  # You can adjust this or make it more dynamic
            self.player_monster.heal(heal_amount)
            self.battle_log.append(f"{self.player_monster.name} healed for {heal_amount} HP!")
            self.wild_monster_turn()
        elif action == "catch":
            catch_probability = 1 - (self.wild_monster.stats['hp'] / self.wild_monster.base_stats['hp'])
            if random.random() < catch_probability:
                self.battle_log.append(f"You caught {self.wild_monster.name}!")
                self.player.add_monster(self.wild_monster)
                self.battle_over = True
            else:
                self.battle_log.append("Failed to catch the monster!")
                self.wild_monster_turn()
        elif action == "run":
            if random.random() < 0.5:
                self.battle_log.append("Got away safely!")
                self.battle_over = True
            else:
                self.battle_log.append("Couldn't escape!")
                self.wild_monster_turn()

    def wild_monster_turn(self):
        move = self.wild_monster.select_move()
        damage = self.wild_monster.use_move(move)
        self.player_monster.take_damage(damage)
        self.battle_log.append(f"Wild {self.wild_monster.name} uses {move['name']} for {damage} damage!")
        if self.player_monster.is_fainted():
            self.battle_log.append(f"{self.player_monster.name} fainted!")
            self.battle_over = True

    def calculate_xp_gain(self, defeated_monster):
        return defeated_monster.level * 10

    def draw_health_bar(self, monster, x, y, is_player):
        if self.health_bar:
            self.screen.blit(self.health_bar, (x, y))
            health_percentage = monster.stats['hp'] / monster.base_stats['hp']
            bar_width = int(92 * health_percentage)  # Assuming health bar is 92 pixels wide
            health_color = (0, 255, 0) if health_percentage > 0.5 else (255, 255, 0) if health_percentage > 0.25 else (255, 0, 0)
            pygame.draw.rect(self.screen, health_color, (x + 54, y + 6, bar_width, 8))
        
        name_text = self.font.render(monster.name, True, (0, 0, 0))
        hp_text = self.font.render(f"HP: {monster.stats['hp']}/{monster.base_stats['hp']}", True, (0, 0, 0))
        
        if is_player:
            self.screen.blit(name_text, (x + 5, y + 5))
            self.screen.blit(hp_text, (x + 5, y + 25))
        else:
            self.screen.blit(name_text, (x + 95, y + 5))
            self.screen.blit(hp_text, (x + 95, y + 25))

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw player monster sprite
        player_monster_pos = (50, self.screen.get_height() - 200)
        self.screen.blit(self.player_monster_sprite, player_monster_pos)

        # Draw wild monster sprite
        wild_monster_pos = (self.screen.get_width() - 210, 50)
        self.screen.blit(self.wild_monster_sprite, wild_monster_pos)

        # Draw health bars
        self.draw_health_bar(self.player_monster, 50, self.screen.get_height() - 230, True)
        self.draw_health_bar(self.wild_monster, self.screen.get_width() - 210, 20, False)
        
        # Draw battle log
        if self.log_box:
            log_box_pos = (10, self.screen.get_height() - 150)
            self.screen.blit(self.log_box, log_box_pos)
            log_y = log_box_pos[1] + 10
            for log in self.battle_log[-3:]:
                log_surface = self.font.render(log, True, (0, 0, 0))
                self.screen.blit(log_surface, (log_box_pos[0] + 10, log_y))
                log_y += 30

        # Draw action prompts
        if self.action_box:
            action_box_pos = (self.screen.get_width() - 150, self.screen.get_height() - 150)
            self.screen.blit(self.action_box, action_box_pos)
            actions = ["1: Attack", "2: Heal", "3: Catch", "4: Run"]
            action_y = action_box_pos[1] + 10
            for action in actions:
                action_surface = self.font.render(action, True, (0, 0, 0))
                self.screen.blit(action_surface, (action_box_pos[0] + 10, action_y))
                action_y += 30

    def is_over(self):
        return self.battle_over

    def end_battle(self):
        pygame.mixer.music.stop()