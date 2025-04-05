import random
import pygame
from enum import Enum
from typing import Callable, Dict, List, Tuple
from Types import pokemon_type_chart # Import the pokemon_type_chart

# --- Constants ---
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (150, 0, 0)
RED_COLOR = (255, 0, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
LIME = (0, 255, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 139)
BROWN = (165, 42, 42)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Button dimensions
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70
BUTTON_SPACING = 130

# Font
TURN_FONT_SIZE = 50
FONT_SIZE = 36
LARGE_FONT_SIZE = 72
CONSOLE_FONT_SIZE = 20

# --- Game States ---
class GameState(Enum):
    """Enumeration for different game states."""
    MENU = 0
    CREDITS = 1
    GAME_MENU = 2
    OPTIONS = 3

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
        text_surface = self.font.render(self.text, True, BLACK)
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

# --- Game Class ---
class Game:
    """Manages the game state and logic."""

    def __init__(self):
        self.health = 100
        self.health2 = 100
        self.turn = 1
        self.max_health = 100
        self.harden_active = False
        self.empower_active = False
        self.experience = 0
        self.experience_needed = 100
        self.level = 1
        # New attribute: names
        self.player_name = "Jimmy"
        self.opponent_name = "Opponent"
        #Console log
        self.console_logs: List[str] = []
        self.show_console = False #changed to false
        self.player_type = "Fire"  # Example type
        self.opponent_type = random.choice(list(pokemon_type_chart.keys())) #added to choose a random type
        self.opponent_color = random.choice(pokemon_type_chart[self.opponent_type]["color"]) #added to choose a random color

    def opponent_turn(self):
        """Simulates the opponent's turn."""
        self.add_log(f"{self.opponent_name}'s turn")
        moves = {
            "Kick": lambda: self._apply_damage(5),
            "Heal": lambda: self._heal_opponent(10),
            "Stomp": lambda: self._apply_damage(10),
            "Scratch": lambda: self._apply_damage(20),
        }
        chosen_move = random.choice(list(moves.keys()))
        log = f"{self.opponent_name} used {chosen_move}!"
        self.add_log(log)
        moves[chosen_move]()
        self.end_turn()
        self.show_console = True #added to show the console after the turn

    def _apply_damage(self, damage):
        """Applies damage to the player."""
        damage_multiplier = 0.5 if self.harden_active else 1
        type_multiplier = self.calculate_type_effectiveness(self.opponent_type, self.player_type)
        self.health -= damage * damage_multiplier * type_multiplier
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()

    def add_log(self, log: str):
        self.console_logs.append(log)
        if len(self.console_logs) > 5:  # Reduced to 5 for better fit
            self.console_logs.pop(0)

    def _heal_opponent(self, heal_amount):
        """Heals the opponent."""
        if self.health2 < self.max_health:
            self.health2 += heal_amount
        self.health2 = min(self.health2, self.max_health)  # Ensure health doesn't exceed max
        self.add_log(f"{self.opponent_name} healed itself!")

    def end_turn(self):
        """Ends the current turn and switches to the next."""
        self.add_log("Turn Ended")
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()
        elif self.turn == 1:
            self.turn = 2
            self.opponent_turn()
        elif self.turn == 2:
            self.turn = 1
            self.harden_active = False

    def player_kick(self):
        """Handles the player's kick action."""
        damage_multiplier = 2 if self.empower_active else 1
        type_multiplier = self.calculate_type_effectiveness(self.player_type, self.opponent_type)
        self.health2 -= 25 * damage_multiplier * type_multiplier
        if self.health <= 0 or self.health2 <= 0:
            self.check_win()
        self.end_turn()
        self.empower_active = False

    def player_heal(self):
        """Handles the player's heal action."""
        if self.health < self.max_health:
            self.health += 20
        self.health = min(self.health, self.max_health)
        self.end_turn()

    def player_harden(self):
        """Handles the player's harden action."""
        self.harden_active = True
        self.end_turn()

    def player_empower(self):
        """Handles the player's empower action."""
        self.empower_active = True
        self.end_turn()

    def check_win(self):
        """Checks if the player has won and updates experience."""
        if self.health2 <= 0:
            self.experience += 50  # Increase experience on win
            self.check_level_up()
            self.add_log("You won!")
        else:
            self.add_log("You lost")
        self.reset_game()

    def check_level_up(self):
        """Checks if the player has leveled up."""
        while self.experience >= self.experience_needed:
            self.level += 1
            self.experience -= self.experience_needed
            self.experience_needed += 50  # Increase experience needed for next level
            self.add_log(f"Level Up! You are now level {self.level}!")

    def reset_game(self):
        """Resets the game state."""
        self.health = 100
        self.health2 = 100
        self.turn = 1
        self.harden_active = False
        self.empower_active = False
        self.opponent_type = random.choice(list(pokemon_type_chart.keys())) #added to choose a random type
        self.opponent_color = random.choice(pokemon_type_chart[self.opponent_type]["color"]) #added to choose a random color
        global current_state
        current_state = GameState.MENU

    def calculate_type_effectiveness(self, attacking_type, defending_type):
        """Calculates type effectiveness multiplier."""
        if defending_type in pokemon_type_chart[attacking_type]["weaknesses"]:
            return 2.0  # Super effective
        elif defending_type in pokemon_type_chart[attacking_type]["resistances"]:
            return 0.5  # Not very effective
        elif defending_type in pokemon_type_chart[attacking_type]["immunities"]:
            return 0.0  # No effect
        else:
            return 1.0  # Normal effectiveness

# --- Drawing Functions ---
def draw_turn(screen: pygame.Surface, game: Game):
    """Draws the current turn number on the screen."""
    turn_text = pygame.font.Font(None, TURN_FONT_SIZE).render(f"Turn {game.turn}", True, BLACK)
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - 50, 20))

def draw_health_bar(screen: pygame.Surface, x: int, y: int, width: int, height: int, health: int, max_health: int, name: str, status_effect: str = None):
    """Draws a health bar with optional status effect."""
    if health < 0:
        health = 0

    health_percentage = health / max_health
    health_width = int(width * health_percentage)

    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, GREEN, (x, y, health_width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    pygame.draw.rect(screen, DARK_RED, (x + health_width, y, width - health_width, height))

    name_text = pygame.font.Font(None, FONT_SIZE).render(name, True, BLACK)
    screen.blit(name_text, (x, y + height + 5))

    if status_effect:
        effect_color = BLUE if status_effect == "Harden" else PURPLE
        pygame.draw.rect(screen, effect_color, (x, y - 30, 50, 20))
        effect_text = pygame.font.Font(None, FONT_SIZE).render(status_effect, True, BLACK)
        screen.blit(effect_text, (x, y - 30))

def draw_experience_bar(screen: pygame.Surface, x: int, y: int, width: int, height: int, experience: int, experience_needed: int, level: int):
    """Draws the experience bar."""
    if experience < 0:
        experience = 0
    
    experience_percentage = experience / experience_needed
    experience_width = int(width * experience_percentage)

    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, GOLD, (x, y, experience_width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

    level_text = pygame.font.Font(None, FONT_SIZE).render(f"Level: {level}", True, BLACK)
    screen.blit(level_text, (x, y - 30))

def draw_credits(screen: pygame.Surface, font: pygame.font.Font, large_font: pygame.font.Font, credits_back_button: Button):
    """Draws the credits screen."""
    screen.fill(WHITE)
    credits_text = large_font.render("Credits", True, BLACK)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(credits_text, credits_rect)

    name_text = font.render("Created by: Luken", True, BLACK)
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
    screen.blit(name_text, name_rect)

    credits_back_button.draw(screen)

def draw_game_menu(screen: pygame.Surface, game_menu_back_button: Button, game_buttons: List[Button], game:Game, close_console_button: Button):
    """Draws the game menu screen."""
    bottom_third_height = SCREEN_HEIGHT // 3
    pygame.draw.rect(screen, LIGHT_GRAY, (0, SCREEN_HEIGHT - bottom_third_height, SCREEN_WIDTH, bottom_third_height))

    game_menu_text = pygame.font.Font(None, LARGE_FONT_SIZE).render("Game Menu", True, BLACK)
    game_menu_rect = game_menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(game_menu_text, game_menu_rect)

    circle_radius = 100
    pygame.draw.circle(screen, BLUE, (circle_radius + 150, SCREEN_HEIGHT - circle_radius - 300), circle_radius)
    pygame.draw.circle(screen, game.opponent_color, (SCREEN_WIDTH - circle_radius - 150, circle_radius + 250), circle_radius) #changed the color to the opponent color

    game_menu_back_button.draw(screen)

    for button in game_buttons:
        button.draw(screen)
    if game.show_console:
        draw_console(screen, game, pygame.font.Font(None, CONSOLE_FONT_SIZE), close_console_button)

def draw_options_menu(screen: pygame.Surface, options_back_button: Button, options_buttons: List[Button]):
    """Draws the options menu screen."""
    screen.fill(WHITE)
    options_text = pygame.font.Font(None, LARGE_FONT_SIZE).render("Options", True, BLACK)
    options_rect = options_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(options_text, options_rect)

    options_back_button.draw(screen)

    for button in options_buttons:
        button.draw(screen)

def draw_console(screen: pygame.Surface, game: Game, font: pygame.font.Font, close_button: Button):
    """Draws the console log on the screen."""
    console_rect = pygame.Rect(10, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 20, 190)
    pygame.draw.rect(screen, LIGHT_GRAY, console_rect)
    pygame.draw.rect(screen, BLACK, console_rect, 2)

    y_offset = console_rect.y + 10
    for log in reversed(game.console_logs):
        log_text = font.render(log, True, RED)
        screen.blit(log_text, (console_rect.x + 10, y_offset))
        y_offset += font.get_linesize()
        if y_offset > console_rect.bottom - 10:
            break
    close_button.draw(screen)

# --- Button Actions ---
def start_game(game: Game):
    """Starts the game."""
    global current_state
    current_state = GameState.GAME_MENU

def open_options():
    """Opens the options menu."""
    global current_state
    current_state = GameState.OPTIONS

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
    current_state = GameState.MENU
    game.reset_game()

def close_console(game: Game):
    """Closes the console log."""
    game.show_console = False

# --- Menu Configuration ---
def create_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the main menu buttons."""
    button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    button_y_start = 250
    return [
        Button(button_x, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT, "Fight!!", GREEN, GRAY, font, start_game, game),
        Button(button_x, button_y_start + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Options", YELLOW, GRAY, font, open_options),
        Button(button_x, button_y_start + 2 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Credits", LIGHT_BLUE, GRAY, font, open_credits),
        Button(button_x, button_y_start + 3 * BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Exit", RED, GRAY, font, exit_action),
        Button(20, 20, 100, 40, "test", LIGHT_BLUE, GRAY, font, test_print, "hello")
    ]

def create_credits_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the credits buttons."""
    return [
        Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, font, back_to_menu, game)
    ]

def create_game_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the game menu buttons."""
    game_button_width = SCREEN_WIDTH // 2
    game_button_height = SCREEN_HEIGHT // 6
    game_button_y = SCREEN_HEIGHT - SCREEN_HEIGHT // 3
    return [
        Button(0, game_button_y, game_button_width, game_button_height, "Kick", LIGHT_BLUE, GRAY, font, game.player_kick),
        Button(0, game_button_y + game_button_height, game_button_width, game_button_height, "Heal", LIGHT_BLUE, GRAY, font, game.player_heal),
        Button(game_button_width, game_button_y, game_button_width, game_button_height, "Harden", LIGHT_BLUE, GRAY, font, game.player_harden),
        Button(game_button_width, game_button_y + game_button_height, game_button_width, game_button_height, "Empower", LIGHT_BLUE, GRAY, font, game.player_empower),
        Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, font, back_to_menu, game)
    ]

def create_options_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the options menu buttons."""
    button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    button_y_start = 250
    return [
        Button(button_x, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT, "Option 1", GREEN, GRAY, font, test_print, "Option 1"),
        Button(button_x, button_y_start + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT, "Option 2", YELLOW, GRAY, font, test_print, "Option 2"),
        Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, font, back_to_menu, game)
    ]

# --- Main Game Loop ---
def main():
    """Main game loop."""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Pokemii Menu")

    # Fonts
    font = pygame.font.Font(None, FONT_SIZE)
    large_font = pygame.font.Font(None, LARGE_FONT_SIZE)
    console_font = pygame.font.Font(None, CONSOLE_FONT_SIZE)

    # Game instance
    game = Game()

    # --- Button Creation ---
    menu_buttons = create_menu_buttons(font, game)
    credits_buttons = create_credits_buttons(font, game)
    game_menu_buttons = create_game_menu_buttons(font, game)
    options_buttons = create_options_buttons(font, game)
    close_console_button = Button(SCREEN_WIDTH - 30, SCREEN_HEIGHT - 200, 20, 20, "X", RED, DARK_RED, console_font, close_console, game) #added the close console button

    global current_state
    current_state = GameState.MENU

    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if current_state == GameState.MENU:
                    for button in menu_buttons:
                        button.handle_event(event)
                elif current_state == GameState.CREDITS:
                    for button in credits_buttons:
                        button.handle_event(event)
                elif current_state == GameState.GAME_MENU:
                    for button in game_menu_buttons:
                        button.handle_event(event)
                    if game.show_console:
                        close_console_button.handle_event(event)
                elif current_state == GameState.OPTIONS:
                    for button in options_buttons:
                        button.handle_event(event)

            screen.fill(WHITE)

            if current_state == GameState.MENU:
                for button in menu_buttons:
                    button.draw(screen)
            elif current_state == GameState.CREDITS:
                draw_credits(screen, font, large_font, credits_buttons[0])
            elif current_state == GameState.GAME_MENU:
                # Draw everything else first
                draw_game_menu(screen, game_menu_buttons[-1], game_menu_buttons[:-1], game, close_console_button)
                draw_health_bar(screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
                draw_health_bar(screen, SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
                draw_experience_bar(screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
                draw_turn(screen, game)
                game.show_console = False #added to hide the console after the turn
            elif current_state == GameState.OPTIONS:
                draw_options_menu(screen, options_buttons[-1], options_buttons[:-1])

            pygame.display.flip()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
