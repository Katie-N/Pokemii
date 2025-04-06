import pygame
import globalSettings
from game import Game, GameState
from typing import Callable, Dict, List, Tuple

# --- Button Class ---
class Button:
    """Represents a clickable button."""
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int], hover_color: Tuple[int, int, int], font: pygame.font.Font, action: Callable = None, arg=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False
        self.arg = arg
        self.font = font

    def draw(self, screen: pygame.Surface):
        """Draws the button on the screen."""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, globalSettings.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event):
        """Handles mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    if self.arg is not None:
                        self.action(self.arg)
                    else:
                        self.action()

    def __repr__(self):
        return f"Button({self.text}, {self.rect.x}, {self.rect.y})"

# --- Button Actions ---
def start_game(game: Game):
    """Starts the game."""
    globalSettings.current_state = GameState.GAME_MENU

def open_options():
    """Opens the options menu."""
    globalSettings.current_state = GameState.OPTIONS

def open_credits():
    """Opens the credits screen."""
    globalSettings.current_state = GameState.CREDITS

def exit_action():
    """Exits the game."""
    print("Exiting game.")
    pygame.quit()
    exit()

# def test_print(message: str):
#     """Prints a test message."""
#     print(message)

def back_to_menu(game: Game):
    """Returns to the main menu."""
    
    globalSettings.current_state = GameState.MENU
    game.reset_game()

# --- Menu Configuration ---
# def create_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
#     """Creates the main menu buttons."""
#     button_x = (globalSettings.SCREEN_WIDTH - globalSettings.BUTTON_WIDTH) // 2
#     button_y_start = 250
#     return [
#         Button(button_x, button_y_start, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Fight!!", globalSettings.GREEN, globalSettings.GRAY, font, start_game, game),
#         Button(button_x, button_y_start + globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Options", globalSettings.YELLOW, globalSettings.GRAY, font, open_options),
#         Button(button_x, button_y_start + 2 * globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Credits", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, open_credits),
#         Button(button_x, button_y_start + 3 * globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Exit", globalSettings.RED, globalSettings.GRAY, font, exit_action),
#         Button(20, 20, 100, 40, "test", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, test_print, "hello")
#     ]

# def create_credits_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
#     """Creates the credits buttons."""
#     return [
#         Button(20, 20, 150, 50, "Back to Menu", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, back_to_menu, game)
#     ]

def create_game_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the game menu buttons."""
    game_button_width = globalSettings.SCREEN_WIDTH // 2
    game_button_height = globalSettings.SCREEN_HEIGHT // 6
    game_button_y = globalSettings.SCREEN_HEIGHT - globalSettings.SCREEN_HEIGHT // 3
    return [
        Button(0, game_button_y, game_button_width, game_button_height, "Kick", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, game.player_kick),
        Button(0, game_button_y + game_button_height, game_button_width, game_button_height, "Heal", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, game.player_heal),
        Button(game_button_width, game_button_y, game_button_width, game_button_height, "Harden", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, game.player_harden),
        Button(game_button_width, game_button_y + game_button_height, game_button_width, game_button_height, "Empower", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, game.player_empower),
        Button(20, 20, 150, 50, "Back to Menu", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, back_to_menu, game)
    ]

# def create_options_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
#     """Creates the options menu buttons."""
#     button_x = (globalSettings.SCREEN_WIDTH - globalSettings.BUTTON_WIDTH) // 2
#     button_y_start = 250
#     return [
#         Button(button_x, button_y_start, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Option 1", globalSettings.GREEN, globalSettings.GRAY, font, test_print, "Option 1"),
#         Button(button_x, button_y_start + globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Option 2", globalSettings.YELLOW, globalSettings.GRAY, font, test_print, "Option 2"),
#         Button(20, 20, 150, 50, "Back to Menu", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, back_to_menu, game)
#     ]