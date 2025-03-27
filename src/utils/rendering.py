from constants import SCALING_FACTOR


def world_to_screen(x):
    return x*SCALING_FACTOR


def screen_to_world(x):
    return x/SCALING_FACTOR
