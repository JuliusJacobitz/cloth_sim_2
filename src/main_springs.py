import pygame
import sys
from utils.calculations import calc_acc
from utils.fps import display_fps
from utils.misc import create_fonts
from constants import size, TARGET_FPS
from classes import Spring, Circle
from utils.rendering import Background

# pygame
pygame.init()
screen = pygame.display.set_mode(size)
background = Background()
clock = pygame.time.Clock()
fonts = create_fonts([32, 16, 14, 8])
dt = 0

# create elements
c1 = Circle(
    pygame.Vector2(3, 3),
    vel=pygame.Vector2(200, 0),
    mass=1,
    draw_history=False,
    fixed=False,
)
c2 = Circle(
    pygame.Vector2(4, 4),
    vel=pygame.Vector2(0, 100),
    mass=1,
    draw_history=False,
    fixed=False,
)
c3 = Circle(
    pygame.Vector2(3, 4),
    vel=pygame.Vector2(0, 0),
    mass=1,
    draw_history=False,
    fixed=False,
)
c4 = Circle(
    pygame.Vector2(4, 3),
    vel=pygame.Vector2(0, 0),
    mass=1,
    draw_history=False,
    fixed=False,
)
objects = [c1, c2, c3, c4]

s_c1_c2 = Spring(c1, c2)
s_c1_c3 = Spring(c1, c3)
s_c1_c4 = Spring(c1, c4)
s_c2_c3 = Spring(c2, c3)
s_c2_c4 = Spring(c2, c4)
s_c3_c4 = Spring(c3, c4)
springs = [s_c1_c2, s_c1_c3, s_c1_c4, s_c2_c3, s_c2_c4, s_c3_c4]


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))

    background.draw(screen)

    accelerations = calc_acc(
        objects=objects,
        springs=springs,
        add_earth_gravity=True,
        pairwise_grav_forces=False,
    )
    for i, obj in enumerate(objects):
        obj.move(dt=dt, a=accelerations[i])
        obj.draw(screen)

    for spring in springs:
        spring.draw(screen)

    display_fps(fonts=fonts, clock=clock, screen=screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000
