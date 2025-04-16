import pygame
import worldObstacles as wo

def load_world1(player, set_current_world):
    """Sets up the first world."""
    print("Loading World 1...")
    player.rect.x = 100
    player.rect.y = 100

    # Obstacles for World 1
    obstacles = [
        pygame.Rect(0, 550, 400, 50),  # Example obstacle 1
        pygame.Rect(450, 550, 400, 50),  # Example obstacle 2
        wo.btmLeft
    ]

    # Slow obstacles for World 1
    slow_obstacles = [
        wo.SlowObstacle(200, 150, 100, 100, slow_factor=0.5, color=(0, 0, 255)),
    ]

    # Transition obstacles for World 1
    transition_obstacles = [
        wo.create_transition_obstacle(
            300, 0, 150, 50,  # Position and size of the obstacle
            "world2",  # Target world
            (400, 550),  # Spawn position in the target world
            set_current_world,  # Callback to update the current world
            player,  # Pass the player object
            color=(255, 255, 0)  # Color of the obstacle
        ),
    ]

    return obstacles, slow_obstacles, transition_obstacles


