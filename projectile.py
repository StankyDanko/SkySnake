# projectile.py
import pygame
from config import ammo_colors, WIDTH, HEIGHT

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
        self.gravity = 0.5
        self.stopped = False
        self.ammo_type = ammo_type
        self.is_platform = False
        self.prev_vy = vy
        self.bounces = 0
        self.max_bounces = 3 if ammo_type == "bouncy" else 0
        self.timer = 0

    def update(self, platforms, snake_segments, acid_group):
        if not self.stopped:
            self.pos[0] += self.vx
            self.pos[1] += self.vy
            self.vy += self.gravity
            self.rect.center = (int(self.pos[0]), int(self.pos[1]))

            for segment in snake_segments:
                if self.rect.colliderect(segment.rect) and not self.is_platform:
                    if len(snake_segments) > 1:
                        snake_segments.pop()
                        if self.ammo_type != "piercing":
                            self.kill()
                    elif segment == snake_segments[0]:
                        print("You win!")
                        global running
                        running = False
                        self.kill()

            if self.ammo_type == "feathershot" and not self.is_platform:
                if self.prev_vy <= 0 and self.vy > 0:
                    self.stopped = True
                    self.is_platform = True
                    self.image = pygame.Surface((30, 30))
                    self.image.fill(CYAN)
                    self.rect = self.image.get_rect(center=self.rect.center)
                    self.timer = 0

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
            elif self.ammo_type == "piercing":
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top:
                            self.stopped = True
                            self.vy = 0
                            self.vx = 0
            else:
                for platform in platforms:
                    if self.rect.colliderect(platform.rect):
                        if self.vy > 0 and self.rect.bottom - self.vy <= platform.rect.top:
                            self.stopped = True
                            self.vy = 0
                            self.vx = 0

            self.prev_vy = self.vy

            if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT:
                self.kill()

        if self.is_platform:
            self.timer += 1
            if self.timer >= 3600:
                self.kill()