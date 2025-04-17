import pygame
import globalSettings
from game import Game, GameState
import draw
import buttons
from cursor import specialCursor
import load_assets

def run_game():
    """Runs the game logic after menu transition."""
    game = Game()
    if not globalSettings.fightScreenAssetsLoaded:
        print("Loading fight screen assets...")
        load_assets.load_fight_screen_assets()

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
        
        # Update the next frame each run
        globalSettings.animators["player"].update()
        globalSettings.animators["opponent"].update()

        globalSettings.screen.fill(globalSettings.WHITE)
        draw.draw_background(globalSettings.screen, globalSettings.images["blurryWuhu"])
        draw.draw_game_HUD(game)
        draw.draw_game_menu(globalSettings.screen, game_menu_buttons[-1], game_menu_buttons[:-1])
        draw.draw_turn(globalSettings.screen, game)
        draw.draw_players(globalSettings.screen)
        
        specialCursor(globalSettings.screen, globalSettings.images["cursor"])
        
        pygame.display.flip()
        clock.tick(60)
        if globalSettings.current_state == GameState.MENU:
            return

    # Optional fallback in case loop exits normally
    globalSettings.current_state = GameState.MENU