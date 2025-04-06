import pygame
# --- Constants ---
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (150, 0, 0)
RED_COLOR = (255, 0, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Button dimensions
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70
BUTTON_SPACING = 130

# Font
TURN_FONT_SIZE = 50
FONT_SIZE = 36
LARGE_FONT_SIZE = 72

# ----------------------------------- #
# Global Variables for the Game Logic
currentState = None

# From mainMenu.py

# Screen dimensions
pygame.init()
infoObject = pygame.display.Info()
MAX_WIDTH = infoObject.current_w
MAX_HEIGHT = infoObject.current_h

if MAX_WIDTH / MAX_HEIGHT >= 16 / 9:
    SCREEN_HEIGHT = MAX_HEIGHT
    SCREEN_WIDTH = int(SCREEN_HEIGHT * 16 / 9)
else:
    SCREEN_WIDTH = MAX_WIDTH
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 9 / 16)

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Button dimensions
MAIN_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.286458)
MAIN_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 0.1398148)
NAV_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.0322916)
NAV_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 0.084259)
BUTTON_TEXT_COLOR = WHITE

# --- New Global Variable ---
SAVE_BUTTON_SIZE = 100  # Set the desired size here
SAVE_MENU_BUTTON_WIDTH = 300 # New constant for save menu button width
SAVE_MENU_BUTTON_HEIGHT = 60 # New constant for save menu button height
SAVE_MENU_BUTTON_SPACING = 70 # New constant for save menu button spacing
