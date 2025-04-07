import pygame
import globalSettings
from game import Game, GameState
import draw
import buttons
from cursor import specialCursor

def run_game():
    """Runs the game logic after menu transition."""
    game = Game()

    game_menu_buttons = buttons.create_game_menu_buttons(globalSettings.font, game)

    globalSettings.current_state = GameState.GAME_MENU

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globalSettings.current_state = GameState.MENU
                return  # Return to the main menu

            if globalSettings.current_state == GameState.GAME_MENU:
                for button in game_menu_buttons:
                    button.handle_event(event)

        globalSettings.screen.fill(globalSettings.WHITE)

        if globalSettings.current_state == GameState.GAME_MENU:
            draw.draw_game_menu(globalSettings.screen, game_menu_buttons[-1], game_menu_buttons[:-1])
            draw.draw_health_bar(globalSettings.screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
            draw.draw_health_bar(globalSettings.screen, globalSettings.SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
            draw.draw_experience_bar(globalSettings.screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
            draw.draw_turn(globalSettings.screen, game)
        elif globalSettings.current_state == GameState.MENU:
            return
        specialCursor(globalSettings.screen, globalSettings.images["cursor.png"])
        
        pygame.display.flip()
        clock.tick(60)

    # Optional fallback in case loop exits normally
    globalSettings.current_state = GameState.MENU