import pygame
import worldObstacles as wo
import globalSettings as gs

def load_world3(player, set_current_world):
    """Sets up the third world."""
    print("Loading World 3...")
    player.rect.x = 100
    player.rect.y = 100

    # Obstacles for World 3
    obstacles = [
        wo.btmLeft,
        wo.btmRight,
    ]

    # Slow obstacles for World 3
    slow_obstacles = [
        wo.SlowObstacle(200, 150, 100, 100, slow_factor=0.5, color=(0, 0, 255)),
    ]

    # Transition obstacles for World 3
    transition_obstacles = [
        wo.create_transition_obstacle(
            0, 200, 50, 150,  # Position and size of the obstacle
            "world2",  # Target world
            (400, 0),  # Spawn position in the target world
            set_current_world,  # Callback to update the current world
            player,  # Pass the player object
            color=(255, 255, 0)  # Color of the obstacle
        ),
    ]

    return obstacles, slow_obstacles, transition_obstacles
