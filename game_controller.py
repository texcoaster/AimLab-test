# game_controller.py
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK

# Placeholder imports for screens (will be replaced later)
from screens.base_screen import BaseScreen

class GameController:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("발로란트 에임 트레이너")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = None

    def quit_game(self):
        self.running = False

    def set_screen(self, screen_instance):
        if not isinstance(screen_instance, BaseScreen):
            raise TypeError("Screen must be an instance of BaseScreen")
        self.current_screen = screen_instance

    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if self.current_screen:
                    self.current_screen.handle_events(events) # Pass all events to current screen

            if self.current_screen:
                self.current_screen.update()

            self.screen.fill(BLACK)
            if self.current_screen:
                self.current_screen.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
