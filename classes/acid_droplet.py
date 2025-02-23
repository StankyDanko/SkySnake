# classes/acid_droplet.py
import pygame
from config.config import NEON_GREEN, HEIGHT

class AcidDroplet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(NEON_GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = [x, y]
        self.vy = 5
        self.gravity = 0.5

    def update(self, platforms, snake_segments, feathershot_platforms):
        self.pos[1] += self.vy
        self.vy += self.gravity
        self.rect.center = (int(self.pos[0]), int(self.pos[1]))

        for proj in feathershot_platforms:
            if proj.is_platform and self.rect.colliderect(proj.rect):
                proj.kill()
                self.kill()

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.kill()

        if self.rect.top > HEIGHT:
            self.kill()