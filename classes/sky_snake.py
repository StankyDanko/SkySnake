import pygame
import random
import math
from config.config import RED, WIDTH, HEIGHT
from classes.food import Food
from classes.acid_droplet import AcidDroplet

class SkySnake:
    def __init__(self):
        self.head_pos = [WIDTH / 2, HEIGHT / 2]
        self.velocity = [5, 0]
        self.spacing_frames = 4
        self.max_positions = 200
        self.positions = [self.head_pos.copy() for _ in range(self.max_positions)]
        self.segments = []
        for i in range(6):
            segment = pygame.sprite.Sprite()
            segment.image = pygame.Surface((20, 20))
            segment.image.fill(RED)
            segment.rect = segment.image.get_rect(center=self.head_pos)
            self.segments.append(segment)
        self.drop_timer = 0

    def update(self, food_group, acid_group, feathershot_platforms):
        self.head_pos[0] += self.velocity[0]
        self.head_pos[1] += self.velocity[1]

        if self.head_pos[0] < 0 or self.head_pos[0] > WIDTH:
            self.velocity[0] = -self.velocity[0]
        if self.head_pos[1] < 0 or self.head_pos[1] > HEIGHT:
            self.velocity[1] = -self.velocity[1]

        self.positions.append(self.head_pos.copy())
        if len(self.positions) > self.max_positions:
            self.positions.pop(0)

        for i, segment in enumerate(self.segments):
            index = - (i + 1) * self.spacing_frames - 1
            if -index < len(self.positions):
                segment.rect.center = self.positions[index]

        head_rect = self.segments[0].rect
        for food in food_group:
            if head_rect.colliderect(food.rect):
                food.kill()
                new_food = Food()
                food_group.add(new_food)
                new_segment = pygame.sprite.Sprite()
                new_segment.image = pygame.Surface((20, 20))
                new_segment.image.fill(RED)
                new_segment.rect = new_segment.image.get_rect(center=self.segments[-1].rect.center)
                self.segments.append(new_segment)

        for proj in feathershot_platforms:
            if proj.is_platform and head_rect.colliderect(proj.rect):
                proj.kill()
                new_segment = pygame.sprite.Sprite()
                new_segment.image = pygame.Surface((20, 20))
                new_segment.image.fill(RED)
                new_segment.rect = new_segment.image.get_rect(center=self.segments[-1].rect.center)
                self.segments.append(new_segment)

        self.drop_timer += 1
        if self.drop_timer >= 180:
            self.drop_timer = 0
            drop_segment = random.choice(self.segments)
            acid = AcidDroplet(drop_segment.rect.centerx, drop_segment.rect.bottom)
            acid_group.add(acid)

        if random.random() < 0.0167:
            angle = random.uniform(-45, 45)
            self.velocity = self.rotate_vector(self.velocity, angle)

    def rotate_vector(self, vec, angle_deg):
        angle_rad = math.radians(angle_deg)
        x, y = vec
        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
        return [new_x, new_y]