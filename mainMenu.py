import pygame
import os

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Screen dimensions
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

# --- Functions ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_button(text, x, y, width, height, text_color, surface):
    """Creates a transparent button and returns its rectangle."""
    button_rect = pygame.Rect(x, y, width, height)
    # Create a transparent surface for the button
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw a semi-transparent rectangle (optional, for a subtle button effect)
    pygame.draw.rect(button_surface, (0, 0, 0, 128), (0, 0, width, height))  # Last value is alpha (0-255)
    surface.blit(button_surface, (x,y))
    font = pygame.font.Font(None, 36)
    draw_text(text, font, text_color, surface, x + 10, y + 10)
    return button_rect

def load_images(assets_path):
    """Loads and scales background images."""
    try:
        pic1_path = os.path.join(assets_path, "MiiChannel.png")
        pic2_path = os.path.join(assets_path, "fightMenu.png")

        if os.path.exists(pic1_path):
            pic1 = pygame.image.load(pic1_path).convert()
            pic1 = pygame.transform.scale(pic1, SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic1_path}")

        if os.path.exists(pic2_path):
            pic2 = pygame.image.load(pic2_path).convert()
            pic2 = pygame.transform.scale(pic2, SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic2_path}")

        return pic1, pic2

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return None, None

def calculate_button_positions():
    """Calculates button positions relative to the screen."""
    button_y = int(SCREEN_HEIGHT * 0.77222)
    left_button_x = int(SCREEN_WIDTH * 0.1916)
    right_button_x = int(SCREEN_WIDTH * 0.52083)
    next_button_x = int(SCREEN_WIDTH * 0.9333)
    next_button_y = int(SCREEN_HEIGHT * 0.347222)
    back_button_x = int(SCREEN_WIDTH * 0.033333)

    return (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
    )

def handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed):
    """Handles the menu sliding logic."""
    if second_menu_visible:
        menu_offset -= menu_slide_speed
        if menu_offset <= -SCREEN_WIDTH:
            menu_offset = -SCREEN_WIDTH
    else:
        menu_offset += menu_slide_speed
        if menu_offset >= 0:
            menu_offset = 0
    return menu_offset

def handle_events(
    train_button,
    compete_button,
    next_button,
    option1_button,
    option2_button,
    back_button,
    second_menu_visible
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if train_button.collidepoint(mouse_pos):
                print("Play button clicked!")
            if compete_button.collidepoint(mouse_pos):
                print("Quit button clicked!")
                return True, False, second_menu_visible
            if next_button.collidepoint(mouse_pos):
                return False, False, True
            if option1_button.collidepoint(mouse_pos):
                print("Option 1 button clicked!")
            if option2_button.collidepoint(mouse_pos):
                print("Option 2 button clicked!")
            if back_button.collidepoint(mouse_pos):
                return False, True, False
    return False, False, second_menu_visible

def draw_main_menu(screen, pic1, menu_offset, title_font, button_positions):
    """Draws the main menu."""
    first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    first_menu_surface.blit(pic1, (0, 0))
    draw_text("My Game", title_font, WHITE, first_menu_surface, SCREEN_WIDTH // 2 - 80, 50)

    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        _,
    ) = button_positions

    train_button = create_button(
        "Train",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
    )
    compete_button = create_button(
        "Compete",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
    )
    next_button = create_button(
        "More",
        next_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
    )

    screen.blit(first_menu_surface, (menu_offset, 0))
    return train_button, compete_button, next_button

def draw_second_menu(screen, pic2, menu_offset, title_font, button_positions):
    """Draws the second menu."""
    second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    second_menu_surface.blit(pic2, (0, 0))
    draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2 - 80, 50)

    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
    ) = button_positions

    option1_button = create_button(
        "Option 1",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
    )
    option2_button = create_button(
        "Option 2",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
    )
    back_button = create_button(
        "Back",
        back_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
    )

    screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
    return option1_button, option2_button, back_button

def main_menu():
    """Displays the main menu."""
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Load images
    assets_path = os.path.join(".", "assets", "menus")
    pic1, pic2 = load_images(assets_path)
    if pic1 is None or pic2 is None:
        return

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Calculate button positions
    button_positions = calculate_button_positions()

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 20
    second_menu_visible = False

    running = True
    while running:
        # Handle events
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)
        option1_button, option2_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)
        
        quit_game, back_to_main, second_menu_visible = handle_events(train_button, compete_button, next_button, option1_button, option2_button, back_button, second_menu_visible)
        if quit_game:
            running = False
        if back_to_main:
            second_menu_visible = False

        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        # Draw everything
        screen.fill(BLACK)

        # Draw Main Menu
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)

        # Draw Second Menu
        if second_menu_visible or menu_offset > -SCREEN_WIDTH:
            option1_button, option2_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)

        pygame.display.flip()

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
