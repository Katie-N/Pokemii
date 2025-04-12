import pygame
import os
import mainMenu
import buttonsFromRect
import draw
import globalSettings
import cursor
import buttons

# Initialize Pygame
pygame.init()

# --- Functions ---

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
    if mainMenu.main_menu():
        main()
