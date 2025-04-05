import pygame

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = BLUE
BUTTON_TEXT_COLOR = WHITE

# --- Functions ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_button(text, x, y, width, height, color, text_color, surface):
    """Creates a button and returns its rectangle."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    font = pygame.font.Font(None, 36)
    draw_text(text, font, text_color, surface, x + 10, y + 10)
    return button_rect

def main_menu():
    """Displays the main menu."""
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Button positions
    play_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    play_button_y = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 75
    quit_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    quit_button_y = SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 - 25
    slide_button_x = SCREEN_WIDTH - BUTTON_WIDTH
    slide_button_y = SCREEN_HEIGHT - BUTTON_HEIGHT

    # Create buttons
    play_button = create_button("Play", play_button_x, play_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
    quit_button = create_button("Quit", quit_button_x, quit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
    slide_button = create_button("More", slide_button_x, slide_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)

    # --- Second Menu Variables ---
    second_menu_offset = SCREEN_WIDTH  # Start off-screen to the right
    second_menu_visible = False
    menu_slide_speed = 10
    
    # Second Menu Buttons
    option1_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    option1_button_y = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 75
    option2_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    option2_button_y = SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 - 25
    back_button_x = 0
    back_button_y = SCREEN_HEIGHT - BUTTON_HEIGHT
    
    option1_button = create_button("Option 1", option1_button_x, option1_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
    option2_button = create_button("Option 2", option2_button_x, option2_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
    back_button = create_button("Back", back_button_x, back_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    print("Play button clicked!")
                    # Add game start logic here
                if quit_button.collidepoint(mouse_pos):
                    print("Quit button clicked!")
                    running = False
                if slide_button.collidepoint(mouse_pos):
                    second_menu_visible = True
                if second_menu_visible:
                    if option1_button.collidepoint(mouse_pos):
                        print("Option 1 button clicked!")
                    if option2_button.collidepoint(mouse_pos):
                        print("Option 2 button clicked!")
                    if back_button.collidepoint(mouse_pos):
                        second_menu_visible = False

        # --- Menu Sliding Logic ---
        if second_menu_visible:
            second_menu_offset -= menu_slide_speed
            if second_menu_offset <= 0:
                second_menu_offset = 0
        else:
            second_menu_offset += menu_slide_speed
            if second_menu_offset >= SCREEN_WIDTH:
                second_menu_offset = SCREEN_WIDTH

        # Draw everything
        screen.fill(GRAY)  # Background color
        
        # Draw Main Menu
        if second_menu_offset >= SCREEN_WIDTH:
          draw_text("My Game", title_font, WHITE, screen, SCREEN_WIDTH // 2 - 80, 50)
          create_button("Play", play_button_x, play_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
          create_button("Quit", quit_button_x, quit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)
          create_button("More", slide_button_x, slide_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, screen)

        # Draw Second Menu
        if second_menu_offset < SCREEN_WIDTH:
            second_menu_surface = pygame.Surface(SCREEN_SIZE)
            second_menu_surface.fill(LIGHT_BLUE)
            draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2 - 80, 50)
            create_button("Option 1", option1_button_x, option1_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, second_menu_surface)
            create_button("Option 2", option2_button_x, option2_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, second_menu_surface)
            create_button("Back", back_button_x, back_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_TEXT_COLOR, second_menu_surface)
            screen.blit(second_menu_surface, (second_menu_offset, 0))

        pygame.display.flip()  # Update the display

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
