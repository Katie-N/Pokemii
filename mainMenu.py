import pygame
import os
from typing import List
from constants import *
from buttons import Button
from actions import *
from game import Game

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
    pygame.draw.rect(button_surface, (0, 0, 0, 0), (0, 0, width, height))  # Last value is alpha (0-255)
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
    importMii_button,
    tradeMii_button,
    back_button,
    second_menu_visible,
    game: Game,
    game_menu_button #added game_menu_button
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if train_button.rect.collidepoint(mouse_pos): #changed to train_button.rect.collidepoint
                print("Train button clicked!")
            if compete_button.rect.collidepoint(mouse_pos): #changed to compete_button.rect.collidepoint
                print("Compete button clicked!")
                start_game(game)
                return False, False, second_menu_visible
            if next_button.rect.collidepoint(mouse_pos): #changed to next_button.rect.collidepoint
                return False, False, True
            if importMii_button.rect.collidepoint(mouse_pos): #changed to importMii_button.rect.collidepoint
                print("Import Mii button clicked!")
            if tradeMii_button.rect.collidepoint(mouse_pos): #changed to tradeMii_button.rect.collidepoint
                print("Trade Mii button clicked!")
            if back_button.rect.collidepoint(mouse_pos): #changed to back_button.rect.collidepoint
                return False, True, False
            if game_menu_button.rect.collidepoint(mouse_pos): #added the game menu button
                open_game_menu()
                return False, False, second_menu_visible
    return False, False, second_menu_visible

def draw_main_menu(screen, pic1, menu_offset, title_font, button_positions, game_menu_button): #added the game menu button
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
        WHITE,
        first_menu_surface,
    )
    compete_button = create_button(
        "Compete",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        first_menu_surface,
    )
    next_button = create_button(
        ">",
        next_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        WHITE,
        first_menu_surface,
    )
    game_menu_button.draw(first_menu_surface) #added the game menu button

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

    importMii_button = create_button(
        "Import Mii",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )
    tradeMii_button = create_button(
        "Trade Mii",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )
    back_button = create_button(
        "<",
        back_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )

    screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
    return importMii_button, tradeMii_button, back_button

def main_menu(game: Game):
    """Displays the main menu."""
    global current_state
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Load images
    assets_path = os.path.join(".", "assets", "menus")
    pic1, pic2 = load_images(assets_path)
    if pic1 is None or pic2 is None:
        return False

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Calculate button positions
    button_positions = calculate_button_positions()

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 20
    second_menu_visible = False
    # Create the "Game Menu" button
    game_menu_button = Button(20, 20, 150, 50, "Game Menu", LIGHT_BLUE, GRAY, pygame.font.Font(None, FONT_SIZE), open_game_menu) #added the game menu button

    running = True
    while running:
        # Handle events
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions, game_menu_button) #added the game menu button
        importMii_button, tradeMii_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)
        
        quit_game, back_to_main, second_menu_visible = handle_events(train_button, compete_button, next_button, importMii_button, tradeMii_button, back_button, second_menu_visible, game, game_menu_button) #added the game menu button
        if quit_game:
            return False
        if back_to_main:
            second_menu_visible = False
            current_state = GameState.MAIN_MENU

        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        # Draw everything
        screen.fill(BLACK)

        # Draw Main Menu
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions, game_menu_button) #added the game menu button

        # Draw Second Menu
        if second_menu_visible or menu_offset > -SCREEN_WIDTH:
            importMii_button, tradeMii_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)

        pygame.display.flip()
        if current_state != GameState.MAIN_MENU:
            running = False
    return True
