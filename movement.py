import pygame
from worldObstacles import SlowObstacle
class Player:
    """Represents the player in the game."""

    def __init__(self, x, y, width, height, color, speed):
        """
        Initializes the player.
        :param x: Initial x-coordinate of the player.
        :param y: Initial y-coordinate of the player.
        :param width: Width of the player.
        :param height: Height of the player.
        :param color: Color of the player (RGB tuple).
        :param speed: Movement speed of the player.
        """
        self.rect = pygame.Rect(x, y, width, height)  # Player's rectangle
        self.color = color  # Player's color
        self.speed = speed  # Player's movement speed
        self.base_speed = speed  # Store the original speed

    def handle_movement(self, screen_width, screen_height, obstacles, slow_obstacles):
        """
        Handles player movement using arrow keys and WSAD.
        :param screen_width: Width of the screen (for boundary constraints).
        :param screen_height: Height of the screen (for boundary constraints).
        :param obstacles: List of pygame.Rect objects representing obstacles.
        :param slow_obstacles: List of SlowObstacle objects that slow the player down.
        """
        keys = pygame.key.get_pressed()
        new_rect = self.rect.copy()  # Create a copy to test movement

        # Arrow keys and WSAD mapping
        if keys[pygame.K_UP] or keys[pygame.K_w]:  # Move up
            new_rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  # Move down
            new_rect.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  # Move left
            new_rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:  # Move right
            new_rect.x += self.speed

        # Check for collisions with obstacles
        if not any(new_rect.colliderect(obstacle) for obstacle in obstacles):
            self.rect = new_rect  # Update position if no collision

        # Enforce screen boundaries
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

        # Check for slow obstacles and adjust speed
        self.speed = self.base_speed  # Reset to base speed
        for slow_obstacle in slow_obstacles:
            if self.rect.colliderect(slow_obstacle.rect):
                self.speed = self.base_speed * slow_obstacle.slow_factor
                break  # Apply the slowest speed if overlapping multiple obstacles