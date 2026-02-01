# screens/base_screen.py
from abc import ABC, abstractmethod

class BaseScreen(ABC):
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def set_game_controller(self, game_controller):
        """Sets or updates the game controller for this screen."""
        self.game_controller = game_controller

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass