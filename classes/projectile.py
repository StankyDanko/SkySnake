# classes/projectile.py
import pygame
import logging  # Import logging module
from config.config import ammo_colors, WIDTH, HEIGHT, CYAN

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, ammo_type):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(ammo_colors[ammo_type])
        self.rect = self.image.get_rect()
        self.pos = [x, y]
        self.rect.center = (int(x), int(y))
        self.vx = vx
        self.vy = vy
        self.gravity = 0.3 if ammo_type == "feathershot" else 0.5  # Reduced gravity for feathershot
        self.stopped = False
        self.ammo_type = ammo_type
        self.is_platform = False
        self.prev_vy = vy
        self.bounces = 0
        self.max_bounces = 3 if ammo_type == "bouncy" else 0
        self.timer = 0
        self.defeated_snake = False  # Flag to indicate if snake is defeated

    def update(self, platforms, snake_segments, acid_group, projectiles):
        if not self.stopped:
            logging.debug(f"Updating projectile: pos={self.pos}, stopped={self.stopped}")
            self.pos[0] += self.vx
            self.pos[1] += self.vy
            self.vy += self.gravity
            self.rect.center = (int(self.pos[0]), int(self.pos[1]))

            # Check collision with snake segments
            for segment in snake_segments:
                if self.rect.colliderect(segment.rect) and not self.stopped:
                    if len(snake_segments) > 1:
                        snake_segments.pop()  # Remove last body segment
                        logging.info(f"Removed segment, new length: {len(snake_segments)}")
                        if self.ammo_type != "piercing":
                            self.kill()
                    else:
                        logging.info("Defeating snake")
                        self.defeated_snake = True
                        self.kill()

            # Handle bouncy ammo
            if self.ammo_type == "bouncy":
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top:
                            self.rect.bottom = platform.rect.top
                            self.vy = -self.vy * 0.8
                            self.bounces += 1
                            if self.bounces >= self.max_bounces:
                                self.stopped = True
                                self.vy = 0
                                self.vx = 0
                for proj in projectiles:
                    if proj.is_platform and self.rect.colliderect(proj.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= proj.rect.top:
                            self.rect.bottom = proj.rect.top
                            self.vy = -self.vy * 0.8
                            self.bounces += 1
                            if self.bounces >= self.max_bounces:
                                self.stopped = True
                                self.vy = 0
                                self.vx = 0
            # Handle piercing ammo
            elif self.ammo_type == "piercing":
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top:
                            self.stopped = True
                            self.vy = 0
                            self.vx = 0
            # Handle regular and feathershot ammo
            else:
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top:
                            self.stopped = True
                            self.vy = 0
                            self.vx = 0

            self.prev_vy = self.vy

            # Remove projectile if it goes off-screen
            if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
                self.kill()

        # Handle platform timer
        if self.is_platform:
            self.timer += 1
            if self.timer >= 3600:
                self.kill()