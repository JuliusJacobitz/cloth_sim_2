from scipy.constants import G, g

import pygame


def calc_grav_force(obj1, obj2) -> float:
    F = G * (obj1.mass * obj2.mass) / obj1.pos.distance_to(obj2.pos)
    return F


def calc_acc(
    objects, springs, add_earth_gravity: bool = True, pairwise_grav_forces: bool = False
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
                    new_acc += (direction * f) / obj1.mass

        # calculate spring forces
        for spring in obj1.get_attatched_springs(springs):
            f = spring.D * spring.delta_l
            direction = (spring.get_neighbour_obj(obj1).pos - obj1.pos).normalize()
            new_acc += (direction * f) / obj1.mass

        # add earth gravity acceleration
        if add_earth_gravity:
            new_acc += pygame.Vector2([0, g])

        accelerations.append(new_acc)

    return accelerations
