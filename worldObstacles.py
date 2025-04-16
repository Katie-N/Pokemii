import pygame
import globalSettings as gs

class SlowObstacle:
    """Represents an obstacle that slows the player down."""

    def __init__(self, x, y, width, height, slow_factor, color=(0, 0, 255)):
        """
        Initializes the slow obstacle.
        :param x: X-coordinate of the obstacle.
        :param y: Y-coordinate of the obstacle.
        :param width: Width of the obstacle.
        :param height: Height of the obstacle.
        :param slow_factor: Factor by which the player's speed is reduced (e.g., 0.5 for 50% speed).
        :param color: Color of the obstacle (RGB tuple).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.slow_factor = slow_factor
        self.color = color

    def draw(self, screen):
        """Draws the slow obstacle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)

class TransitionObstacle:
    """Represents an obstacle that triggers a location transition when touched by the player."""

    def __init__(self, x, y, width, height, new_location_callback, color=(255, 255, 0)):
        """
        Initializes the transition obstacle.
        :param x: X-coordinate of the obstacle.
        :param y: Y-coordinate of the obstacle.
        :param width: Width of the obstacle.
        :param height: Height of the obstacle.
        :param new_location_callback: A function to call when the player touches the obstacle.
        :param color: Color of the obstacle (RGB tuple).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.new_location_callback = new_location_callback
        self.color = color

    def check_collision(self, player_rect):
        """
        Checks if the player collides with the obstacle.
        :param player_rect: The player's rectangle.
        """
        if self.rect.colliderect(player_rect):
            self.new_location_callback()  # Trigger the location transition

    def draw(self, screen):
        """Draws the transition obstacle on the screen."""
        pygame.draw.rect(screen, self.color, self.rect)

# Predefined static obstacles
btmLeft = pygame.Rect(0, 550, 300, 50)  # Bottom left
btmRight = pygame.Rect(450, 550, 400, 50)  # Bottom right
topLeft = pygame.Rect(0, 0, 300, 50)  # Top left
topRight = pygame.Rect(450, 0, 400, 50)  # Top right
rightTop = pygame.Rect(750, 50, 50, 150)  # Right top

# Factory function for creating TransitionObstacle dynamically
def create_transition_obstacle(x, y, width, height, target_world, spawn_position, set_current_world, player, color=(255, 255, 0)):
    """
    Creates a TransitionObstacle dynamically.
    :param x: X-coordinate of the obstacle.
    :param y: Y-coordinate of the obstacle.
    :param width: Width of the obstacle.
    :param height: Height of the obstacle.
    :param target_world: The name of the target world (e.g., "world2").
    :param spawn_position: The spawn position in the target world (tuple of x, y).
    :param set_current_world: The function to call to update the current world.
    :param player: The player object to pass to set_current_world.
    :param color: Color of the obstacle (RGB tuple).
    :return: A TransitionObstacle object.
    """
    return TransitionObstacle(
        x, y, width, height,
        lambda: set_current_world(target_world, player, spawn_position=spawn_position),
        color
    )
def top_center_transition_obstacle(target_world, set_current_world, player):
    return create_transition_obstacle(300, 0, 150, 50, target_world, (400, 550), set_current_world, player)  # Example transition obstacle
   