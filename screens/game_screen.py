# screens/game_screen.py
import pygame
import random
from screens.base_screen import BaseScreen
from entities.target import Target
from entities.button import Button
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, RED, GREEN, BLUE, FONT_NAME, FONT_SIZE

class GameScreen(BaseScreen):
    COUNTDOWN = 0
    PLAYING = 1
    GAME_OVER = 2

    def __init__(self, game_controller):
        super().__init__(game_controller)
        self.state = self.COUNTDOWN
        self.score = 0
        self.time_left = 30 # seconds
        self.countdown_timer = 3 # seconds
        self.last_tick = pygame.time.get_ticks()

        self.targets = pygame.sprite.Group()
        self.target_spawn_timer = 0.5 # seconds between target spawns
        self.current_target_spawn_time = 0

        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        # Game Over buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        self.restart_button = Button(
            button_x, SCREEN_HEIGHT // 2 - 60, button_width, button_height,
            "다시 시작",
            self._reset_game
        )
        # Placeholder for main menu button, will be updated when StartScreen is properly imported
        self.main_menu_button = Button(
            button_x, SCREEN_HEIGHT // 2 + 20, button_width, button_height,
            "메인으로",
            self._go_to_main_menu
        )
        self.game_over_buttons = [self.restart_button, self.main_menu_button]

    def _reset_game(self):
        self.state = self.COUNTDOWN
        self.score = 0
        self.time_left = 30
        self.countdown_timer = 3
        self.targets.empty()
        self.last_tick = pygame.time.get_ticks()

    def _go_to_main_menu(self):
        # This will be replaced with an actual import of StartScreen later
        from screens.start_screen import StartScreen
        self.game_controller.set_screen(StartScreen(self.game_controller))


    def handle_events(self, events):
        for event in events:
            if self.state == self.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Left click
                    for target in list(self.targets): # iterate over a copy because we might remove elements
                        if target.rect.collidepoint(event.pos):
                            self.score += target.hit()
                            target.kill() # Remove target from group
            elif self.state == self.GAME_OVER:
                for button in self.game_over_buttons:
                    button.handle_event(event)

    def update(self):
        current_tick = pygame.time.get_ticks()
        delta_time = (current_tick - self.last_tick) / 1000.0 # Convert to seconds
        self.last_tick = current_tick

        if self.state == self.COUNTDOWN:
            self.countdown_timer -= delta_time
            if self.countdown_timer <= 0:
                self.state = self.PLAYING
                self.last_tick = pygame.time.get_ticks() # Reset for game timer
        elif self.state == self.PLAYING:
            self.time_left -= delta_time
            self.current_target_spawn_time += delta_time

            if self.current_target_spawn_time >= self.target_spawn_timer:
                self.current_target_spawn_time = 0
                self._spawn_target()

            if self.time_left <= 0:
                self.state = self.GAME_OVER
                self.time_left = 0 # Ensure it doesn't go negative

            self.targets.update()

        elif self.state == self.GAME_OVER:
            pass # No continuous update needed, waits for button press

    def _spawn_target(self):
        # Create a new target and add it to the group
        target = Target.create_random(20, 50, 10, 30) # min_radius, max_radius, min_score, max_score
        self.targets.add(target)


    def draw(self, screen):
        screen.fill(BLACK) # Clear screen

        if self.state == self.COUNTDOWN:
            countdown_text = self.font.render(f"시작까지: {int(self.countdown_timer) + 1}", True, WHITE)
            countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(countdown_text, countdown_rect)
        elif self.state == self.PLAYING:
            # Draw targets
            self.targets.draw(screen)

            # Draw HUD (Score and Time)
            score_text = self.font.render(f"점수: {self.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            time_text = self.font.render(f"시간: {int(self.time_left)}", True, WHITE)
            screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))

            # Draw crosshair
            pygame.draw.line(screen, RED, (pygame.mouse.get_pos()[0] - 10, pygame.mouse.get_pos()[1]), (pygame.mouse.get_pos()[0] + 10, pygame.mouse.get_pos()[1]), 2)
            pygame.draw.line(screen, RED, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 10), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 10), 2)
        elif self.state == self.GAME_OVER:
            game_over_text = self.font.render("게임 오버!", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            screen.blit(game_over_text, game_over_rect)

            final_score_text = self.font.render(f"최종 점수: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + FONT_SIZE))
            screen.blit(final_score_text, final_score_rect)

            for button in self.game_over_buttons:
                button.draw(screen)
