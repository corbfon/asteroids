import math

import pygame


class Projectile:
    x_vel: float
    y_vel: float
    speed = 8
    rect: pygame.Rect

    def __init__(self, start_x: int, start_y: int, angle: int) -> None:
        angle_rad = math.radians(angle)

        self.x_vel = math.sin(angle_rad) * -1 * self.speed
        self.y_vel = math.cos(angle_rad) * -1 * self.speed
        self.rect = pygame.Rect(start_x, start_y, 4, 4)

    def move(self):
        self.rect.x += int(self.x_vel)
        self.rect.y += int(self.y_vel)
