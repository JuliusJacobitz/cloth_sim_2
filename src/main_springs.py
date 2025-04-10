import pygame
import sys
from utils.calculations import calc_acc
from utils.fps import display_fps
from utils.misc import create_fonts
from constants import window_size, TARGET_FPS
from classes import Spring, Circle, World
from utils.rendering import CAMERA

# pygame
pygame.init()
screen = pygame.display.set_mode(window_size)
background = World()
clock = pygame.time.Clock()
fonts = create_fonts([32, 16, 14, 8])
dt = 0
attatched_to_mouse = None

# create elements
c1 = Circle(
    pygame.Vector2(3, 3),
    vel=pygame.Vector2(10, 0),
    mass=1,
    draw_history=False,
    fixed=False,
)
c2 = Circle(
    pygame.Vector2(0, 4),
    vel=pygame.Vector2(0, 0),
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

c_origin = Circle(
    pygame.Vector2(10, 10),
    vel=pygame.Vector2(0, 0),
    mass=1,
    fixed=True,
    color=(255, 0, 0),
)

objects = [c1, c2, c3, c4, c_origin]

s_c1_c2 = Spring(c1, c2)
s_c1_c3 = Spring(c1, c3)
s_c1_c4 = Spring(c1, c4)
s_c2_c3 = Spring(c2, c3)
s_c2_c4 = Spring(c2, c4)
s_c3_c4 = Spring(c3, c4)
springs = [s_c1_c2, s_c1_c3, s_c1_c4, s_c2_c3, s_c2_c4, s_c3_c4]


# game loop
while True:
    # inputs
    mouse_pos_screen = pygame.mouse.get_pos()
    mouse_pos_world = pygame.Vector2(CAMERA.screen_to_world(mouse_pos_screen[0], mouse_pos_screen[1]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in CAMERA.movement_keys.values():
                CAMERA.move(event.key)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # check which object overlays with mouse
            if not attatched_to_mouse:
                for obj in objects:
                    if mouse_pos_world.distance_squared_to(obj.pos) <= obj.radius:
                        attatched_to_mouse = obj
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            if attatched_to_mouse:
                attatched_to_mouse.fixed = False
            attatched_to_mouse = None

    screen.fill((0, 0, 0))

    background.draw(screen)

    # interaction
    if attatched_to_mouse:
        attatched_to_mouse.fixed = True
        attatched_to_mouse.pos = mouse_pos_world
        attatched_to_mouse.vel = pygame.Vector2(0,0)

    # rest
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
