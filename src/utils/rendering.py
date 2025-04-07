from constants import INITIAL_SCALING_FACTOR, INITIAL_CAM_POS
import pygame


class Camera:
    def __init__(self, scaling_factor=INITIAL_SCALING_FACTOR, pos=INITIAL_CAM_POS):
        self.scaling_factor = scaling_factor
        self.pos = pos

        self.movement_keys = (
            pygame.K_DOWN,
            pygame.K_UP,
            pygame.K_RIGHT,
            pygame.K_LEFT,
            pygame.K_o,
            pygame.K_p,
        )

    def world_to_screen(self, x, y, offset=True):
        if offset:
            x = x - self.pos[0]
            y = y - self.pos[1]
        x = x * self.scaling_factor
        y = y * self.scaling_factor
        return (x, y)

    def screen_to_world(self, x, y, offset=True):
        x = (x / self.scaling_factor) + self.pos[0]
        y = (y / self.scaling_factor) + self.pos[1]
        return (x, y)

    def move(self, key):
        # scaling
        if key == pygame.K_o:
            self.scaling_factor *= 0.90

        elif key == pygame.K_p:
            self.scaling_factor *= 1.10

        # movement
        elif key == pygame.K_UP:
            self.pos += pygame.Vector2(0, -2.5)

        elif key == pygame.K_DOWN:
            self.pos += pygame.Vector2(0, 2.5)

        elif key == pygame.K_LEFT:
            self.pos += pygame.Vector2(-2.5, 0)

        elif key == pygame.K_RIGHT:
            self.pos += pygame.Vector2(2.5, 0)


CAMERA = Camera()
