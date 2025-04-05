import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pokemii Menu")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
light_blue = (173, 216, 230)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Button class
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
        text_surface = font.render(self.text, True, black)
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

# --- Game States ---
class GameState:
    MENU = 0
    CREDITS = 1
    GAME_MENU = 2

current_state = GameState.MENU

# --- Button Actions ---
def start_game():
    global current_state
    current_state = GameState.GAME_MENU

def options():
    print("Opening Options!")
    # Add your options menu code here

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
    global current_state
    current_state = GameState.MENU

# --- Button Creation ---
button_width = 300
button_height = 70
button_x = (screen_width - button_width) // 2
button_y_start = 250
button_spacing = 130

menu_buttons = [
    Button(button_x, button_y_start, button_width, button_height, "Start Game", green, gray, start_game),
    Button(button_x, button_y_start + button_spacing, button_width, button_height, "Options", yellow, gray, options),
    Button(button_x, button_y_start + 2 * button_spacing, button_width, button_height, "Credits", light_blue, gray, open_credits),
    Button(button_x, button_y_start + 3 * button_spacing, button_width, button_height, "Exit", red, gray, exit_action),
    Button(20, 20, 100, 40, "test", light_blue, gray, test_print, "hello")
]

credits_back_button = Button(20, 20, 150, 50, "Back to Menu", light_blue, gray, back_to_menu)
game_menu_back_button = Button(20, 20, 150, 50, "Back to Menu", light_blue, gray, back_to_menu)

# --- Credits Text ---
def draw_credits(screen):
    screen.fill(white)
    credits_text = large_font.render("Credits", True, black)
    credits_rect = credits_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(credits_text, credits_rect)

    name_text = font.render("Created by: Luken", True, black)
    name_rect = name_text.get_rect(center=(screen_width // 2, 250))
    screen.blit(name_text, name_rect)

    credits_back_button.draw(screen)

# --- Game Menu text ---
def draw_game_menu(screen):
    screen.fill(white)
    game_menu_text = large_font.render("Game Menu", True, black)
    game_menu_rect = game_menu_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(game_menu_text, game_menu_rect)

    # Draw the solid blue circle - moved higher up
    circle_radius = 100
    circle_x = circle_radius + 150  # Moved to the right
    circle_y = screen_height - circle_radius - 250  # Moved up even higher (increased from 100 to 250)
    pygame.draw.circle(screen, blue, (circle_x, circle_y), circle_radius)

    game_menu_back_button.draw(screen)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if current_state == GameState.MENU:
            for button in menu_buttons:
                button.handle_event(event)
        elif current_state == GameState.CREDITS:
            credits_back_button.handle_event(event)
        elif current_state == GameState.GAME_MENU:
            game_menu_back_button.handle_event(event)

    # Clear the screen
    screen.fill(white)

    # Draw content based on game state
    if current_state == GameState.MENU:
        for button in menu_buttons:
            button.draw(screen)
    elif current_state == GameState.CREDITS:
        draw_credits(screen)
    elif current_state == GameState.GAME_MENU:
        draw_game_menu(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
