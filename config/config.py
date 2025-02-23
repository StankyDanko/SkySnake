# config/config.py
# Screen dimensions
WIDTH = 1920  # Set to 1920x1080 as preferred resolution
HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)  # Added for platform color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
NEON_GREEN = (57, 255, 20)

# Ammo colors
ammo_colors = {
    "regular": WHITE,
    "bouncy": ORANGE,
    "piercing": RED,
    "feathershot": CYAN
}

# Velocity multipliers for different ammo types
velocity_multipliers = {
    "regular": 1.0,
    "bouncy": 0.8,
    "piercing": 1.2,
    "feathershot": 0.9
}

# Debug print to confirm loading
print("config.py loaded successfully")