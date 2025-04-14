import pygame
from worldObstacles import SlowObstacle, TransitionObstacle

def load_world1(player, set_current_world):
    """Sets up the first world."""
    print("Loading World 1...")
    player.rect.x = 100
    player.rect.y = 100

    # Obstacles for World 1
    obstacles = [
        pygame.Rect(300, 200, 100, 100),  # Example obstacle 1
        pygame.Rect(500, 400, 150, 50),  # Example obstacle 2
    ]

    # Slow obstacles for World 1
    slow_obstacles = [
        SlowObstacle(200, 150, 100, 100, slow_factor=0.5, color=(0, 0, 255)),
    ]

    # Transition obstacles for World 1
    transition_obstacles = [
        TransitionObstacle(
            600, 100, 100, 100,
            lambda: set_current_world("world2", player),  # Transition to World 2
            color=(255, 255, 0)
        ),
    ]

    return obstacles, slow_obstacles, transition_obstacles


