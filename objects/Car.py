import pygame
import math

from util import load_image


class Car:
    x_vel: float = 0
    y_vel: float = 0
    original_img: pygame.Surface
    img: pygame.Surface
    rect: pygame.Rect
    angle = 0
    thrust = 0.5

    def __init__(self, start_x: int, start_y: int) -> None:
        self.original_img = load_image("assets/images/characters/octane.png", 64, 64)
        self.img = self.original_img.copy()
        self.rect = self.img.get_rect()
        self.rect.center = (start_x, start_y)

    def calculate_physics(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT]:
            self.rotate("left")
        if keys_pressed[pygame.K_RIGHT]:
            self.rotate("right")
        if keys_pressed[pygame.K_UP]:
            self.go("forward")
        if keys_pressed[pygame.K_DOWN]:
            self.go("backward")

    def rotate(self, dir: str):
        speed = math.sqrt(self.x_vel**2 + self.y_vel**2)
        angular_velocity = 2.5 - (speed / 40)
        if dir == "left":
            self.angle += angular_velocity
        elif dir == "right":
            self.angle -= angular_velocity

        self.img = pygame.transform.rotate(self.original_img, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)

    def go(self, dir: str):
        dir_num = -1
        if dir == "forward":
            dir_num = 1
        angle_rad = math.radians(self.angle)
        self.x_vel += math.cos(angle_rad) * dir_num * self.thrust
        self.y_vel += math.sin(angle_rad) * dir_num * self.thrust

    def move(self):
        angle_rad = math.radians(self.angle)
        speed = math.sqrt(self.x_vel**2 + self.y_vel**2)
        self.x_vel = math.cos(angle_rad) * speed
        self.y_vel = math.sin(angle_rad) * speed
        self.rect.x += int(self.x_vel)
        self.rect.y -= int(self.y_vel)

    def update(self, keys_pressed):
        self.calculate_physics(keys_pressed)
        self.move()
