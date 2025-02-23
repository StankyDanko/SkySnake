import pygame
import logging  # Import logging module
from config import WHITE, WIDTH, HEIGHT, velocity_multipliers
from projectile import Projectile

# Configure logging for player actions
logging.basicConfig(filename='game.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = 5
        self.jump_power = -12
        self.vy = 0
        self.gravity = 0.5
        self.on_ground = False
        self.health = 100
        self.current_ammo = "regular"
        self.ammo_types = ["regular", "bouncy", "piercing", "feathershot"]
        self.ammo_counts = {"regular": 10, "bouncy": 5, "piercing": 3, "feathershot": 2}
        self.last_y = self.rect.y

    def update(self, keys, platforms, projectiles, snake_segments, acid_group):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

        self.vy += self.gravity
        self.rect.y += self.vy

        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top + 2:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                    fall_height = self.last_y - self.rect.y
                    if fall_height > 100:
                        damage = (fall_height / HEIGHT) * 45
                        self.health -= damage
                        if self.health < 0:
                            self.health = 0
                elif self.vy == 0 and self.rect.bottom <= platform.rect.top + 2:
                    self.on_ground = True
        self.last_y = self.rect.y

        for proj in projectiles:
            if proj.is_platform and self.rect.colliderect(proj.rect):
                if self.vy > 0 and self.rect.bottom - self.vy <= proj.rect.top + 2:
                    self.rect.bottom = proj.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy == 0 and self.rect.bottom <= proj.rect.top + 2:
                    self.on_ground = True

        for segment in snake_segments:
            if self.rect.colliderect(segment.rect):
                self.health -= 0.666

        for acid in acid_group:
            if self.rect.colliderect(acid.rect):
                self.health -= 10
                acid.kill()

        for proj in projectiles:
            if proj.stopped and not proj.is_platform and self.rect.colliderect(proj.rect):
                if proj.ammo_type in self.ammo_counts:
                    self.ammo_counts[proj.ammo_type] += 1
                    proj.kill()

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shoot(self, mx, my, power):
        if self.current_ammo in self.ammo_counts and self.ammo_counts[self.current_ammo] > 0:
            self.ammo_counts[self.current_ammo] -= 1
            dx = mx - self.rect.centerx
            dy = my - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                multiplier = velocity_multipliers.get(self.current_ammo, 1.0)
                v = power * 0.2 * multiplier
                vx = v * (dx / distance)
                vy = v * (dy / distance)
                logging.info(f"Shooting {self.current_ammo} projectile with power {power}")
                return Projectile(self.rect.centerx, self.rect.centery, vx, vy, self.current_ammo)
        else:
            logging.warning(f"Cannot shoot: No ammo for {self.current_ammo}")
        return None