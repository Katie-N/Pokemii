from enum import Enum
from game import Game
from constants import *

class GameState(Enum):
    """Enumeration for different game states."""
    MAIN_MENU = 0
    OPTIONS_MENU = 1
    CREDITS = 2
    GAME_MENU = 3

current_state = GameState.MAIN_MENU

def start_game(game: Game):
    """Starts the game."""
    global current_state
    current_state = GameState.GAME_MENU

def open_options():
    """Opens the options menu."""
    global current_state
    current_state = GameState.OPTIONS_MENU

def open_credits():
    """Opens the credits screen."""
    global current_state
    current_state = GameState.CREDITS

def exit_action():
    """Exits the game."""
    print("Exiting game.")
    pygame.quit()
    exit()

def test_print(message: str):
    """Prints a test message."""
    print(message)

def back_to_menu(game: Game):
    """Returns to the main menu."""
    global current_state
    current_state = GameState.MAIN_MENU
    game.reset_game()

def close_console(game: Game):
    """Closes the console log."""
    game.show_console = False

def open_game_menu():
     """Opens the game menu."""
     global current_state
     current_state = GameState.GAME_MENU
