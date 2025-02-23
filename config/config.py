# config.py
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
NEON_GREEN = (57, 255, 20)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

# Game dimensions
WIDTH = 1920
HEIGHT = 1080

# Ammo colors
ammo_colors = {
    "regular": RED,    
    "bouncy": PURPLE,
    "piercing": GREEN,
    "feathershot": CYAN
}

# Velocity multipliers for different ammo types
velocity_multipliers = {
    "regular": 1.0,
    "bouncy": 1.2,
    "piercing": 1.5,
    "feathershot": 0.8
}