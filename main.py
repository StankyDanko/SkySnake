# main.py
import pygame
import random
import math
import logging
import os  # Import os for file operations
from config.config import *  # Assumes config.py exists with constants like WIDTH, HEIGHT, etc.
from classes.platform import Platform
from classes.projectile import Projectile
from classes.food import Food
from classes.acid_droplet import AcidDroplet
from classes.sky_snake import SkySnake
from classes.player import Player

# Create debug folder if it doesn't exist
debug_folder = 'debug'
if not os.path.exists(debug_folder):
    os.makedirs(debug_folder)

# Define log file paths
log_file_3 = os.path.join(debug_folder, 'game.log.3')
log_file_2 = os.path.join(debug_folder, 'game.log.2')
log_file_1 = os.path.join(debug_folder, 'game.log.1')

# Rotate log files
if os.path.exists(log_file_3):
    os.remove(log_file_3)
if os.path.exists(log_file_2):
    os.rename(log_file_2, log_file_3)
if os.path.exists(log_file_1):
    os.rename(log_file_1, log_file_2)

# Set up logging to game.log.1 in the debug folder
logging.basicConfig(
    filename=log_file_1,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite if exists
)

logging.info("Game starting")

try:
    # Initialize Pygame
    pygame.init()
    logging.info("Pygame initialized")

    # Set up the game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slingshot Hero")
    logging.info("Game window set up")

    # Fonts for rendering UI text
    font = pygame.font.Font(None, 36)
    paused_font = pygame.font.Font(None, 72)
    paused_text = paused_font.render("PAUSED", True, WHITE)
    continue_text = font.render("CONTINUE", True, WHITE)
    quit_text = font.render("QUIT", True, WHITE)
    paused_rect = paused_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    continue_rect = continue_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))

    logging.info("Fonts initialized")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    logging.info("Clock initialized")

    # Sprite groups
    projectiles = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    food_group = pygame.sprite.Group()
    acid_group = pygame.sprite.Group()
    logging.info("Sprite groups created")

    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    logging.info("Player initialized")

    snake = SkySnake()
    logging.info("SkySnake initialized")

    # Add initial platforms
    ground = Platform(0, HEIGHT - 20, WIDTH, 20)
    platforms.add(ground)
    logging.info("Platforms initialized")

    # Add initial food
    for _ in range(3):
        food = Food()
        food_group.add(food)
    logging.info("Food initialized")

    # Charging mechanics
    charging = False
    power = 0
    max_power = 100
    charge_rate = 4

    # Game state
    game_state = "running"  # Possible states: "running", "paused", "won", "lost"

    # Function to reset the game
    def reset_game():
        global player, snake, game_state
        projectiles.empty()
        food_group.empty()
        acid_group.empty()
        player = Player()
        player_group.empty()
        player_group.add(player)
        snake = SkySnake()
        for _ in range(3):
            food = Food()
            food_group.add(food)
        game_state = "running"
        logging.info("Game reset")

    logging.info("Game loop starting")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event received")
                pygame.quit()
                exit()
            elif game_state == "running":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        charging = True
                        power = 0
                        logging.debug("Mouse button down: charging")
                    elif event.button == 3:  # Right mouse button
                        # Transform feathershot projectiles into platforms
                        for proj in projectiles:
                            if proj.ammo_type == "feathershot" and not proj.is_platform:
                                proj.is_platform = True
                                proj.stopped = True  # Stop movement
                                proj.image = pygame.Surface((30, 30))
                                proj.image.fill(CYAN)
                                proj.rect = proj.image.get_rect(center=proj.rect.center)
                                proj.timer = 0
                                logging.info("Feathershot transformed into platform")
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and charging:
                    charging = False
                    mx, my = event.pos
                    projectile = player.shoot(mx, my, power)
                    if projectile:
                        projectiles.add(projectile)
                        logging.info(f"Projectile launched: {projectile.ammo_type}")
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "paused"
                    elif event.mod & pygame.KMOD_SHIFT:
                        if event.key == pygame.K_1:
                            player.ammo_counts["regular"] = 10
                        elif event.key == pygame.K_2:
                            player.ammo_counts["bouncy"] = 10
                        elif event.key == pygame.K_3:
                            player.ammo_counts["piercing"] = 10
                        elif event.key == pygame.K_4:
                            player.ammo_counts["feathershot"] = 10
                        elif event.key == pygame.K_5:
                            player.health = min(player.health + 5, 100)
                        elif event.key == pygame.K_6:
                            new_segment = pygame.sprite.Sprite()
                            new_segment.image = pygame.Surface((20, 20))
                            new_segment.image.fill(RED)
                            new_segment.rect = new_segment.image.get_rect(center=snake.segments[-1].rect.center)
                            snake.segments.append(new_segment)
                        elif event.key == pygame.K_7:
                            if len(snake.segments) > 1:
                                snake.segments.pop()
                        elif event.key == pygame.K_8:
                            new_food = Food()
                            food_group.add(new_food)
                        elif event.key == pygame.K_9:
                            current_speed = math.hypot(snake.velocity[0], snake.velocity[1])
                            if current_speed > 0:
                                new_speed = min(current_speed * 1.1, 20)
                                scale = new_speed / current_speed
                                snake.velocity[0] *= scale
                                snake.velocity[1] *= scale
                        elif event.key == pygame.K_0:
                            current_speed = math.hypot(snake.velocity[0], snake.velocity[1])
                            if current_speed > 0:
                                new_speed = max(current_speed * 0.9, 1)
                                scale = new_speed / current_speed
                                snake.velocity[0] *= scale
                                snake.velocity[1] *= scale
                    else:
                        if event.key == pygame.K_1:
                            player.current_ammo = "regular"
                        elif event.key == pygame.K_2:
                            player.current_ammo = "bouncy"
                        elif event.key == pygame.K_3:
                            player.current_ammo = "piercing"
                        elif event.key == pygame.K_4:
                            player.current_ammo = "feathershot"
            elif game_state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "running"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_rect.collidepoint(event.pos):
                        game_state = "running"
                    elif quit_rect.collidepoint(event.pos):
                        logging.info("Quit selected from pause menu")
                        pygame.quit()
                        exit()
            elif game_state in ["won", "lost"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        logging.info("Quit key pressed")
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_r:
                        reset_game()

        if game_state == "running":
            keys = pygame.key.get_pressed()
            player.update(keys, platforms, projectiles, snake.segments, acid_group, food_group)
            snake.update(food_group, acid_group, projectiles)
            acid_group.update(platforms, snake.segments, projectiles)
            projectiles.update(platforms, snake.segments, acid_group, projectiles)

            # Check if snake is defeated
            for proj in projectiles:
                if proj.defeated_snake:
                    logging.info("Snake defeated, setting game_state to won")
                    game_state = "won"
                    proj.defeated_snake = False
                    break

            if player.health <= 0:
                logging.info("Player health <= 0, setting game_state to lost")
                game_state = "lost"

        # Draw everything
        screen.fill(BLACK)
        if game_state == "running":
            platforms.draw(screen)
            food_group.draw(screen)
            for segment in snake.segments:
                screen.blit(segment.image, segment.rect)
            player_group.draw(screen)
            projectiles.draw(screen)
            acid_group.draw(screen)

            # Draw aiming trajectory
            if charging:
                mx, my = pygame.mouse.get_pos()
                dx = mx - player.rect.centerx
                dy = my - player.rect.centery
                distance = (dx**2 + dy**2)**0.5
                if distance > 0:
                    multiplier = velocity_multipliers.get(player.current_ammo, 1.0)
                    v = power * 0.2 * multiplier
                    vx = v * (dx / distance)
                    vy = v * (dy / distance)
                    for t in range(30):
                        x = player.rect.centerx + vx * t
                        y = player.rect.centery + vy * t + 0.5 * 0.5 * t**2
                        if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
                            pygame.draw.circle(screen, WHITE, (int(x), int(y)), 2)

            # Draw UI
            screen.blit(font.render(f"Ammo: {player.current_ammo}", True, WHITE), (10, 10))
            screen.blit(font.render(f"Health: {int(player.health)}%", True, WHITE), (10, 50))
            power = min(power + charge_rate, max_power) if charging else power
        elif game_state == "paused":
            # Draw pause menu
            pause_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 100, 300, 200)
            pygame.draw.rect(screen, BLACK, pause_rect)
            screen.blit(paused_text, paused_rect)
            screen.blit(continue_text, continue_rect)
            screen.blit(quit_text, quit_rect)
        elif game_state == "won":
            screen.blit(font.render("Congratulations, you defeated the SkySnake!", True, WHITE), (WIDTH // 2 - 200, HEIGHT // 2))
            screen.blit(font.render("Press 'R' to restart or 'Q' to quit", True, WHITE), (WIDTH // 2 - 150, HEIGHT // 2 + 40))
        elif game_state == "lost":
            screen.blit(font.render("Game Over! You died.", True, WHITE), (WIDTH // 2 - 100, HEIGHT // 2))
            screen.blit(font.render("Press 'R' to restart or 'Q' to quit", True, WHITE), (WIDTH // 2 - 150, HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(60)
except Exception as e:
    logging.error(f"An error occurred: {e}", exc_info=True)
    pygame.quit()
    exit()