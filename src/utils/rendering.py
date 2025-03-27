from constants import SCALING_FACTOR
import pygame


def world_to_screen(x):
    return x * SCALING_FACTOR


def screen_to_world(x):
    return x / SCALING_FACTOR


class Background:
    def __init__(self, color=(35, 35, 35)):
        self.color = color

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()
        world_width = screen_to_world(screen_width)
        world_height = screen_to_world(screen_height)

        # vertical lines
        for i in range(int(world_width) + 1):
            start = pygame.Vector2(world_to_screen(i), 0)
            end = pygame.Vector2(world_to_screen(i), screen_height)
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)

        # horizontal lines
        for i in range(int(world_height) + 1):
            start = pygame.Vector2(0, world_to_screen(i))
            end = pygame.Vector2(screen_width, world_to_screen(i))
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)
