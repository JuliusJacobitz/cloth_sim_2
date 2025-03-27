from constants import INITIAL_SCALING_FACTOR
import pygame


class Scaler:
    def __init__(self, scaling_factor=INITIAL_SCALING_FACTOR):
        self.scaling_factor = scaling_factor

    def world_to_screen(self, x):
        return x * self.scaling_factor

    def screen_to_world(self, x):
        return x / self.scaling_factor


class Background:
    def __init__(self, color=(35, 35, 35)):
        self.color = color

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        world_width = SCALER.screen_to_world(screen_width)
        world_height = SCALER.screen_to_world(screen_height)

        # vertical lines
        for i in range(int(world_width) + 1):
            start = pygame.Vector2(SCALER.world_to_screen(i), 0)
            end = pygame.Vector2(SCALER.world_to_screen(i), screen_height)
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)

        # horizontal lines
        for i in range(int(world_height) + 1):
            start = pygame.Vector2(0, SCALER.world_to_screen(i))
            end = pygame.Vector2(screen_width, SCALER.world_to_screen(i))
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)


SCALER = Scaler()
