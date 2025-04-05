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

def create_button(text, x, y, width, height, text_color, surface, action=None, image_path=None):
    """Creates a button, optionally with an image, and returns its rectangle."""
    button_rect = pygame.Rect(x, y, width, height)
    # Create a transparent surface for the button
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw a semi-transparent rectangle (optional, for a subtle button effect)
    pygame.draw.rect(button_surface, (0, 0, 0, 0), (0, 0, width, height))  # Last value is alpha (0-255)
    
    if image_path:
        try:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (width, height))
            button_surface.blit(image, (0, 0))
        except pygame.error as e:
            print(f"Error loading image: {e}")
    
    surface.blit(button_surface, (x,y))
    font = pygame.font.Font(None, 36)
    draw_text(text, font, text_color, surface, x + 10, y + 10)
    return button_rect, action

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
    pick_save_x = 0
    pick_save_y = 0

    return (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
        pick_save_x,
        pick_save_y,
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
    save_button,
    importMii_button,
    tradeMii_button,
    back_button,
    second_menu_visible
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not second_menu_visible:
                if importMii_button[0].collidepoint(mouse_pos):
                    print("Import Mii button clicked!")
                    if importMii_button[1]:
                        importMii_button[1]()
                if tradeMii_button[0].collidepoint(mouse_pos):
                    print("Trade Mii button clicked!")
                    if tradeMii_button[1]:
                        tradeMii_button[1]()
                    return True, False, second_menu_visible
                if next_button[0].collidepoint(mouse_pos):
                    return False, False, True
            else:
                if train_button[0].collidepoint(mouse_pos):
                    print("Train button clicked!")
                    if train_button[1]:
                        train_button[1]()
                if compete_button[0].collidepoint(mouse_pos):
                    print("Compete button clicked!")
                    if compete_button[1]:
                        compete_button[1]()
                if save_button[0].collidepoint(mouse_pos):
                    print("Save button clicked!")
                        
                if back_button[0].collidepoint(mouse_pos):
                    return False, True, False
    return False, False, second_menu_visible

# DRAW MII CHANNEL MENU

def draw_main_menu(screen, pic1, menu_offset, title_font, button_positions):
    """Draws the main menu."""
    first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    first_menu_surface.blit(pic1, (0, 0))
    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
        pick_save_x,
        pick_save_y,
    ) = button_positions

    def import_mii_action():
        print("Importing Mii...")

    def trade_mii_action():
        print("Trading Mii...")

    importMii_button = create_button(
        "",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
        import_mii_action
    )
    tradeMii_button = create_button(
        "",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
        trade_mii_action
    )
    next_button = create_button(
        "",
        next_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        first_menu_surface,
    )

    screen.blit(first_menu_surface, (menu_offset, 0))
    return importMii_button, tradeMii_button, next_button

# DRAW TRAINING MENU

def draw_second_menu(screen, pic2, menu_offset, title_font, button_positions):
    """Draws the second menu."""
    second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    second_menu_surface.blit(pic2, (0, 0))
    (   button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
        pick_save_x,
        pick_save_y,
    ) = button_positions

    def train_action():
        print("Training...")

    def compete_action():
        print("Competing...")

    train_button = create_button(
        "",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
        train_action
    )
    compete_button = create_button(
        "",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
        compete_action
    )
    back_button = create_button(
        "",
        back_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        BUTTON_TEXT_COLOR,
        second_menu_surface,
    )
    
    assets_path = os.path.join(".", "assets")
    save_image_path = os.path.join(assets_path, "save.png")
    
    save_button = create_button(
        "Pick Save",
        pick_save_x,
        pick_save_y,
        50,
        50,
        BLACK,
        second_menu_surface,
        image_path=save_image_path
    )

    screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
    return train_button, compete_button, back_button, save_button

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
        importMii_button, tradeMii_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)
        train_button, compete_button, back_button, save_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)
        
        quit_game, back_to_main, second_menu_visible = handle_events(train_button, compete_button, next_button, save_button, importMii_button, tradeMii_button, back_button, second_menu_visible)
        if quit_game:
            running = False
        if back_to_main:
            second_menu_visible = False

        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        # Draw everything
        screen.fill(BLACK)

        # Draw Main Menu
        importMii_button, tradeMii_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)

        # Draw Second Menu
        if second_menu_visible or menu_offset > -SCREEN_WIDTH:
            train_button, compete_button, back_button, save_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)

        pygame.display.flip()

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
