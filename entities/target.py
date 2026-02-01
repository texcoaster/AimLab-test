# entities/target.py
import pygame
import random
from settings import RED, GREEN, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, score_value=10):
        super().__init__()
        self.radius = radius
        self.color = color
        self.score_value = score_value

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Targets might move later, but for now, they are static
        pass

    def draw(self, screen):
        # This can be used for explicit drawing, but Group.draw() is usually enough
        screen.blit(self.image, self.rect)

    def hit(self):
        # Logic when the target is hit
        return self.score_value

    @classmethod
    def create_random(cls, min_radius, max_radius, min_score, max_score):
        radius = random.randint(min_radius, max_radius)
        x = random.randint(radius, SCREEN_WIDTH - radius)
        y = random.randint(radius, SCREEN_HEIGHT - radius)
        color = random.choice([RED, GREEN, BLUE]) # Example colors
        score_value = random.randint(min_score, max_score)
        return cls(x, y, radius, color, score_value)
