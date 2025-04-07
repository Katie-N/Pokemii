import pygame
import globalSettings
import save_file_manager
import draw
from cursor import specialCursor

def create_save_menu_buttons(images):
    """Creates the save menu buttons."""
    save_menu_buttons = []
    for saveId in save_file_manager.save_manager.get_save_file_ids():
        saveData = save_file_manager.save_manager.load_save_file(saveId)
        save_menu_buttons.append(
            (
                pygame.Rect(0, 0, 0, 0),
                lambda saveData=saveData: save_file_manager.save_manager.login_user(saveData),
                saveData["Name"],
            )
        )
    save_menu_buttons.append(
        (
            pygame.Rect(0, 0, 0, 0),
            lambda: handle_new_save(),
            "New Save",
        )
    )
    return save_menu_buttons

def handle_new_save():
    """Handles the creation of a new save by asking for the player's name."""
    screen = globalSettings.screen
    font = pygame.font.Font(None, 48)
    input_box = pygame.Rect(200, 200, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input box
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                # Change the color of the input box
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        # Send the entered name to the save manager
                        save_file_manager.save_manager.new_player(name=text)
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(globalSettings.BLACK)
        # Render the current text
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long
        width = max(400, txt_surface.get_width() + 10)
        input_box.w = width
        # Draw the text box
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        # Display instructions
        instructions = font.render("Enter your name and press Enter:", True, (255, 255, 255))
        screen.blit(instructions, (200, 150))

        pygame.display.flip()

def save_menu(screen, title_font, close_button_rect):
    """Displays the save menu."""
    save_menu_buttons = create_save_menu_buttons(globalSettings.images)
    running = True
    while running:
        screen.fill(globalSettings.BLACK)
        draw.draw_save_menu(screen, save_menu_buttons)

        # Draw close button
        pygame.draw.rect(screen, (255, 0, 0), close_button_rect)
        close_text = title_font.render("Close", True, (255, 255, 255))
        screen.blit(
            close_text,
            (
                close_button_rect.x + (close_button_rect.width - close_text.get_width()) // 2,
                close_button_rect.y + (close_button_rect.height - close_text.get_height()) // 2,
            ),
        )

        specialCursor(globalSettings.screen, globalSettings.images["cursor.png"])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if close_button_rect.collidepoint(mouse_pos):
                    running = False
                for button in save_menu_buttons:
                    if button[0].collidepoint(mouse_pos) and button[1]:
                        button[1]()
                        # Regenerate the save menu buttons after a save is selected just in case it was a new save
                        save_menu_buttons = create_save_menu_buttons(images)