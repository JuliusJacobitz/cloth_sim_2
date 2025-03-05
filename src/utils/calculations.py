from scipy.constants import G, g

import pygame


def calc_grav_force(obj1, obj2) -> float:
    F = G * (obj1.mass * obj2.mass) / obj1.pos.distance_to(obj2.pos)
    return F


def calc_acc(
    objects, springs, add_earth_gravity: bool = True, pairwise_grav_forces: bool = False
):
    # calculate acc forces based on gravity between objects
    accelerations = []
    for index in range(len(objects)):
        acc = pygame.Vector2(0, 0)
        obj1 = objects[index]

        # calculate gravitational force between all objects
        if pairwise_grav_forces:
            for i, obj2 in enumerate(objects):
                if i == index:
                    continue
                else:
                    f = calc_grav_force(obj1, obj2)
                    direction = (obj2.pos - obj1.pos).normalize()
                    acc = acc + direction * f

        # calculate spring forces
        for i, spring in enumerate(obj1.get_attatched_springs(springs)):
            f = spring.D * spring.delta_l
            direction = (spring.get_neighbour_obj(obj1).pos - obj1.pos).normalize()
            acc = acc + direction * f

        acc = acc / obj1.mass

        # add earth gravity acceleration
        if add_earth_gravity:
            acc += pygame.Vector2([0, g])

        accelerations.append(acc)

    return accelerations
