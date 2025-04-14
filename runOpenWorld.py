import pygame
from movement import Player
from worlds.worldLoader import load_world, register_world
from worlds.world1 import load_world1
from worlds.world2 import load_world2

# Initialize pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Open World Game")

# Player setup
player = Player(x=100, y=100, width=50, height=50, color=(255, 0, 0), speed=5)

# Register worlds
register_world("world1", load_world1)
register_world("world2", load_world2)

# Define a function to update the current world
def set_current_world(new_world, player):
    global current_world, obstacles, slow_obstacles, transition_obstacles
    current_world = new_world
    obstacles, slow_obstacles, transition_obstacles = load_world(current_world, player, set_current_world)

# Load the initial world
current_world = "world1"
obstacles, slow_obstacles, transition_obstacles = load_world(current_world, player, set_current_world)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    player.handle_movement(screen_width, screen_height, obstacles, slow_obstacles)

    # Check for collisions with transition obstacles
    for transition_obstacle in transition_obstacles:
        transition_obstacle.check_collision(player.rect)

    # Draw everything
    screen.fill((0, 0, 0))  # Clear screen with black
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 255, 0), obstacle)  # Draw regular obstacles
    for slow_obstacle in slow_obstacles:
        slow_obstacle.draw(screen)  # Draw slow obstacles
    for transition_obstacle in transition_obstacles:
        transition_obstacle.draw(screen)  # Draw transition obstacles
    pygame.draw.rect(screen, player.color, player.rect)  # Draw the player

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()