import pygame
import worldObstacles as wo
import globalSettings as gs

def load_world2(player, set_current_world):
    """Sets up the second world."""
    print("Loading World 2...")
    player.rect.x = 50
    player.rect.y = 50

    # Obstacles for World 2
    obstacles = [
        wo.topLeft,
        wo.topRight,
        wo.rightTop,
    ]

    # Slow obstacles for World 2
    slow_obstacles = [
        wo.SlowObstacle(400, 300, 150, 150, slow_factor=0.3, color=(0, 255, 255)),
    ]

    # Transition obstacles for World 2
    transition_obstacles = [
        wo.create_transition_obstacle(
            300, 0, 150, 50,  # Position and size of the obstacle
            "world1",  # Target world
            (400, 550),  # Spawn position in the target world
            set_current_world,  # Callback to update the current world
            player,  # Pass the player object
            color=(255, 255, 0)  # Color of the obstacle
        ),
    ]

    return obstacles, slow_obstacles, transition_obstacles
