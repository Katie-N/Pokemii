import globalSettings
import draw
import pygame

def create_button(text, x, y, width, height, text_color, surface, action=None, image=None):
    """Creates a button, optionally with an image, and returns its rectangle."""
    try:
        button_rect = pygame.Rect(x, y, width, height)
        # Create a transparent surface for the button
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        # Draw a semi-transparent rectangle (optional, for a subtle button effect)
        pygame.draw.rect(button_surface, (0, 0, 0, 0), (0, 0, width, height))  # Last value is alpha (0-255)

        if image:
            button_surface.blit(image, (0, 0))

        surface.blit(button_surface, (x,y))
        font = pygame.font.Font(None, 36)
        draw.draw_text(text, font, text_color, surface, x + 10, y + 10)
        return button_rect, action
    except Exception as e:
        print(f"Error creating button: {e}")
        return None, None


def calculate_button_positions():
    """Calculates button positions relative to the screen."""
    try:
        button_y = int(globalSettings.SCREEN_HEIGHT * 0.77222)
        left_button_x = int(globalSettings.SCREEN_WIDTH * 0.1916)
        right_button_x = int(globalSettings.SCREEN_WIDTH * 0.52083)
        next_button_x = int(globalSettings.SCREEN_WIDTH * 0.9333)
        next_button_y = int(globalSettings.SCREEN_HEIGHT * 0.347222)
        back_button_x = int(globalSettings.SCREEN_WIDTH * 0.033333)
        pick_save_x = 10
        pick_save_y = 10

        return (
            button_y,
            left_button_x,
            right_button_x,
            next_button_x,
            next_button_y,
            back_button_x,
            pick_save_x,
            pick_save_y,
        )
    except Exception as e:
        print(f"Error calculating button positions: {e}")
        return (0,0,0,0,0,0,0,0)
