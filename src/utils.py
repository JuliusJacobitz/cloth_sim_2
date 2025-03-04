from scipy.constants import G
import pygame

def calc_acc_force(circle1, circle2) -> float:
    F = G * (circle1.mass * circle2.mass) / circle1.pos.distance_to(circle2.pos)
    return F


def calc_acc(objects):
    accelerations = []
    for index in range(len(objects)):
        acc = pygame.Vector2(0, 0)
        c1 = objects[index]
        for i, c2 in enumerate(objects):
            if i == index:
                continue
            else:
                f = calc_acc_force(c1, c2)
                dir_c1_c2 = (c2.pos - c1.pos).normalize()
                acc = acc + dir_c1_c2 * f

        acc = acc/c1.mass

        accelerations.append(acc)

    return accelerations