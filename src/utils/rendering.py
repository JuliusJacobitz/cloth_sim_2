from constants import INITIAL_SCALING_FACTOR, INITIAL_CAM_POS
import pygame


class Camera:
    def __init__(self, scaling_factor=INITIAL_SCALING_FACTOR, pos=INITIAL_CAM_POS):
        self.scaling_factor = scaling_factor
        self.pos = pos

        self.movement_keys = {
            "down": pygame.K_DOWN,
            "up": pygame.K_UP,
            "right": pygame.K_RIGHT,
            "left": pygame.K_LEFT,
            "z_out": pygame.K_o,
            "z_in": pygame.K_p,
        }

    def world_to_screen(self, x, y, offset=True):
        if offset:
            x = x - self.pos[0]
            y = y - self.pos[1]
        x = x * self.scaling_factor
        y = y * self.scaling_factor
        return (x, y)

    def screen_to_world(self, x, y, offset=True):
        x = x / self.scaling_factor
        y = y / self.scaling_factor
        if offset:
            x += self.pos[0]
            y += self.pos[1]
        return (x, y)

    def move(self, key):
        # scaling
        if key == self.movement_keys["z_out"]:
            self.scaling_factor *= 0.90

        elif key == self.movement_keys["z_in"]:
            self.scaling_factor *= 1.10

        # movement
        elif key == self.movement_keys["up"]:
            self.pos += pygame.Vector2(0, -2.5)

        elif key == self.movement_keys["down"]:
            self.pos += pygame.Vector2(0, 2.5)

        elif key == self.movement_keys["left"]:
            self.pos += pygame.Vector2(-2.5, 0)

        elif key == self.movement_keys["right"]:
            self.pos += pygame.Vector2(2.5, 0)


CAMERA = Camera()
