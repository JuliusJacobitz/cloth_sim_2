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
c1 = Circle(
    pygame.Vector2(500, 400), vel=pygame.Vector2(0, 0), mass=1e1, draw_history=False
)
c2 = Circle(pygame.Vector2(400, 500), vel=pygame.Vector2(0, 0), mass=1e1, fixed=True)
c3 = Circle(pygame.Vector2(600, 500), vel=pygame.Vector2(0, 0), mass=1e1, fixed=True)
c4 = Circle(pygame.Vector2(30, 40), vel=pygame.Vector2(0, 0), mass=1e1, fixed=True)
c5 = Circle(pygame.Vector2(100, 40), vel=pygame.Vector2(0, 0), mass=1e1, fixed=False)
objects = [c1, c2, c3, c4, c5]

s_c1_c2 = Spring(c1, c2)
s_c1_c3 = Spring(c1, c3)
s1_c4_c5 = Spring(c4, c5, l=50)
springs = [s_c1_c2, s_c1_c3, s1_c4_c5]

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0,0,0))

    accelerations = calc_acc(objects=objects, springs=springs,add_earth_gravity=True)
    for i, obj in enumerate(objects):
        obj.move(dt=dt, a=accelerations[i])
        obj.draw(screen)

    for spring in springs:
        spring.draw(screen)

    display_fps(fonts=fonts, clock=clock, screen=screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000
