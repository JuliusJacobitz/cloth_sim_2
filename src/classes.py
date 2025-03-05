import pygame
from constants import DRAG, HEIGHT, WIDTH

class Circle:
    def __init__(
        self, pos, vel, mass, radius=10, draw_history: bool = True, fixed: bool = False, collide:bool=True
    ):
        self.pos = pos  # meters
        self.pos_history = []
        self.vel = vel  # m/s
        self.mass = mass  # kg

        self.fixed = fixed  # if object is affected by outside forces
        self.collide = collide # if object should collide with walls

        self.radius = radius
        self.color = (255, 255, 255)

        self.draw_history = draw_history

    def move(self, dt, a):
        if not self.fixed:
            self.vel[0] = self.vel[0] + a[0] * dt
            self.vel[1] = self.vel[1] + a[1] * dt

            if DRAG:
                self.vel = self.vel - (DRAG * self.vel)

            self.pos[0] = self.pos[0] + self.vel[0] * dt
            self.pos[1] = self.pos[1] + self.vel[1] * dt

            if self.collide:
                # Collision detection with ground
                if self.pos[1] + self.radius > HEIGHT:
                    self.pos[1] = HEIGHT-self.radius

                # Collision detection with walls
                # right wall
                if self.pos[0] > WIDTH:
                    self.pos[0] = WIDTH - abs(WIDTH-self.pos[0])
                    self.vel[0] = -self.vel[0]

                # left wall
                if self.pos[0] < 0:
                    self.pos[0] = abs(self.pos[0])
                    self.vel[0] = -self.vel[0]

            if self.draw_history:
                self.pos_history.append((self.pos[0], self.pos[1]))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), self.radius)

        if self.draw_history:
            if len(self.pos_history) > 1:
                pygame.draw.lines(
                    screen, (255, 255, 255), closed=False, points=self.pos_history
                )

    def get_attatched_springs(self, springs):
        return [i for i in springs if (i.obj1 == self) or (i.obj2 == self)]


class Spring:
    def __init__(
        self,
        obj1: Circle,
        obj2: Circle,
        l: float = 100,
        D: float = 1,
    ):
        self.D = D  # spring-constant D
        self.l = l  # length of spring in rest

        self.obj1 = obj1
        self.obj2 = obj2

    @property
    def current_l(self):
        return self.obj1.pos.distance_to(self.obj2.pos)

    @property
    def delta_l(self):
        return self.current_l - self.l

    def get_neighbour_obj(self, obj: Circle):
        assert obj in [self.obj1, self.obj2]
        if obj == self.obj1:
            return self.obj2
        elif obj == self.obj2:
            return self.obj1
        else:
            raise ValueError("No neighbour found for given obj")

    def draw(self, screen):
        pygame.draw.line(screen, "red", self.obj1.pos, self.obj2.pos, width=2)

