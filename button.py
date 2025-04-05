import pygame

class Button:
    def __init__(self, x, y, normal_image, hover_image, pressed_image, text, width, height):
        self.x = x
        self.y = y
        self.normal_image = pygame.transform.scale(normal_image, (width, height))
        self.hover_image = pygame.transform.scale(hover_image, (width, height))
        self.pressed_image = pygame.transform.scale(pressed_image, (width, height))
        self.current_image = self.normal_image
        self.rect = self.current_image.get_rect(topleft=(x, y))
        self.is_hovered = False
        self.is_pressed = False
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.text_color = (255, 255, 255)

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = self.font.render(self.text, True, self.text_color).get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed:
                self.is_pressed = False
                if self.is_hovered:
                    return True  # Button was clicked

        if self.is_pressed:
            self.current_image = self.pressed_image
        elif self.is_hovered:
            self.current_image = self.hover_image
        else:
            self.current_image = self.normal_image
        return False
