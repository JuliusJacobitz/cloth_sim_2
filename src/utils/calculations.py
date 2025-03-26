from scipy.constants import G, g

import pygame
from typing import List
import math
from classes import Circle

def calc_grav_force(obj1, obj2) -> float:
    F = G * (obj1.mass * obj2.mass) / obj1.pos.distance_to(obj2.pos)
    return F


def calc_acc(
    objects:List[Circle],
    springs,
    add_earth_gravity: bool = True,
    pairwise_grav_forces: bool = False,
    air_drag: bool = True,
):
    """
    For each object calculate its accelerations and return it as a list.
    """
    # calculate acc forces for each object
    accelerations = []
    for obj1 in objects:
        new_acc = pygame.Vector2(0, 0)

        # calculate gravitational force between all objects
        if pairwise_grav_forces:
            for obj2 in objects:
                if obj2 == obj1:
                    continue
                else:
                    f = calc_grav_force(obj1, obj2)
                    direction = (obj2.pos - obj1.pos).normalize()
                    new_acc = new_acc + ((direction * f) / obj1.mass)

        # calculate spring forces based on hooke's law
        for spring in obj1.get_attatched_springs(springs):
            obj2 = spring.get_neighbour_obj(obj1)

            # f = spring.D * spring.delta_l
            direction = (obj2.pos - obj1.pos).normalize()

            # dampening
            dampening_coeff:float = 2*0.1*math.sqrt(spring.D*obj1.mass)
            relative_vel:float = (obj2.vel - obj1.vel ) * direction

            f_spring = spring.D * spring.delta_l
            f_dampening = dampening_coeff*relative_vel
            f_total = (f_spring+f_dampening) * direction
            
            new_acc = new_acc + f_total/obj1.mass

        # earth gravity acceleration
        if add_earth_gravity:
            new_acc = new_acc + pygame.Vector2([0, 9.81])

        # air drag
        if air_drag and hasattr(obj1, "air_drag_coef"):
            f = -obj1.air_drag_coef * obj1.vel
            new_acc = new_acc + (f / obj1.mass)

        accelerations.append(new_acc)

    return accelerations
