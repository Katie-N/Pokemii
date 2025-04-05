import pygame
import os
import random

# Initialize Pygame
pygame.init()

# --- Constants ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_RED = (150, 0, 0)
RED_COLOR = (255, 0, 0)

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
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = BLUE
BUTTON_TEXT_COLOR = WHITE

# --- Fonts ---
TURN_FONT = pygame.font.Font(None, 50)
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# --- Game Variables ---
health = 100
health2 = 100
turn = 1

# --- Game States ---
class GameState:
    MAIN_MENU = 0
    OPTIONS_MENU = 1
    CREDITS = 2
    GAME_MENU = 3

current_state = GameState.MAIN_MENU

# --- Button Class ---
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None, arg=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.hovered = False
        self.arg = arg

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    if self.arg is not None:
                        self.action(self.arg)
                    else:
                        self.action()

# --- Functions ---
def draw_text(text, font, color, surface, x, y):
    """Draws text on the screen."""
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def create_button(text, x, y, width, height, color, text_color, surface):
    """Creates a button and returns its rectangle."""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, color, button_rect)
    font = pygame.font.Font(None, 36)
    draw_text(text, font, text_color, surface, x + 10, y + 10)
    return button_rect

# --- Game Functions ---
def opponent_turn():
    global health, health2, turn
    moves = ["Kick", "Heal", "Stomp", "Scratch"]
    chosen_move = random.choice(moves)
    print(f"Opponent used {chosen_move}!")

    if chosen_move == "Kick":
        health -= 5
        print("Opponent kicked Jimmy!")
    elif chosen_move == "Heal":
        max_health = 100
        if health2 < max_health:
            health2 += 10
        print("Opponent healed itself!")
    elif chosen_move == "Stomp":
        health -= 10
        print("Opponent stomped Jimmy!")
    elif chosen_move == "Scratch":
        health -= 20
        print("Opponent scratched Jimmy!")
    end_turn()

def end_turn():
    global turn, health, health2
    print("Turn Ended")
    if turn == 1:
        turn = 2
        opponent_turn()
    elif turn == 2:
        turn = 1

def draw_turn(screen, turn):
    turn_text = TURN_FONT.render(f"Turn {turn}", True, BLACK)
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - 50, 20))

def draw_health_bar(screen, x, y, width, height, health):
    #health_bar variables
    max_health = 100
    if health < 0:
        health = 0

    # Calculate health bar
    health_percentage = health / max_health

    # Draw the background
    pygame.draw.rect(screen, GRAY, (x, y, width, height))

    # Draw the health portion
    health_width = int(width * health_percentage)
    pygame.draw.rect(screen, GREEN, (x, y, health_width, height))

    # Draw the border
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)

    # Draw the damage
    damage_width = width - health_width
    pygame.draw.rect(screen, DARK_RED, (x + health_width, y, damage_width, height))

def draw_health_bar_jimmy(screen, x, y, width, height, health):
    draw_health_bar(screen, x, y, width, height, health)
    #Draw the name
    name_text = FONT.render("Jimmy", True, BLACK)
    screen.blit(name_text, (x, y+height+5))

def draw_health_bar_opponent(screen, x, y, width, height, health):
    draw_health_bar(screen, x, y, width, height, health)
    #Draw the name
    name_text = FONT.render("Opponent", True, BLACK)
    screen.blit(name_text, (x, y+height+5))

# --- Button Actions ---
def start_game():
    global current_state
    current_state = GameState.GAME_MENU

def options():
    global current_state
    current_state = GameState.OPTIONS_MENU

def open_credits():
    global current_state
    current_state = GameState.CREDITS

def exit_action():
    print("Exiting game.")
    pygame.quit()
    exit()

def test_print(message):
    print(message)

def back_to_menu():
    global current_state, turn
    current_state = GameState.MAIN_MENU
    turn = 1

def game_button_action1(): #Kick
    global health2
    print("Game Kick clicked!")
    health2 -= 5
    end_turn()

def game_button_action2(): #Heal
    global health
    print("Game Heal clicked!")
    max_health = 100
    if health < max_health:
        health += 20
    end_turn()

def game_button_action3():
    print("Game Button 3 clicked!")
    end_turn()

def game_button_action4():
    print("Game Button 4 clicked!")
    end_turn()

# --- Menu Functions ---
def draw_credits(screen):
    screen.fill(WHITE)
    credits_text = LARGE_FONT.render("Credits", True, BLACK)
    credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(credits_text, credits_rect)

    name_text = FONT.render("Created by: Luken", True, BLACK)
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
    screen.blit(name_text, name_rect)

    credits_back_button.draw(screen)

def draw_game_menu(screen):
    # Calculate the height of the bottom 1/3
    bottom_third_height = SCREEN_HEIGHT // 3

    # Draw the light gray rectangle for the bottom 1/3
    pygame.draw.rect(screen, LIGHT_GRAY, (0, SCREEN_HEIGHT - bottom_third_height, SCREEN_WIDTH, bottom_third_height))

    game_menu_text = LARGE_FONT.render("Game Menu", True, BLACK)
    game_menu_rect = game_menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(game_menu_text, game_menu_rect)

    # Draw the solid blue circle - moved higher up
    circle_radius = 100
    circle_x = circle_radius + 150  # Moved to the right
    circle_y = SCREEN_HEIGHT - circle_radius - 300  # Moved up even higher (increased from 100 to 300)
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), circle_radius)
    # Draw the solid red circle
    circle_radius = 100
    circle_x_red = SCREEN_WIDTH - circle_radius - 150  # Moved to the left
    circle_y_red = circle_radius + 250  # Moved down
    pygame.draw.circle(screen, RED_COLOR, (circle_x_red, circle_y_red), circle_radius)

    game_menu_back_button.draw(screen)

    # --- Draw the 4 buttons in the bottom rectangle
    game_button_width = SCREEN_WIDTH // 2  # Two columns now
    game_button_height = bottom_third_height // 2
    game_button_y = SCREEN_HEIGHT - bottom_third_height
    game_buttons = [
        Button(0, game_button_y, game_button_width, game_button_height, "Kick", LIGHT_BLUE, GRAY,
               game_button_action1),
        Button(0, game_button_y + game_button_height, game_button_width, game_button_height, "Heal", LIGHT_BLUE,
               GRAY, game_button_action2),  # Under Kick
        Button(game_button_width, game_button_y, game_button_width, game_button_height, "Button 3", LIGHT_BLUE,
               GRAY, game_button_action3),
        Button(game_button_width, game_button_y + game_button_height, game_button_width, game_button_height,
               "Button 4", LIGHT_BLUE, GRAY, game_button_action4),  # Under button 3
    ]

    for button in game_buttons:
        button.draw(screen)

    return game_buttons  # return the list of buttons

def main_menu():
    """Displays the main menu."""
    global current_state, turn, health, health2, game_menu_back_button #added game_menu_back_button
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Main Menu")

    # Load and scale background images
    assets_path = os.path.join(".", "assets", "menus")
    pic1_path = os.path.join(assets_path, "MiiChannel.png")
    pic2_path = os.path.join(assets_path, "fightMenu.png")

    try:
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

    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image: {e}")
        return

    # Font for the title
    title_font = pygame.font.Font(None, 64)

    # Button positions
    play_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    play_button_y = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 75
    quit_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    quit_button_y = SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 - 25
    slide_button_x = SCREEN_WIDTH - BUTTON_WIDTH
    slide_button_y = SCREEN_HEIGHT - BUTTON_HEIGHT

    # Create buttons
    play_button = Button(play_button_x, play_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Fight!!", BUTTON_COLOR, GRAY, start_game)
    quit_button = Button(quit_button_x, quit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", BUTTON_COLOR, GRAY, exit_action)
    slide_button = Button(slide_button_x, slide_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "More", BUTTON_COLOR, GRAY, options)

    # --- Menu Variables ---
    menu_offset = 0
    menu_slide_speed = 10
    second_menu_visible = False

    # Second Menu Buttons
    option1_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    option1_button_y = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - 75
    option2_button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
    option2_button_y = SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 - 25
    back_button_x = 0
    back_button_y = SCREEN_HEIGHT - BUTTON_HEIGHT

    option1_button = Button(option1_button_x, option1_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Option 1", BUTTON_COLOR, GRAY, test_print, "Option 1")
    option2_button = Button(option2_button_x, option2_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Option 2", BUTTON_COLOR, GRAY, test_print, "Option 2")
    back_button = Button(back_button_x, back_button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", BUTTON_COLOR, GRAY, back_to_menu)
    game_menu_back_button = Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, back_to_menu) #added game_menu_back_button here

    # --- Menu Buttons ---
    menu_buttons = [play_button, quit_button, slide_button]
    option_buttons = [option1_button, option2_button, back_button]
    credits_back_button = Button(20, 20, 150, 50, "Back to Menu", LIGHT_BLUE, GRAY, back_to_menu)
    game_buttons = []

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # added to modify health
                if event.key == pygame.K_LEFT:
                    health -= 5
                if event.key == pygame.K_RIGHT:
                    health += 5
            if current_state == GameState.MAIN_MENU:
                for button in menu_buttons:
                    button.handle_event(event)
            elif current_state == GameState.OPTIONS_MENU:
                for button in option_buttons:
                    button.handle_event(event)
            elif current_state == GameState.CREDITS:
                credits_back_button.handle_event(event)
            elif current_state == GameState.GAME_MENU:
                game_menu_back_button.handle_event(event)
                for button in game_buttons:
                    button.handle_event(event)

        # --- Menu Sliding Logic ---
        if current_state == GameState.OPTIONS_MENU:
            menu_offset -= menu_slide_speed
            if menu_offset <= -SCREEN_WIDTH:
                menu_offset = -SCREEN_WIDTH
        else:
            menu_offset += menu_slide_speed
            if menu_offset >= 0:
                menu_offset = 0

        # Clear the screen
        screen.fill(BLACK)

        # Draw content based on game state
        if current_state == GameState.MAIN_MENU:
            # Draw Main Menu
            first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            first_menu_surface.blit(pic1, (0, 0))
            draw_text("My Game", title_font, WHITE, first_menu_surface, SCREEN_WIDTH // 2 - 80, 50)
            for button in menu_buttons:
                button.draw(first_menu_surface)
            screen.blit(first_menu_surface, (menu_offset, 0))

            # Draw Second Menu
            second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            second_menu_surface.blit(pic2, (0, 0))
            draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2 - 80, 50)
            for button in option_buttons:
                button.draw(second_menu_surface)
            screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
        elif current_state == GameState.OPTIONS_MENU:
            # Draw Main Menu
            first_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            first_menu_surface.blit(pic1, (0, 0))
            draw_text("My Game", title_font, WHITE, first_menu_surface, SCREEN_WIDTH // 2 - 80, 50)
            for button in menu_buttons:
                button.draw(first_menu_surface)
            screen.blit(first_menu_surface, (menu_offset, 0))

            # Draw Second Menu
            second_menu_surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
            second_menu_surface.blit(pic2, (0, 0))
            draw_text("Options", title_font, BLACK, second_menu_surface, SCREEN_WIDTH // 2 - 80, 50)
            for button in option_buttons:
                button.draw(second_menu_surface)
            screen.blit(second_menu_surface, (menu_offset + SCREEN_WIDTH, 0))
        elif current_state == GameState.CREDITS:
            draw_credits(screen)
        elif current_state == GameState.GAME_MENU:
            game_buttons = draw_game_menu(screen)
            draw_health_bar_jimmy(screen, 20, 100, 200, 20, health)  # added to draw the healthbar
            draw_health_bar_opponent(screen, SCREEN_WIDTH-220, 100, 200, 20, health2) #draw the second health bar
            draw_turn(screen, turn)

        pygame.display.flip()

    pygame.quit()

# --- Main ---
if __name__ == "__main__":
    main_menu()
