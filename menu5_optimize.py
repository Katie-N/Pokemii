import globalSettings

import random
import pygame
from enum import Enum
from typing import Callable, Dict, List, Tuple

from game import Game, GameState

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

# --- Drawing Functions ---
def draw_turn(screen: pygame.Surface, game: Game):
    """Draws the current turn number on the screen."""
    turn_text = pygame.font.Font(None, globalSettings.TURN_FONT_SIZE).render(f"Turn {game.turn}", True, globalSettings.BLACK)
    screen.blit(turn_text, (globalSettings.SCREEN_WIDTH // 2 - 50, 20))

def draw_health_bar(screen: pygame.Surface, x: int, y: int, width: int, height: int, health: int, max_health: int, name: str, status_effect: str = None):
    """Draws a health bar with optional status effect."""
    if health < 0:
        health = 0

    health_percentage = health / max_health
    health_width = int(width * health_percentage)

    pygame.draw.rect(screen, globalSettings.GRAY, (x, y, width, height))
    pygame.draw.rect(screen, globalSettings.GREEN, (x, y, health_width, height))
    pygame.draw.rect(screen, globalSettings.BLACK, (x, y, width, height), 2)
    pygame.draw.rect(screen, globalSettings.DARK_RED, (x + health_width, y, width - health_width, height))

    name_text = pygame.font.Font(None, globalSettings.FONT_SIZE).render(name, True, globalSettings.BLACK)
    screen.blit(name_text, (x, y + height + 5))

    if status_effect:
        effect_color = globalSettings.BLUE if status_effect == "Harden" else globalSettings.PURPLE
        pygame.draw.rect(screen, effect_color, (x, y - 30, 50, 20))
        effect_text = pygame.font.Font(None, globalSettings.FONT_SIZE).render(status_effect, True, globalSettings.BLACK)
        screen.blit(effect_text, (x, y - 30))

def draw_experience_bar(screen: pygame.Surface, x: int, y: int, width: int, height: int, experience: int, experience_needed: int, level: int):
    """Draws the experience bar."""
    if experience < 0:
        experience = 0
    
    experience_percentage = experience / experience_needed
    experience_width = int(width * experience_percentage)

    pygame.draw.rect(screen, globalSettings.GRAY, (x, y, width, height))
    pygame.draw.rect(screen, globalSettings.GOLD, (x, y, experience_width, height))
    pygame.draw.rect(screen, globalSettings.BLACK, (x, y, width, height), 2)

    level_text = pygame.font.Font(None, globalSettings.FONT_SIZE).render(f"Level: {level}", True, globalSettings.BLACK)
    screen.blit(level_text, (x, y - 30))

def draw_credits(screen: pygame.Surface, font: pygame.font.Font, large_font: pygame.font.Font, credits_back_button: Button):
    """Draws the credits screen."""
    screen.fill(globalSettings.WHITE)
    credits_text = large_font.render("Credits", True, globalSettings.BLACK)
    credits_rect = credits_text.get_rect(center=(globalSettings.SCREEN_WIDTH // 2, 100))
    screen.blit(credits_text, credits_rect)

    name_text = font.render("Created by: Luken", True, globalSettings.BLACK)
    name_rect = name_text.get_rect(center=(globalSettings.SCREEN_WIDTH // 2, 250))
    screen.blit(name_text, name_rect)

    credits_back_button.draw(screen)

def draw_game_menu(screen: pygame.Surface, game_menu_back_button: Button, game_buttons: List[Button]):
    """Draws the game menu screen."""
    bottom_third_height = globalSettings.SCREEN_HEIGHT // 3
    pygame.draw.rect(screen, globalSettings.LIGHT_GRAY, (0, globalSettings.SCREEN_HEIGHT - bottom_third_height, globalSettings.SCREEN_WIDTH, bottom_third_height))

    game_menu_text = pygame.font.Font(None, globalSettings.LARGE_FONT_SIZE).render("Game Menu", True, globalSettings.BLACK)
    game_menu_rect = game_menu_text.get_rect(center=(globalSettings.SCREEN_WIDTH // 2, 100))
    screen.blit(game_menu_text, game_menu_rect)

    circle_radius = 100
    pygame.draw.circle(screen, globalSettings.BLUE, (circle_radius + 150, globalSettings.SCREEN_HEIGHT - circle_radius - 300), circle_radius)
    pygame.draw.circle(screen, globalSettings.RED_COLOR, (globalSettings.SCREEN_WIDTH - circle_radius - 150, circle_radius + 250), circle_radius)

    game_menu_back_button.draw(screen)

    for button in game_buttons:
        button.draw(screen)

def draw_options_menu(screen: pygame.Surface, options_back_button: Button, options_buttons: List[Button]):
    """Draws the options menu screen."""
    screen.fill(globalSettings.WHITE)
    options_text = pygame.font.Font(None, globalSettings.LARGE_FONT_SIZE).render("Options", True, globalSettings.BLACK)
    options_rect = options_text.get_rect(center=(globalSettings.SCREEN_WIDTH // 2, 100))
    screen.blit(options_text, options_rect)

    options_back_button.draw(screen)

    for button in options_buttons:
        button.draw(screen)

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

def test_print(message: str):
    """Prints a test message."""
    print(message)

def back_to_menu(game: Game):
    """Returns to the main menu."""
    
    globalSettings.current_state = GameState.MENU
    game.reset_game()

# --- Menu Configuration ---
def create_menu_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the main menu buttons."""
    button_x = (globalSettings.SCREEN_WIDTH - globalSettings.BUTTON_WIDTH) // 2
    button_y_start = 250
    return [
        Button(button_x, button_y_start, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Fight!!", globalSettings.GREEN, globalSettings.GRAY, font, start_game, game),
        Button(button_x, button_y_start + globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Options", globalSettings.YELLOW, globalSettings.GRAY, font, open_options),
        Button(button_x, button_y_start + 2 * globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Credits", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, open_credits),
        Button(button_x, button_y_start + 3 * globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Exit", globalSettings.RED, globalSettings.GRAY, font, exit_action),
        Button(20, 20, 100, 40, "test", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, test_print, "hello")
    ]

def create_credits_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the credits buttons."""
    return [
        Button(20, 20, 150, 50, "Back to Menu", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, back_to_menu, game)
    ]

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

def create_options_buttons(font: pygame.font.Font, game: Game) -> List[Button]:
    """Creates the options menu buttons."""
    button_x = (globalSettings.SCREEN_WIDTH - globalSettings.BUTTON_WIDTH) // 2
    button_y_start = 250
    return [
        Button(button_x, button_y_start, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Option 1", globalSettings.GREEN, globalSettings.GRAY, font, test_print, "Option 1"),
        Button(button_x, button_y_start + globalSettings.BUTTON_SPACING, globalSettings.BUTTON_WIDTH, globalSettings.BUTTON_HEIGHT, "Option 2", globalSettings.YELLOW, globalSettings.GRAY, font, test_print, "Option 2"),
        Button(20, 20, 150, 50, "Back to Menu", globalSettings.LIGHT_BLUE, globalSettings.GRAY, font, back_to_menu, game)
    ]

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
    menu_buttons = create_menu_buttons(font, game)
    credits_buttons = create_credits_buttons(font, game)
    game_menu_buttons = create_game_menu_buttons(font, game)
    options_buttons = create_options_buttons(font, game)

    
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
                draw_credits(screen, font, large_font, credits_buttons[0])
            elif globalSettings.current_state == GameState.GAME_MENU:
                draw_game_menu(screen, game_menu_buttons[-1], game_menu_buttons[:-1])
                draw_health_bar(screen, 20, 100, 200, 20, game.health, game.max_health, "Jimmy", "Harden" if game.harden_active else None)
                draw_health_bar(screen, globalSettings.SCREEN_WIDTH - 220, 100, 200, 20, game.health2, game.max_health, "Opponent")
                draw_experience_bar(screen, 20, 150, 200, 10, game.experience, game.experience_needed, game.level)
                draw_turn(screen, game)
            elif globalSettings.current_state == GameState.OPTIONS:
                draw_options_menu(screen, options_buttons[-1], options_buttons[:-1])

            pygame.display.flip()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
