# food.py
import pygame
import random
from config import ORANGE, WIDTH, HEIGHT

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))