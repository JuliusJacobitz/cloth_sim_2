import pygame
import sys
from utils.calculations import calc_acc
from utils.fps import display_fps
from utils.misc import create_fonts
from constants import size, TARGET_FPS
from classes import Spring, Circle

# pygame
pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fonts = create_fonts([32, 16, 14, 8])
dt = 0

# create elements
c1 = Circle(pygame.Vector2(500, 300), vel=pygame.Vector2(100, 0), mass=1e14, collide=False, fixed=False)
c2 = Circle(pygame.Vector2(500, 500), vel=pygame.Vector2(-100, 0), mass=1e14, collide=False, fixed=False)

objects = [c1, c2]
springs = []

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))

    accelerations = calc_acc(
        objects=objects,
        springs=springs,
        add_earth_gravity=False,
        pairwise_grav_forces=True,
    )
    for i, obj in enumerate(objects):
        obj.move(dt=dt, a=accelerations[i])
        obj.draw(screen)

    for spring in springs:
        spring.draw(screen)

    display_fps(fonts=fonts, clock=clock, screen=screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000
