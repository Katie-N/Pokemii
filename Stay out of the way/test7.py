import pygame
import os
import random
from enum import Enum
from typing import Callable, Dict, List, Tuple
from Types import pokemon_type_chart  # Import the pokemon_type_chart
pygame.init()

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
infoObject = pygame.display.Info()
MAX_WIDTH = infoObject.current_w
MAX_HEIGHT = infoObject.current_h

if MAX_WIDTH / MAX_HEIGHT >= 16 / 9:
    SCREEN_HEIGHT = MAX_HEIGHT
    SCREEN_WIDTH = int(SCREEN_HEIGHT * 16 / 9)
else:
    SCREEN_WIDTH = MAX_WIDTH
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 9 / 16)

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Button dimensions
MAIN_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.286458)
MAIN_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 0.1398148)
NAV_BUTTON_WIDTH = int(SCREEN_WIDTH * 0.0322916)
NAV_BUTTON_HEIGHT = int(SCREEN_HEIGHT * 0.084259)
BUTTON_SPACING = int(SCREEN_HEIGHT * 0.13)

# Font
TURN_FONT_SIZE = int(SCREEN_HEIGHT * 0.05555)
FONT_SIZE = int(SCREEN_HEIGHT * 0.04)
LARGE_FONT_SIZE = int(SCREEN_HEIGHT * 0.08)
CONSOLE_FONT_SIZE = int(SCREEN_HEIGHT * 0.02222)

# --- Game States ---
class GameState(Enum):
    """Enumeration for different game states."""
    MAIN_MENU = 0
    OPTIONS_MENU = 1
    CREDITS = 2
    GAME_MENU = 3

current_state = GameState.MAIN_MENU

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
        current_state = GameState.MAIN_MENU

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

# --- Menu Configuration ---
def create_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the main menu buttons."""
    button_x = (SCREEN_WIDTH - MAIN_BUTTON_WIDTH) // 2
    button_y_start = int(SCREEN_HEIGHT * 0.27777)
    return [
        Button(button_x, button_y_start, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Fight!!", GREEN, GRAY, font, start_game, game),
        Button(button_x, button_y_start + BUTTON_SPACING, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Options", YELLOW, GRAY, font, open_options),
        Button(button_x, button_y_start + 2 * BUTTON_SPACING, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Credits", LIGHT_BLUE, GRAY, font, open_credits),
        Button(button_x, button_y_start + 3 * BUTTON_SPACING, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Exit", RED, GRAY, font, exit_action),
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
    button_x = (SCREEN_WIDTH - MAIN_BUTTON_WIDTH) // 2
    button_y_start = 250
    return [
        Button(button_x, button_y_start, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Option 1", GREEN, GRAY, font, test_print, "Option 1"),
        Button(button_x, button_y_start + BUTTON_SPACING, MAIN_BUTTON_WIDTH, MAIN_BUTTON_HEIGHT, "Option 2", YELLOW, GRAY, font, test_print, "Option 2"),
        Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, font, back_to_menu, game)
    ]

# --- Main Menu Functions (From mainMenu.py) ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_button(text, x, y, width, height, text_color, surface):
    """Creates a transparent button and returns its rectangle."""
    button_rect = pygame.Rect(x, y, width, height)
    # Create a transparent surface for the button
    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Draw a semi-transparent rectangle (optional, for a subtle button effect)
    pygame.draw.rect(button_surface, (0, 0, 0, 0), (0, 0, width, height))  # Last value is alpha (0-255)
    surface.blit(button_surface, (x,y))
    font = pygame.font.Font(None, 36)
    draw_text(text, font, text_color, surface, x + 10, y + 10)
    return button_rect

def load_images(assets_path):
    """Loads and scales background images."""
    try:
        pic1_path = os.path.join(assets_path, "MiiChannel.png")
        pic2_path = os.path.join(assets_path, "fightMenu.png")

        if os.path.exists(pic1_path):
            pic1 = pygame.image.load(pic1_path).convert()
            pic1 = pygame.transform.scale(pic1, SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic1_path}")

        if os.path.exists(pic2_path):
            pic2 = pygame.image.load(pic2_path).convert()
            pic2 = pygame.transform.scale(pic2, SCREEN_SIZE)
        else:
            raise FileNotFoundError(f"Image file not found: {pic2_path}")

        return pic1, pic2

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return None, None

def calculate_button_positions():
    """Calculates button positions relative to the screen."""
    button_y = int(SCREEN_HEIGHT * 0.77222)
    left_button_x = int(SCREEN_WIDTH * 0.1916)
    right_button_x = int(SCREEN_WIDTH * 0.52083)
    next_button_x = int(SCREEN_WIDTH * 0.9333)
    next_button_y = int(SCREEN_HEIGHT * 0.347222)
    back_button_x = int(SCREEN_WIDTH * 0.033333)

    return (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
    )

def handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed):
    """Handles the menu sliding logic."""
    if second_menu_visible:
        menu_offset -= menu_slide_speed
        if menu_offset <= -SCREEN_WIDTH:
            menu_offset = -SCREEN_WIDTH
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
    game: Game
):
    """Handles events in the main menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, False, second_menu_visible
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if train_button.collidepoint(mouse_pos):
                print("Train button clicked!")
            if compete_button.collidepoint(mouse_pos):
                print("Compete button clicked!")
                start_game(game)
                return False, False, second_menu_visible
            if next_button.collidepoint(mouse_pos):
                return False, False, True
            if importMii_button.collidepoint(mouse_pos):
                print("Import Mii button clicked!")
            if tradeMii_button.collidepoint(mouse_pos):
                print("Trade Mii button clicked!")
            if back_button.collidepoint(mouse_pos):
                return False, True, False
    return False, False, second_menu_visible

def draw_main_menu(screen, pic1, menu_offset, title_font, button_positions):
    """Draws the main menu."""
    first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    first_menu_surface.blit(pic1, (0, 0))
    draw_text("My Game", title_font, WHITE, first_menu_surface, SCREEN_WIDTH // 2 - 80, 50)

    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        _,
    ) = button_positions

    train_button = create_button(
        "Train",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        first_menu_surface,
    )
    compete_button = create_button(
        "Compete",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        first_menu_surface,
    )
    next_button = create_button(
        ">",
        next_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        WHITE,
        first_menu_surface,
    )

    screen.blit(first_menu_surface, (menu_offset, 0))
    return train_button, compete_button, next_button

def draw_second_menu(screen, pic2, menu_offset, title_font, button_positions):
    """Draws the second menu."""
    second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
    second_menu_surface.blit(pic2, (0, 0))
    draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2 - 80, 50)

    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
    ) = button_positions

    importMii_button = create_button(
        "Import Mii",
        left_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )
    tradeMii_button = create_button(
        "Trade Mii",
        right_button_x,
        button_y,
        MAIN_BUTTON_WIDTH,
        MAIN_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )
    back_button = create_button(
        "<",
        back_button_x,
        next_button_y,
        NAV_BUTTON_WIDTH,
        NAV_BUTTON_HEIGHT,
        WHITE,
        second_menu_surface,
    )

    screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
    return importMii_button, tradeMii_button, back_button

def main_menu(game: Game):
    """Displays the main menu."""
    global current_state
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Load images
    assets_path = os.path.join(".", "assets", "menus")
    pic1, pic2 = load_images(assets_path)
    if pic1 is None or pic2 is None:
        return False

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Calculate button positions
    button_positions = calculate_button_positions()

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 20
    second_menu_visible = False

    running = True
    while running:
        # Handle events
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)
        importMii_button, tradeMii_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)
        
        quit_game, back_to_main, second_menu_visible = handle_events(train_button, compete_button, next_button, importMii_button, tradeMii_button, back_button, second_menu_visible, game)
        if quit_game:
            return False
        if back_to_main:
            second_menu_visible = False
            current_state = GameState.MAIN_MENU

        # --- Menu Sliding Logic ---
        menu_offset = handle_menu_sliding(second_menu_visible, menu_offset, menu_slide_speed)

        # Draw everything
        screen.fill(BLACK)

        # Draw Main Menu
        train_button, compete_button, next_button = draw_main_menu(screen, pic1, menu_offset, title_font, button_positions)

        # Draw Second Menu
        if second_menu_visible or menu_offset > -SCREEN_WIDTH:
            importMii_button, tradeMii_button, back_button = draw_second_menu(screen, pic2, menu_offset, title_font, button_positions)

        pygame.display.flip()
        if current_state != GameState.MAIN_MENU:
            running = False
    return True

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
    menu_buttons = create_menu_buttons(font, game)
    credits_buttons = create_credits_buttons(font, game)
    game_menu_buttons = create_game_
