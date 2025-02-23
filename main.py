import pygame
import random
import math
import logging
import os  # Import os for file operations
from config.config import *
from classes.platform import Platform
from classes.projectile import Projectile
from classes.food import Food
from classes.acid_droplet import AcidDroplet
from classes.sky_snake import SkySnake
from classes.player import Player

# Rotate log files
if os.path.exists('game.log.3'):
    os.remove('game.log.3')
if os.path.exists('game.log.2'):
    os.rename('game.log.2', 'game.log.3')
if os.path.exists('game.log.1'):
    os.rename('game.log.1', 'game.log.2')

# Set up logging to game.log.1 for the current session
logging.basicConfig(
    filename='game.log.1',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'  # Overwrite if exists
)

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slingshot Hero")

# Font for rendering UI text
font = pygame.font.Font(None, 36)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Sprite groups
projectiles = pygame.sprite.Group()
platforms = pygame.sprite.Group()
food_group = pygame.sprite.Group()
acid_group = pygame.sprite.Group()
player = Player()
player_group = pygame.sprite.GroupSingle(player)
snake = SkySnake()

# Add initial platforms
ground = Platform(0, HEIGHT - 20, WIDTH, 20)
platforms.add(ground)

# Add initial food
for _ in range(3):
    food = Food()
    food_group.add(food)

# Charging mechanics
charging = False
power = 0
max_power = 100
charge_rate = 4

# Game state
game_state = "running"  # Possible states: "running", "won", "lost"

# Function to reset the game
def reset_game():
    global projectiles, food_group, acid_group, player, snake, game_state
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

logging.info("Game started")  # Log game start

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Quit event received")
                pygame.quit()
                exit()
            elif game_state == "running":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    charging = True
                    power = 0
                    logging.debug("Mouse button down: charging")
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and charging:
                    charging = False
                    mx, my = event.pos
                    projectile = player.shoot(mx, my, power)
                    if projectile:
                        projectiles.add(projectile)
                        logging.info(f"Projectile launched: {projectile.ammo_type}")
                elif event.type == pygame.KEYDOWN:
                    if event.mod & pygame.KMOD_SHIFT:
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
            player.update(keys, platforms, projectiles, snake.segments, acid_group)
            snake.update(food_group, acid_group, projectiles)
            acid_group.update(platforms, snake.segments, projectiles)
            projectiles.update(platforms, snake.segments, acid_group, projectiles)  # Updated call

            if player.health <= 0:
                game_state = "lost"
                logging.info("Game state changed to lost")

            # Check if snake's head is hit
            for proj in projectiles:
                if proj.rect.colliderect(snake.segments[0].rect) and not proj.is_platform:
                    game_state = "won"
                    proj.kill()
                    logging.info("Game state changed to won")
                    break

        screen.fill(BLACK)
        if game_state == "running":
            platforms.draw(screen)
            food_group.draw(screen)
            for segment in snake.segments:
                screen.blit(segment.image, segment.rect)
            player_group.draw(screen)
            projectiles.draw(screen)
            acid_group.draw(screen)

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

            screen.blit(font.render(f"Ammo: {player.current_ammo}", True, WHITE), (10, 10))
            screen.blit(font.render(f"Health: {int(player.health)}%", True, WHITE), (10, 50))
            power = min(power + charge_rate, max_power) if charging else power
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