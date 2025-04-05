import globalSettings
import pygame
from game import Game, GameState
import draw
import buttons
import buttonsFromRect

# --- Main Game Loop ---
def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode(globalSettings.SCREEN_SIZE)
    pygame.display.set_caption("Pokemii Menu")

    # Fonts
    font = pygame.font.Font(None, globalSettings.FONT_SIZE)
    large_font = pygame.font.Font(None, globalSettings.LARGE_FONT_SIZE)

    # Game instance
    game = Game()

    # --- Button Creation ---
    menu_buttons = buttons.create_menu_buttons(font, game)
    credits_buttons = buttons.create_credits_buttons(font, game)
    game_menu_buttons = buttons.create_game_menu_buttons(font, game)
    options_buttons = buttons.create_options_buttons(font, game)

    globalSettings.current_state = GameState.MENU

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if globalSettings.current_state == GameState.MENU:
                    for button in menu_buttons:
                        button.handle_event(event)
                elif globalSettings.current_state == GameState.CREDITS:
                    for button in credits_buttons:
                        button.handle_event(event)
                elif globalSettings.current_state == GameState.GAME_MENU:
                    for button in game_menu_buttons:
                        button.handle_event(event)
                elif globalSettings.current_state == GameState.OPTIONS:
                    for button in options_buttons:
                        button.handle_event(event)

            screen.fill(globalSettings.WHITE)

            if globalSettings.current_state == GameState.MENU:
                for button in menu_buttons:
                    button.draw(screen)
            elif globalSettings.current_state == GameState.CREDITS:
                draw.draw_credits(screen, font, large_font, credits_buttons[0])
            elif globalSettings.current_state == GameState.GAME_MENU:
                # Draw the initial game menu
                draw.draw_game_menu(screen, game_menu_buttons[-1], game_menu_buttons[:-1])
                draw.draw_health_bar(screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
                draw.draw_health_bar(screen, globalSettings.SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
                draw.draw_experience_bar(screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
                draw.draw_turn(screen, game)
            elif globalSettings.current_state == GameState.OPTIONS:
                draw.draw_options_menu(screen, options_buttons[-1], options_buttons[:-1])

            pygame.display.flip()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
