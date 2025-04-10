import pygame
from constants import WORLD_HEIGHT, WORLD_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH
from utils.rendering import CAMERA
from abc import abstractmethod

class World:
    def __init__(self, width=WORLD_WIDTH, height=WORLD_HEIGHT, color=(35, 35, 35)):
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        # vertical lines
        for i in range(int(self.width) + 1):
            start = pygame.Vector2(CAMERA.world_to_screen(i, 0))
            end = pygame.Vector2(CAMERA.world_to_screen(i, self.height))
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)

        # horizontal lines
        for i in range(int(self.height) + 1):
            start = pygame.Vector2(CAMERA.world_to_screen(0, i))
            end = pygame.Vector2(CAMERA.world_to_screen(self.width, i))
            pygame.draw.line(screen, self.color, start_pos=start, end_pos=end)

class GameObject:
    def __init__(self, mass, position, velocity, acceleration, force) -> None:
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.force  = force
    
    @abstractmethod
    def move(self, dt, a):
        raise NotImplementedError
    
    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError

class Circle(GameObject):
    air_drag_coef = 1e-4

    def __init__(
        self,
        mass, position, velocity, acceleration=pygame.Vector2(0,0), force=pygame.Vector2(0,0),
        radius=0.1,  # 10 cm
        draw_history: bool = False,
        fixed: bool = False,
        collide: bool = True,
        color=(255, 255, 255),
    ):
        super().__init__(mass, position, velocity, acceleration, force)
        self.pos_history = []
        self.fixed = fixed  # if object is affected by outside forces
        self.collide = collide  # if object should collide with walls

        self.radius = radius
        self.color = color

        self.draw_history = draw_history

    def move(self, dt, a):
        if not self.fixed:
            self.velocity[0] = self.velocity[0] + a[0] * dt
            self.velocity[1] = self.velocity[1] + a[1] * dt

            self.position[0] = self.position[0] + self.velocity[0] * dt
            self.position[1] = self.position[1] + self.velocity[1] * dt

            if self.collide:
                # Collision detection with ground
                if self.position[1] + self.radius > WORLD_HEIGHT:
                    self.position[1] = min(
                        WORLD_HEIGHT - self.radius,
                        WORLD_HEIGHT - abs(WORLD_HEIGHT - self.position[1]),
                    )
                    self.velocity[1] = -self.velocity[1]

                # Collision detection with walls
                # right wall
                if self.position[0] + self.radius > WORLD_WIDTH:
                    self.position[0] = WORLD_WIDTH - abs(WORLD_WIDTH - self.position[0])
                    self.velocity[0] = -self.velocity[0]

                # left wall
                if self.position[0] - self.radius < 0:
                    self.position[0] = abs(self.position[0])
                    self.velocity[0] = -self.velocity[0]

            if self.draw_history:
                self.pos_history.append((self.position[0], self.position[1]))

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            CAMERA.world_to_screen(self.position[0], self.position[1]),
            self.radius * CAMERA.scaling_factor,
        )

        if self.draw_history:
            # if len(self.pos_history) > 1:
            #     pygame.draw.lines(
            #         screen, (255, 255, 255), closed=False, points=self.pos_history
            #     )
            raise NotImplementedError()

    def get_attatched_springs(self, springs):
        res = [i for i in springs if (i.obj1 == self) or (i.obj2 == self)]
        assert len(set(res)) == len(res)
        return res


class Spring:
    def __init__(
        self,
        obj1: Circle,
        obj2: Circle,
        l: float = 1,
        D: float = 1000,
    ):
        self.D = D  # spring-constant D
        self.l = l  # length of spring in rest

        self.obj1 = obj1
        self.obj2 = obj2

    @property
    def current_l(self):
        return self.obj1.position.distance_to(self.obj2.position)

    @property
    def delta_l(self):
        return self.current_l - self.l

    def get_neighbour_obj(self, obj: Circle) -> Circle:
        assert obj in [self.obj1, self.obj2]
        if obj == self.obj1:
            return self.obj2
        elif obj == self.obj2:
            return self.obj1
        else:
            raise ValueError("No neighbour found for given obj")

    def draw(self, screen):
        pygame.draw.line(
            screen,
            "red",
            CAMERA.world_to_screen(self.obj1.position[0], self.obj1.position[1]),
            CAMERA.world_to_screen(self.obj2.position[0], self.obj2.position[1]),
            width=1,
        )
