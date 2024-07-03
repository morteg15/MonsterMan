import pygame
import sys
from player import Player
from world import World
from battle import Battle
from monster_manager import MonsterManager
from sprite_loader import SpriteLoader
from monster_viewer import MonsterViewer

pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Monster Battler")

# Initialize game objects
monster_manager = MonsterManager()
player = None
world = None
battle = None
monster_viewer = None

# Game states
START_SCREEN = 0
PLAYING = 1
BATTLE = 2
GAME_OVER = 3
VIEWING_MONSTERS = 4

current_state = START_SCREEN

clock = pygame.time.Clock()

def start_new_game():
    global player, world, current_state, battle, monster_viewer
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, monster_manager)
    world = World(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, monster_manager)
    monster_viewer = MonsterViewer(screen, player)
    current_state = PLAYING
    battle = None
    SpriteLoader.load_music("overworld_music.mp3")
    pygame.mixer.music.play(-1)  # Loop indefinitely

def draw_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Monster Battler", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 400))

def draw_game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Game Over", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    
    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_state == START_SCREEN:
                if event.key == pygame.K_SPACE:
                    start_new_game()
            elif current_state == PLAYING:
                if event.key == pygame.K_m:
                    current_state = VIEWING_MONSTERS
                elif not battle:
                    old_x, old_y = player.x, player.y
                    if event.key == pygame.K_UP:
                        player.move(0, -TILE_SIZE, world)
                    elif event.key == pygame.K_DOWN:
                        player.move(0, TILE_SIZE, world)
                    elif event.key == pygame.K_LEFT:
                        player.move(-TILE_SIZE, 0, world)
                    elif event.key == pygame.K_RIGHT:
                        player.move(TILE_SIZE, 0, world)
                    
                    if (player.x, player.y) != (old_x, old_y):
                        world.player_has_moved()
                        
                    if world.is_healing_point(player.x, player.y):
                        player.heal_monsters()
                        print("Player's monsters healed!")
            elif current_state == BATTLE:
                if event.key == pygame.K_1:
                    battle.player_action("attack")
                elif event.key == pygame.K_2:
                    battle.player_action("heal")
                elif event.key == pygame.K_3:
                    battle.player_action("catch")
                elif event.key == pygame.K_4:
                    battle.player_action("run")
            elif current_state == GAME_OVER:
                if event.key == pygame.K_r:
                    start_new_game()
            elif current_state == VIEWING_MONSTERS:
                if not monster_viewer.handle_input(event):
                    current_state = PLAYING

    # Game state updates
    if current_state == PLAYING:
        if not battle and world.check_for_encounter(player):
            print("Battle started!")
            pygame.mixer.music.stop()  # Stop overworld music
            wild_monster = monster_manager.get_random_monster(player.get_average_level())
            battle = Battle(player, wild_monster, screen)
            current_state = BATTLE

    # Drawing
    if current_state == START_SCREEN:
        draw_start_screen()
    elif current_state == PLAYING:
        world.draw(screen)
        player.draw(screen)
    elif current_state == BATTLE:
        battle.draw()
        if battle.is_over():
            battle.end_battle()
            if player.active_monster.is_fainted():
                current_state = GAME_OVER
            else:
                battle = None
                current_state = PLAYING
                print("Battle ended!")
                # Restart overworld music
                SpriteLoader.load_music("overworld_music.mp3")
                pygame.mixer.music.play(-1)
    elif current_state == GAME_OVER:
        draw_game_over_screen()
    elif current_state == VIEWING_MONSTERS:
        monster_viewer.draw()

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()