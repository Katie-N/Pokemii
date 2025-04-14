import pygame

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
