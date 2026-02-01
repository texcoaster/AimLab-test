# screens/start_screen.py
import pygame
from screens.base_screen import BaseScreen
from entities.button import Button
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, FONT_NAME, FONT_SIZE
from screens.game_screen import GameScreen # Import the actual GameScreen

class StartScreen(BaseScreen):
    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE * 2) # Larger font for title

        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.start_button = Button(
            button_x, SCREEN_HEIGHT // 2 - 60, button_width, button_height,
            "시작",
            lambda: self.game_controller.set_screen(GameScreen(self.game_controller))
        )
        self.exit_button = Button(
            button_x, SCREEN_HEIGHT // 2 + 20, button_width, button_height,
            "종료",
            self.game_controller.quit_game
        )
        
        self.buttons = [self.start_button, self.exit_button]

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(BLACK) # Fill background

        # Draw title
        title_surface = self.font.render("발로란트 에임 트레이너", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
