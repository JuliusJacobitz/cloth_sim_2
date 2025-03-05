import pygame
import sys
from utils.calculations import calc_acc
from utils.fps import display_fps
from utils.misc import create_fonts


pygame.init()

# pygame constants
size = WIDTH, HEIGHT = 1000, 1000
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
TARGET_FPS = 60

fonts = create_fonts([32, 16, 14, 8])

dt = 0
# gravity acceleration constants
SCALER = 1
g = 9.81  # m/s^2
drag = 0.1  # %


class Circle:
    def __init__(self, pos, vel, mass, radius=10, draw_history: bool = True):
        self.pos = pos  # meters
        self.pos_history = []
        self.vel = vel  # m/s
        self.mass = mass  # kg

        self.radius = radius
        self.color = (255, 255, 255)

        self.draw_history = draw_history

    def move(self, dt, a):
        a = a * SCALER
        self.vel[0] = self.vel[0] + a[0] * dt
        self.vel[1] = self.vel[1] + a[1] * dt

        self.pos[0] = self.pos[0] + self.vel[0] * dt
        self.pos[1] = self.pos[1] + self.vel[1] * dt

        # # Collision detection with ground
        # if self.pos[1] + self.radius > HEIGHT:
        #     self.pos[1] = HEIGHT-self.radius
        #     self.vel[1] = -self.vel[1] * (1-drag)

        # # Collision detection with walls
        # if self.pos[0] > WIDTH:
        #     self.pos[0] = WIDTH - abs(WIDTH-self.pos[0])
        #     self.vel[0] = -self.vel[0]

        # if self.pos[0] < 0:
        #     self.pos[0] = abs(self.pos[0])
        #     self.vel[0] = -self.vel[0]

        if self.draw_history:
            self.pos_history.append((self.pos[0], self.pos[1]))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), self.radius)

        if self.draw_history:
            if len(self.pos_history) > 1:
                pygame.draw.lines(
                    screen, (255, 255, 255), closed=False, points=self.pos_history
                )


c1 = Circle(
    pygame.Vector2(500, 500), vel=pygame.Vector2(0, 0), mass=1e15
)  # mass=5.972e24) # earth
c2 = Circle(
    pygame.Vector2(400, 300), vel=pygame.Vector2(200, 0), mass=1e11
)  # mass=7.34767309e22) # moon
c3 = Circle(pygame.Vector2(500, 800), vel=pygame.Vector2(-200, 0), mass=1e11, radius=10)
# c4 = Circle(pygame.Vector2(500, 200), vel=pygame.Vector2(90, 0), mass=1e14, radius=20)

objects = [c1, c2, c3]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    accelerations = calc_acc(objects=objects)
    for i, obj in enumerate(objects):
        obj.move(dt=dt, a=accelerations[i])
        obj.draw(screen)

    display_fps(fonts=fonts, clock=clock, screen=screen)

    pygame.display.flip()
    dt = clock.tick(TARGET_FPS) / 1000
