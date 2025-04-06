import pygame
import os
import mainMenu
import globalSettings
from game import GameState

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Screen dimensions
try:
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
except pygame.error as e:
    print(f"Error initializing Pygame in main: {e}")
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 900
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# --- Functions ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    try:
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    except Exception as e:
        print(f"Error drawing text: {e}")

def main():
    """Main game loop."""
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("My Game")
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Game Logic ---
        # (Add your game logic here)

        # Draw everything
        screen.fill(GREEN)
        draw_text("Game is Running!", title_font, BLACK, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 32)

        pygame.display.flip()

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    try:
        # --- Temporary Debug Mode ---
        DEBUG_MODE = True  # Set to True to skip to the game menu, False to go to the main menu

        if DEBUG_MODE:
            globalSettings.current_state = GameState.GAME_MENU  # Directly set the game state
            import menu5_optimize
            menu5_optimize.main()
        else:
            mainMenu.main_menu()
    except Exception as e:
        print(f"Error running main menu: {e}")
