import globalSettings
import buttonsFromRect
import draw
import pygame
import os
import save_file_manager
from cursor import specialCursor
import saveMenu  # Import the saveMenu module
# from runGame import run_game
from train import beginTraining
from compete import beginCompeting
from importMii import importMiis
from tradeMii import tradeMiis

# Initialize Pygame
pygame.init()
# Initalize the screen
globalSettings.screen = pygame.display.set_mode(globalSettings.SCREEN_SIZE)

def load_images():
    """Loads and scales all of the images as soon as the game is launched"""
    images = {}
    try:
        pic1_path = os.path.join(globalSettings.menu_path, "MiiChannel.png")
        pic2_path = os.path.join(globalSettings.menu_path, "fightMenu.png")
        save_image_path = os.path.join(globalSettings.menu_path, "save.png")
        cursor_image_path = os.path.join(globalSettings.menu_path, "cursor.png")
        backgroundPicPath = os.path.join(globalSettings.fight_background_path, "blurryWuhu.png")
        fightingMatsPath = os.path.join(globalSettings.fight_background_path, "fightingMats.png")
        
        if os.path.exists(pic1_path):
            images["mii_channel"] = pygame.image.load(pic1_path).convert()
            images["mii_channel"] = pygame.transform.scale(images["mii_channel"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic1_path}")

        if os.path.exists(pic2_path):
            images["fight_menu"] = pygame.image.load(pic2_path).convert()
            images["fight_menu"] = pygame.transform.scale(images["fight_menu"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic2_path}")
        
        if os.path.exists(save_image_path):
            images["save_button"] = pygame.image.load(save_image_path).convert_alpha()
            images["save_button"] = pygame.transform.scale(images["save_button"], (globalSettings.SAVE_BUTTON_SIZE, globalSettings.SAVE_BUTTON_SIZE))
        else:
            raise FileNotFoundError(f"Image file not found: {save_image_path}")

        if os.path.exists(cursor_image_path):
            images["cursor"] = pygame.image.load(cursor_image_path).convert_alpha()
            images["cursor"] = pygame.transform.scale(images["cursor"], (75,75))
        else:
            raise FileNotFoundError(f"Image file not found: {cursor_image_path}")

        if os.path.exists(backgroundPicPath):
            images["blurryWuhu"] = pygame.image.load(backgroundPicPath).convert()
            images["blurryWuhu"] = pygame.transform.scale(images["blurryWuhu"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {backgroundPicPath}")    
    
        if os.path.exists(fightingMatsPath):
            images["fightingMats"] = pygame.image.load(fightingMatsPath).convert_alpha()
            images["fightingMats"] = pygame.transform.scale(images["fightingMats"], globalSettings.SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {fightingMatsPath}")    
        
        return images

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return {}

def handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed):
    """Handles the menu sliding logic."""
    if second_menu_visible:
        menu_offset -= menu_slide_speed
        if menu_offset <= -globalSettings.SCREEN_WIDTH:
            menu_offset = -globalSettings.SCREEN_WIDTH
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
    save_button,
    save_menu_visible,
    close_button_rect,
    images,
    title_font
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible, save_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not second_menu_visible:
                if importMii_button[0].collidepoint(mouse_pos):
                    print("Import Mii button clicked!")
                    if importMii_button[1]:
                        importMii_button[1]()
                        importMiis()
                if tradeMii_button[0].collidepoint(mouse_pos):
                    print("Trade Mii button clicked!")
                    if tradeMii_button[1]:
                        tradeMii_button[1]()
                        tradeMiis()
                    return True, False, second_menu_visible, save_menu_visible
                if next_button[0].collidepoint(mouse_pos):
                    return False, False, True, save_menu_visible
            else:
                if train_button[0].collidepoint(mouse_pos):
                    print("Train button clicked!")
                    if train_button[1]:
                        train_button[1]()
                        beginTraining()
                if compete_button[0].collidepoint(mouse_pos):
                    print("Compete button clicked!")
                    if compete_button[1]:
                        compete_button[1]()
                        beginCompeting()
                        
                if back_button[0].collidepoint(mouse_pos):
                    return False, True, False, save_menu_visible
            if save_button[0].collidepoint(mouse_pos):
                print("Save button clicked!")
                saveMenu.save_menu(globalSettings.screen, title_font, close_button_rect)  # Call saveMenu
                return False, False, second_menu_visible, False
    return False, False, second_menu_visible, save_menu_visible

def main_menu():
    """Displays the main menu."""

    pygame.display.set_caption("Main Menu")

    # Load images
    globalSettings.images = load_images()
    if not globalSettings.images:
        return

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Calculate button positions
    button_positions = buttonsFromRect.calculate_button_positions()
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

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 100
    second_menu_visible = False
    save_menu_visible = False

    # --- Frame Rate ---
    clock = pygame.time.Clock()
    FPS = 60  # Set the desired frame rate

    # --- Create the save button ---
    save_button = buttonsFromRect.create_button(
        "Pick Save",
        pick_save_x,
        pick_save_y,
        globalSettings.SAVE_BUTTON_SIZE,
        globalSettings.SAVE_BUTTON_SIZE,
        globalSettings.BLACK,
        globalSettings.screen,
        None,
        image=globalSettings.images["save_button"]
    )

    # Create the close button for the save menu
    close_button_rect = pygame.Rect(50, 50, 100, 50)  # Example position and size

    # This infinite loop drives the code. It is the main scheduler and handles all the logic
    running = True
    while running:
        # EVENT HANDLING
        importMii_button, tradeMii_button, next_button = draw.draw_main_menu(globalSettings.screen, globalSettings.images, menu_offset, title_font, button_positions)
        train_button, compete_button, back_button = draw.draw_second_menu(globalSettings.screen, globalSettings.images, menu_offset, title_font, button_positions)
        
        quit_game, back_to_main, second_menu_visible, save_menu_visible = handle_events(
            train_button,
            compete_button,
            next_button,
            importMii_button,
            tradeMii_button,
            back_button,
            second_menu_visible,
            save_button,
            save_menu_visible,
            close_button_rect,
            globalSettings.images,
            title_font
        )
        if quit_game:
            running = False
        if back_to_main:
            second_menu_visible = False

        # DRAWING
        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        globalSettings.screen.fill(globalSettings.BLACK)

        # Draw Main Menu
        importMii_button, tradeMii_button, next_button = draw.draw_main_menu(globalSettings.screen, globalSettings.images, menu_offset, title_font, button_positions)

        # Draw Second Menu
        if second_menu_visible or menu_offset > -globalSettings.SCREEN_WIDTH:
            train_button, compete_button, back_button = draw.draw_second_menu(globalSettings.screen, globalSettings.images, menu_offset, title_font, button_positions)
        
        # Draw the save button
        save_button[0].x = pick_save_x
        save_button[0].y = pick_save_y
        save_button[0].width = globalSettings.SAVE_BUTTON_SIZE
        save_button[0].height = globalSettings.SAVE_BUTTON_SIZE
        save_button[0].topleft = (pick_save_x, pick_save_y)
        globalSettings.screen.blit(globalSettings.images["save_button"], (pick_save_x, pick_save_y))

        specialCursor(globalSettings.screen, globalSettings.images["cursor"])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
