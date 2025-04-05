import pygame
import os
from button import Button

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
BUTTON_COLOR = BLUE
BUTTON_TEXT_COLOR = WHITE

# --- Functions ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def load_button_images(assets_path, button_name):
    """Loads button images for a specific button."""
    try:
        normal_image = load_image(assets_path, f"{button_name}_normal.png")
        hover_image = load_image(assets_path, f"{button_name}_hover.png")
        pressed_image = load_image(assets_path, f"{button_name}_pressed.png")

        if normal_image is None or hover_image is None or pressed_image is None:
            raise FileNotFoundError(
                f"Missing one or more images for button: {button_name}"
            )

        return normal_image, hover_image, pressed_image

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading button images: {e}")
        return None, None, None
    
def load_image(path, imageName):
    """Loads and scales background images."""
    try:
        pic_path = os.path.join(path, imageName)

        if os.path.exists(pic_path):
            pic = pygame.image.load(pic_path).convert_alpha()
        else:
            raise FileNotFoundError(f"Image file not found: {pic_path}")

        # Scale the image to fit the screen while maintaining aspect ratio
        image_ratio = pic.get_width() / pic.get_height()
        screen_ratio = SCREEN_WIDTH / SCREEN_HEIGHT

        if image_ratio > screen_ratio:
            # Image is wider than the screen, scale by width
            scale_factor = SCREEN_WIDTH / pic.get_width()
            new_height = int(pic.get_height() * scale_factor)
            pic = pygame.transform.scale(pic, (SCREEN_WIDTH, new_height))
        else:
            # Image is taller than the screen, scale by height
            scale_factor = SCREEN_HEIGHT / pic.get_height()
            new_width = int(pic.get_width() * scale_factor)
            pic = pygame.transform.scale(pic, (new_width, SCREEN_HEIGHT))

        return pic

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return None

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
    import_mii_button,
    trade_mii_button,
    back_button,
    second_menu_visible,
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            if train_button and train_button.handle_event(event):
                print("Play button clicked!")
            if compete_button and compete_button.handle_event(event):
                print("Quit button clicked!")
                return True, False, second_menu_visible
            if next_button and next_button.handle_event(event):
                return False, False, True
            if import_mii_button and import_mii_button.handle_event(event):
                print("Import Mii button clicked!")
            if trade_mii_button and trade_mii_button.handle_event(event):
                print("Trade Mii button clicked!")
            if back_button and back_button.handle_event(event):
                return False, True, False
    return False, False, second_menu_visible

def draw_main_menu(
    screen,
    pic1,
    menu_offset,
    title_font,
    button_positions,
    train_button,
    compete_button,
    next_button,
):
    """Draws the main menu."""
    first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    first_menu_surface.blit(pic1, (0, 0))
    draw_text("My Game", title_font, WHITE, first_menu_surface, SCREEN_WIDTH // 2, 50)

    if train_button:
        train_button.draw(first_menu_surface)
    if compete_button:
        compete_button.draw(first_menu_surface)
    if next_button:
        next_button.draw(first_menu_surface)

    screen.blit(first_menu_surface, (menu_offset, 0))
    return train_button, compete_button, next_button

def draw_second_menu(
    screen,
    pic2,
    menu_offset,
    title_font,
    button_positions,
    import_mii_button,
    trade_mii_button,
    back_button,
):
    """Draws the second menu."""
    second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    second_menu_surface.blit(pic2, (0, 0))
    draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2, 50)

    if import_mii_button:
        import_mii_button.draw(second_menu_surface)
    if trade_mii_button:
        trade_mii_button.draw(second_menu_surface)
    if back_button:
        back_button.draw(second_menu_surface)

    screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
    return import_mii_button, trade_mii_button, back_button

def main_menu():
    """Displays the main menu."""
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Load images
    assets_path = os.path.join(".", "assets")
    menus_path = os.path.join(assets_path, "menus")
    pic1 = load_image(menus_path, "MiiChannel.png")
    pic2 = load_image(menus_path, "fightMenu.png")
    if pic1 is None or pic2 is None:
        return

    # Load button images
    buttons_path = os.path.join(assets_path, "buttons")
    wii_button_normal, wii_button_hover, wii_button_pressed = load_button_images(
        buttons_path, "wiibutton"
    )
    train_normal, train_hover, train_pressed = wii_button_normal, wii_button_hover, wii_button_pressed
    compete_normal, compete_hover, compete_pressed = wii_button_normal, wii_button_hover, wii_button_pressed
    import_mii_normal, import_mii_hover, import_mii_pressed = wii_button_normal, wii_button_hover, wii_button_pressed
    trade_mii_normal, trade_mii_hover, trade_mii_pressed = wii_button_normal, wii_button_hover, wii_button_pressed
    next_normal, next_hover, next_pressed = load_button_images(buttons_path, "next")
    back_normal, back_hover, back_pressed = load_button_images(buttons_path, "back")

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Calculate button positions
    button_positions = calculate_button_positions()
    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
    ) = button_positions

        # Create buttons
    train_button = None
    compete_button = None
    next_button = None
    import_mii_button = None
    trade_mii_button = None
    back_button = None
    
    if train_normal:
        train_button = Button(
            left_button_x, button_y, train_normal, train_hover, train_pressed, "Train", MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT
        )
    if compete_normal:
        compete_button = Button(
            right_button_x, button_y, compete_normal, compete_hover, compete_pressed, "Compete", MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT
        )
    if next_normal:
        next_button = Button(
            next_button_x, next_button_y, next_normal, next_hover, next_pressed, "More", NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT
        )
    if import_mii_normal:
        import_mii_button = Button(
            left_button_x,
            button_y,
            import_mii_normal,
            import_mii_hover,
            import_mii_pressed,
            "Import Mii",
            MAIN_BUTTON_WIDTH,
            MAIN_BUTTON_HEIGHT
        )
    if trade_mii_normal:
        trade_mii_button = Button(
            right_button_x,
            button_y,
            trade_mii_normal,
            trade_mii_hover,
            trade_mii_pressed,
            "Trade Mii",
            MAIN_BUTTON_WIDTH,
            MAIN_BUTTON_HEIGHT
        )
    if back_normal:
        back_button = Button(
            back_button_x, next_button_y, back_normal, back_hover, back_pressed, "Back", NAV_BUTTON_WIDTH, NAV_BUTTON_HEIGHT
        )

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 20
    second_menu_visible = False

    running = True
    while running:
        # Handle events

        quit_game, back_to_main, second_menu_visible = handle_events(
            train_button,
            compete_button,
            next_button,
            import_mii_button,
            trade_mii_button,
            back_button,
            second_menu_visible,
        )
        if quit_game:
            running = False
        if back_to_main:
            second_menu_visible = False

        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        # Draw everything
        screen.fill(BLACK)

        # Draw Main Menu
        train_button, compete_button, next_button = draw_main_menu(
            screen, pic1, menu_offset, title_font, button_positions, train_button, compete_button, next_button
        )

        # Draw Second Menu
        if second_menu_visible or menu_offset > -SCREEN_WIDTH:
            import_mii_button, trade_mii_button, back_button = draw_second_menu(
                screen,
                pic2,
                menu_offset,
                title_font,
                button_positions,
                import_mii_button,
                trade_mii_button,
                back_button,
            )

        pygame.display.flip()

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
