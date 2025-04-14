world_registry = {}

def register_world(world_name, load_function):
    """
    Registers a world with its loading function.
    :param world_name: Name of the world (e.g., "world1").
    :param load_function: Function to load the world.
    """
    world_registry[world_name] = load_function

def load_world(world_name, player, set_current_world):
    """
    Loads the specified world.
    :param world_name: Name of the world to load (e.g., "world1", "world2").
    :param player: The player object to reset position or apply world-specific logic.
    :param set_current_world: Callback function to update the current world.
    :return: A tuple containing obstacles, slow_obstacles, and transition_obstacles.
    """
    if world_name in world_registry:
        return world_registry[world_name](player, set_current_world)
    else:
        raise ValueError(f"Unknown world: {world_name}")