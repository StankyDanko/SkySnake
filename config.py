# config.py
# Game settings and constants

WIDTH, HEIGHT = 1920, 1080
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
NEON_GREEN = (57, 255, 20)

ammo_colors = {
    "regular": RED,
    "bouncy": PURPLE,
    "piercing": GREEN,
    "feathershot": CYAN,
    "acid": NEON_GREEN
}

velocity_multipliers = {
    "regular": 2.5,
    "bouncy": 1.25,
    "piercing": 1.0,
    "feathershot": 1.0
}