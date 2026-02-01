# main.py
from game_controller import GameController
from screens.start_screen import StartScreen # Import the actual StartScreen

if __name__ == "__main__":
    game_controller = GameController()
    start_screen = StartScreen(game_controller)
    game_controller.set_screen(start_screen)
    game_controller.run()