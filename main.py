from enum import Enum, auto
from functools import lru_cache

import pygame
from pygame import Vector2
from pygame.locals import (
    K_q,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_DIMS = Vector2(800, 600)


class Triangle:
    class IntersectionMethods(Enum):
        HERON = auto()
        PROJECTION = auto()

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.intersection_methods = {
            self.IntersectionMethods.HERON: self._intersects_heron,
            self.IntersectionMethods.PROJECTION: self._intersects_projection,
        }

    @property
    def area(self):
        a_len = self.a.distance_to(self.b)
        b_len = self.b.distance_to(self.c)
        c_len = self.c.distance_to(self.a)
        s = (a_len + b_len + c_len) / 2
        pa = (s * (s - a_len) * (s - b_len) * (s - c_len))
        return max(pa, 0.001) ** 0.5

    def _intersects_heron(self, point):
        return self.area < (
            Triangle(self.a, self.b, point).area +
            Triangle(self.b, self.c, point).area +
            Triangle(self.c, self.a, point).area
        ) - 0.01

    def _intersects_projection(self, point):
        ab = self.b - self.a
        bc = self.c - self.b
        ca = self.a - self.c
        ab = ab.rotate(90)
        bc = bc.rotate(90)
        ca = ca.rotate(90)
        ap = point - self.a
        bp = point - self.b
        cp = point - self.c
        return all([
            ab.dot(ap) >= 0,
            bc.dot(bp) >= 0,
            ca.dot(cp) >= 0,
        ])

    def intersects(self, point, method):
        return self.intersection_methods[method](point)

    def draw(self, surface, color):
        pygame.draw.polygon(surface, color, (self.a, self.b, self.c))

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMS)
    pygame.display.set_caption("Triangle")
    tri = Triangle(
        a=Vector2(SCREEN_DIMS.x/2, SCREEN_DIMS.y/3), 
        b=Vector2(SCREEN_DIMS.x/3, SCREEN_DIMS.y/3*2), 
        c=Vector2(SCREEN_DIMS.x/3*2, SCREEN_DIMS.y/3*2))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [K_ESCAPE, K_q]:
                running = False
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0,0,0))
        mouse_inside = tri.intersects(Vector2(pygame.mouse.get_pos()), Triangle.IntersectionMethods.HERON)
        color = (0, 255, 0) if mouse_inside else (255, 0, 0)
        tri.draw(screen, color)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()