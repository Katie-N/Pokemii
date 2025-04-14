import pygame
from worldObstacles import SlowObstacle, TransitionObstacle


def load_world2(player, set_current_world):
    """Sets up the second world."""
    print("Loading World 2...")
    player.rect.x = 50
    player.rect.y = 50

    # Obstacles for World 2
    obstacles = [
        pygame.Rect(100, 300, 200, 50),  # Example obstacle 1
    ]

    # Slow obstacles for World 2
    slow_obstacles = [
        SlowObstacle(400, 300, 150, 150, slow_factor=0.3, color=(0, 255, 255)),
    ]

    # Transition obstacles for World 2
    transition_obstacles = [
        TransitionObstacle(
            700, 500, 100, 100,
            lambda: set_current_world("world1", player),  # Transition back to World 1
            color=(255, 255, 0)
        ),
    ]

    return obstacles, slow_obstacles, transition_obstacles
