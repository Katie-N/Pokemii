import pygame
import globalSettings
from game import Game, GameState
import draw
import buttons

# Add this function to menu5_optimize.py
def run_game():
    """Runs the game logic after menu transition."""
    screen = pygame.display.set_mode(globalSettings.SCREEN_SIZE)
    pygame.display.set_caption("Pokemii Game")

    font = pygame.font.Font(None, globalSettings.FONT_SIZE)
    large_font = pygame.font.Font(None, globalSettings.LARGE_FONT_SIZE)

    game = Game()

    game_menu_buttons = buttons.create_game_menu_buttons(font, game)

    globalSettings.current_state = GameState.GAME_MENU

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Exit to main menu
            if globalSettings.current_state == GameState.GAME_MENU:
                for button in game_menu_buttons:
                    button.handle_event(event)

        screen.fill(globalSettings.WHITE)
        if globalSettings.current_state == GameState.GAME_MENU:
            draw.draw_game_menu(screen, game_menu_buttons[-1], game_menu_buttons[:-1])
            draw.draw_health_bar(screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
            draw.draw_health_bar(screen, globalSettings.SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
            draw.draw_experience_bar(screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
            draw.draw_turn(screen, game)
        
        pygame.display.flip()
        clock.tick(60)

