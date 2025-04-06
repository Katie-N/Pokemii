import globalSettings
from game import Game
from buttons import Button
import pygame
from typing import List
import buttonsFromRect

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

# From mainMenu.py
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

    
# DRAW MII CHANNEL MENU
def draw_main_menu(screen, images, menu_offset, title_font, button_positions):
    """Draws the main menu."""
    first_menu_surface = pygame.Surface(globalSettings.SCREEN_SIZE, pygame.SRCALPHA)
    first_menu_surface.blit(images["mii_channel"], (0, 0))
    (
        button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
        pick_save_x,
        pick_save_y,
    ) = button_positions

    def import_mii_action():
        print("Importing Mii...")

    def trade_mii_action():
        print("Trading Mii...")

    importMii_button = buttonsFromRect.create_button(
        "",
        left_button_x,
        button_y,
        globalSettings.MAIN_BUTTON_WIDTH,
        globalSettings.MAIN_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        first_menu_surface,
        import_mii_action
    )
    tradeMii_button = buttonsFromRect.create_button(
        "",
        right_button_x,
        button_y,
        globalSettings.MAIN_BUTTON_WIDTH,
        globalSettings.MAIN_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        first_menu_surface,
        trade_mii_action
    )
    next_button = buttonsFromRect.create_button(
        "",
        next_button_x,
        next_button_y,
        globalSettings.NAV_BUTTON_WIDTH,
        globalSettings.NAV_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        first_menu_surface,
    )

    screen.blit(first_menu_surface, (menu_offset, 0))
    return importMii_button, tradeMii_button, next_button

# DRAW TRAINING MENU

def draw_second_menu(screen, images, menu_offset, title_font, button_positions):
    """Draws the second menu."""
    second_menu_surface = pygame.Surface(globalSettings.SCREEN_SIZE, pygame.SRCALPHA)
    second_menu_surface.blit(images["fight_menu"], (0, 0))
    (   button_y,
        left_button_x,
        right_button_x,
        next_button_x,
        next_button_y,
        back_button_x,
        pick_save_x,
        pick_save_y,
    ) = button_positions

    def train_action():
        print("Training...")

    def compete_action():
        print("Competing...")

    train_button = buttonsFromRect.create_button(
        "",
        left_button_x,
        button_y,
        globalSettings.MAIN_BUTTON_WIDTH,
        globalSettings.MAIN_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        second_menu_surface,
        train_action
    )
    compete_button = buttonsFromRect.create_button(
        "",
        right_button_x,
        button_y,
        globalSettings.MAIN_BUTTON_WIDTH,
        globalSettings.MAIN_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        second_menu_surface,
        compete_action
    )
    back_button = buttonsFromRect.create_button(
        "",
        back_button_x,
        next_button_y,
        globalSettings.NAV_BUTTON_WIDTH,
        globalSettings.NAV_BUTTON_HEIGHT,
        globalSettings.BUTTON_TEXT_COLOR,
        second_menu_surface,
    )

    screen.blit(second_menu_surface, (menu_offset + globalSettings.SCREEN_WIDTH, 0))
    return train_button, compete_button, back_button

def draw_save_menu(screen, save_menu_buttons):
    """Draws the save options menu."""
    save_menu_surface = pygame.Surface(globalSettings.SCREEN_SIZE, pygame.SRCALPHA)
    save_menu_surface.fill((100,100,100, 150))
    for button in save_menu_buttons:
        # Calculate the button's position
        button_x = globalSettings.SCREEN_WIDTH // 2 - globalSettings.SAVE_MENU_BUTTON_WIDTH // 2
        button_y = globalSettings.SCREEN_HEIGHT // 2 - (len(save_menu_buttons) * globalSettings.SAVE_MENU_BUTTON_SPACING) // 2 + (save_menu_buttons.index(button) * globalSettings.SAVE_MENU_BUTTON_SPACING)
        
        # Update the button's rectangle
        button[0].x = button_x
        button[0].y = button_y
        button[0].width = globalSettings.SAVE_MENU_BUTTON_WIDTH
        button[0].height = globalSettings.SAVE_MENU_BUTTON_HEIGHT
        button[0].topleft = (button_x, button_y)
        
        # Draw the button
        pygame.draw.rect(save_menu_surface, (200,200,200), button[0])
        
        # Draw the text
        draw_text(button[2], pygame.font.Font(None, 36), globalSettings.BLACK, save_menu_surface, button_x + 10, button_y + 10)
    screen.blit(save_menu_surface, (0,0))
