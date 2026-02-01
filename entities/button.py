# entities/button.py
import pygame
from settings import WHITE, BLACK, GREY, FONT_NAME, FONT_SIZE

class Button:
    def __init__(self, x, y, width, height, text, action=None,
                 button_color=GREY, hover_color=WHITE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.button_color = button_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    def set_text(self, new_text):
        """Updates the text displayed on the button."""
        self.text = new_text

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.button_color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:  # Left click
                if self.action:
                    self.action()
