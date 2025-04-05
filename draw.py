import globalSettings
from game import Game
from buttons import Button
import pygame
from typing import List

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
