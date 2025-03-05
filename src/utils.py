from scipy.constants import G
import pygame

def calc_acc_force(obj1, obj2) -> float:
    F = G * (obj1.mass * obj2.mass) / obj1.pos.distance_to(obj2.pos)
    return F


def calc_acc(objects):
    accelerations = []
    for index in range(len(objects)):
        acc = pygame.Vector2(0, 0)
        obj1 = objects[index]
        for i, obj2 in enumerate(objects):
            if i == index:
                continue
            else:
                f = calc_acc_force(obj1, obj2)
                dir_c1_c2 = (obj2.pos - obj1.pos).normalize()
                acc = acc + dir_c1_c2 * f

        acc = acc/obj1.mass

        accelerations.append(acc)

    return accelerations