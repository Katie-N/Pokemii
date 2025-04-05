import pygame
pygame.init()
import os
from game import Game
from mainMenu import main_menu
from buttons import Button
from drawing import *
from actions import *
from constants import *

# Initialize Pygame


# --- Main Game Loop ---
def main():
    """Main game loop."""
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Pokemii")

    # Fonts (Consolidated)
    font = pygame.font.Font(None, FONT_SIZE)
    large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
    console_font = pygame.font.Font(None, CONSOLE_FONT_SIZE)

    # Game instance
    game = Game()

    # Button Creation (Consolidated)
    from buttons import Button
    from actions import create_menu_buttons, create_credits_buttons, create_game_menu_buttons, create_options_buttons, close_console, open_game_menu #added open_game_menu
    menu_buttons = create_menu_buttons(font, game)
    credits_buttons = create_credits_buttons(font, game)
    game_menu_buttons = create_game_menu_buttons(font, game)
    options_buttons = create_options_buttons(font, game)
    close_console_button = Button(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 200, 20, 20, "X", RED, DARK_RED, console_font, close_console, game) #added the close console button
    # Create the "Game Menu" button
    game_menu_button = Button(20, 20, 150, 50, "Game Menu", LIGHT_BLUE, GRAY, font, open_game_menu) #added the game menu button

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if current_state == GameState.MAIN_MENU:
                    for button in menu_buttons:
                        button.handle_event(event)
                    game_menu_button.handle_event(event) #added the game menu button
                elif current_state == GameState.CREDITS:
                    for button in credits_buttons:
                        button.handle_event(event)
                elif current_state == GameState.GAME_MENU:
                    for button in game_menu_buttons:
                        button.handle_event(event)
                    if game.show_console:
                        close_console_button.handle_event(event)
                elif current_state == GameState.OPTIONS_MENU:
                    for button in options_buttons:
                        button.handle_event(event)

            screen.fill(WHITE)

            if current_state == GameState.MAIN_MENU:
                for button in menu_buttons:
                    button.draw(screen)
                game_menu_button.draw(screen) #added the game menu button
            elif current_state == GameState.CREDITS:
                draw_credits(screen, font, large_font, credits_buttons[0])
            elif current_state == GameState.GAME_MENU:
                # Draw everything else first
                draw_game_menu(screen, game_menu_buttons[-1], game_menu_buttons[:-1], game, close_console_button)
                draw_health_bar(screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
                draw_health_bar(screen, SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
                draw_experience_bar(screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
                draw_turn(screen, game)
            elif current_state == GameState.OPTIONS_MENU:
                draw_options_menu(screen, options_buttons[-1], options_buttons[:-1])

            pygame.display.flip()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

# --- Entry Point ---
if __name__ == "__main__":
    game = Game()
    if main_menu(game):
        main()
