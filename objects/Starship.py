import pygame
import math

from util import load_image

class Starship:
  x_vel = 0
  y_vel = 0
  original_img: pygame.Surface
  img: pygame.Surface
  rect: pygame.Rect
  angle = 0
  thrust = 0.5

  def __init__(self, start_x: int, start_y: int) -> None:
      self.original_img = load_image('assets/images/characters/octane.png', 64, 64)
      self.img = self.original_img.copy()
      self.rect = self.img.get_rect()
      self.rect.center = (start_x, start_y)

  def rotate(self, dir: str):
      if dir == 'left':
          self.angle += 5
      elif dir == 'right':
          self.angle -= 5

      self.img = pygame.transform.rotate(self.original_img, self.angle)
      self.rect = self.img.get_rect(center=self.rect.center)

  def go(self, dir: str):
      dir_num = -1
      if dir == 'forward':
          dir_num = 1
      angle_rad = math.radians(self.angle)
      self.x_vel += math.cos(angle_rad) * dir_num * self.thrust
      self.y_vel -= math.sin(angle_rad) * dir_num * self.thrust

  def move(self):
      self.rect.x += int(self.x_vel)
      self.rect.y += int(self.y_vel)