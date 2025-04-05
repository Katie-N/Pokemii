import random
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
light_gray = (200, 200, 200)
light_blue = (173, 216, 230)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
dark_red = (150, 0, 0)
red_color = (255,0,0)
purple = (128,0,128)

# Font
turn_font = pygame.font.Font(None, 50)
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

# --- Game Variables ---
health = 100
health2 = 100
turn = 1
max_health = 100
harden_active = False
empower_active = False

# --- Button Actions ---
def start_game():
    global current_state, health, health2, turn, harden_active, empower_active
    current_state = GameState.GAME_MENU
    health = 100
    health2 = 100
    turn = 1
    harden_active = False
    empower_active = False

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
    global current_state, turn, harden_active, empower_active
    current_state = GameState.MENU
    turn = 1
    harden_active = False
    empower_active = False

def opponent_turn():
    global health, health2, turn, harden_active
    moves = ["Kick", "Heal", "Stomp", "Scratch"]
    chosen_move = random.choice(moves)
    print(f"Opponent used {chosen_move}!")
    damage_multiplier = 0.5 if harden_active else 1

    if chosen_move == "Kick":
        health -= 5 * damage_multiplier
        print("Opponent kicked Jimmy!")
    elif chosen_move == "Heal":
        if health2 < max_health: #added to make sure health does not go above max health
            health2 += 10
        if health2 > max_health: #added to make sure health does not go above max health
            health2 = max_health
        print("Opponent healed itself!")
    elif chosen_move == "Stomp":
        health -= 10 * damage_multiplier
        print("Opponent stomped Jimmy!")
    elif chosen_move == "Scratch":
        health -= 20 * damage_multiplier
        print("Opponent scratched Jimmy!")
    end_turn()

def end_turn():
    global turn, health, health2, harden_active, empower_active
    print("Turn Ended")
    if health <= 0 or health2 <= 0: #added to make sure that the game restarts if the opponent's health is 0
        start_game()
    elif turn == 1:
        turn = 2
        opponent_turn()
    elif turn == 2:
        turn = 1
        harden_active = False #harden is only active for 1 turn
        

def game_button_action1(): #Kick
    global health2, empower_active
    print("Game Kick clicked!")
    damage_multiplier = 2 if empower_active else 1
    health2 -= 25 * damage_multiplier
    end_turn()
    empower_active = False #empower is only active for 1 turn

def game_button_action2(): #Heal
    global health
    print("Game Heal clicked!")
    if health < max_health:
        health += 20
    if health > max_health: #added to make sure health does not go above max health
        health = max_health
    end_turn()
def game_button_action3(): #Harden
    global harden_active
    print("Game Harden clicked!")
    harden_active = True
    end_turn()

def game_button_action4(): #Empower
    global empower_active
    print("Game Empower clicked!")
    empower_active = True
    end_turn()

def draw_turn(screen, turn):
    turn_text = turn_font.render(f"Turn {turn}", True, black)
    screen.blit(turn_text, (screen_width // 2 - 50, 20))

# --- Button Creation ---
button_width = 300
button_height = 70
button_x = (screen_width - button_width) // 2
button_y_start = 250
button_spacing = 130

menu_buttons = [
    Button(button_x, button_y_start, button_width, button_height, "Fight!!", green, gray, start_game),
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
    # Calculate the height of the bottom 1/3
    bottom_third_height = screen_height // 3

    # Draw the light gray rectangle for the bottom 1/3
    pygame.draw.rect(screen, light_gray, (0, screen_height - bottom_third_height, screen_width, bottom_third_height))

    game_menu_text = large_font.render("Game Menu", True, black)
    game_menu_rect = game_menu_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(game_menu_text, game_menu_rect)

    # Draw the solid blue circle - moved higher up
    circle_radius = 100
    circle_x = circle_radius + 150  # Moved to the right
    circle_y = screen_height - circle_radius - 300  # Moved up even higher (increased from 100 to 300)
    pygame.draw.circle(screen, blue, (circle_x, circle_y), circle_radius)
    # Draw the solid red circle
    circle_radius = 100
    circle_x_red = screen_width - circle_radius - 150  # Moved to the left
    circle_y_red = circle_radius + 250  # Moved down
    pygame.draw.circle(screen, red_color, (circle_x_red, circle_y_red), circle_radius)

    game_menu_back_button.draw(screen)

    # --- Draw the 4 buttons in the bottom rectangle
    game_button_width = screen_width // 2  # Two columns now
    game_button_height = bottom_third_height // 2
    game_button_y = screen_height - bottom_third_height
    game_buttons = [
        Button(0, game_button_y, game_button_width, game_button_height, "Kick", light_blue, gray,
               game_button_action1),
        Button(0, game_button_y + game_button_height, game_button_width, game_button_height, "Heal", light_blue,
               gray, game_button_action2),  # Under Kick
        Button(game_button_width, game_button_y, game_button_width, game_button_height, "Harden", light_blue,
               gray, game_button_action3),
        Button(game_button_width, game_button_y + game_button_height, game_button_width, game_button_height,
               "Empower", light_blue, gray, game_button_action4),  # Under button 3
    ]

    for button in game_buttons:
        button.draw(screen)

    return game_buttons  # return the list of buttons

# --- Health Bar ---
def draw_health_bar(screen, x, y, width, height, health):
    #health_bar variables
    if health < 0:
        health = 0

    # Calculate health bar
    health_percentage = health / max_health

    # Draw the background
    pygame.draw.rect(screen, gray, (x, y, width, height))

    # Draw the health portion
    health_width = int(width * health_percentage)
    pygame.draw.rect(screen, green, (x, y, health_width, height))

    # Draw the border
    pygame.draw.rect(screen, black, (x, y, width, height), 2)

    # Draw the damage
    damage_width = width - health_width
    pygame.draw.rect(screen, dark_red, (x + health_width, y, damage_width, height))

def draw_health_bar_jimmy(screen, x, y, width, height, health):
    draw_health_bar(screen, x, y, width, height, health)
    #Draw the name
    name_text = font.render("Jimmy", True, black)
    screen.blit(name_text, (x, y+height+5))
    if harden_active:
        pygame.draw.rect(screen, blue, (x, y-30, 50, 20))
        harden_text = font.render("Harden", True, black)
        screen.blit(harden_text, (x, y-30))
    if empower_active:
        pygame.draw.rect(screen, purple, (x+50, y-30, 50, 20))
        empower_text = font.render("Empower", True, black)
        screen.blit(empower_text, (x+50, y-30))

def draw_health_bar_opponent(screen, x, y, width, height, health):
    draw_health_bar(screen, x, y, width, height, health)
    #Draw the name
    name_text = font.render("Opponent", True, black)
    screen.blit(name_text, (x, y+height+5))
  
 


# Game loop
running = True
game_buttons = []
health = 100
turn = 1
health2 = 100
harden_active = False
empower_active = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # added to modify health
            if event.key == pygame.K_LEFT:
                health -= 5
            if event.key == pygame.K_RIGHT:
                health += 5
        if current_state == GameState.MENU:
            for button in menu_buttons:
                button.handle_event(event)
        elif current_state == GameState.CREDITS:
            credits_back_button.handle_event(event)
        elif current_state == GameState.GAME_MENU:
            game_menu_back_button.handle_event(event)
            for button in game_buttons:
                button.handle_event(event)

    # Clear the screen
    screen.fill(white)

    # Draw content based on game state
    if current_state == GameState.MENU:
        for button in menu_buttons:
            button.draw(screen)
        #removed draw_health_bar here.
    elif current_state == GameState.CREDITS:
        draw_credits(screen)
    elif current_state == GameState.GAME_MENU:
        game_buttons = draw_game_menu(screen)
        draw_health_bar_jimmy(screen, 20, 100, 200, 20, health)  # added to draw the healthbar
        draw_health_bar_opponent(screen, screen_width-220, 100, 200, 20, health2) #draw the second health bar
        draw_turn(screen, turn)
    # Update the display
    pygame.display.flip()

pygame.quit()
