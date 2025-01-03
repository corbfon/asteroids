import pygame
from random import randint, random

from util import load_image

class Asteroid:
  color = 'blue'
  x_vel = 0
  y_vel = 0
  img: pygame.Surface

  def __init__(self, file_path: str, min_x, min_y, max_x, max_y) -> None:
      self.x_vel = randint(1, 4)
      self.y_vel = randint(1, 4)
      x_dir = random()
      y_dir = random()
      if x_dir < 0.5:
          self.x_vel *= -1
      if y_dir < 0.5:
          self.y_vel *= -1
      self.img = load_image(file_path, 64, 64)
      self.rect = self.img.get_rect()
      self.rect.x = randint(min_x, max_x)
      self.rect.y = randint(min_y, max_y)

  def move(self):
      self.rect.x += self.x_vel
      self.rect.y += self.y_vel