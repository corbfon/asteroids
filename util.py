import sys

import pygame
from pygame.locals import QUIT


def load_image(path: str, width: int, height: int):
  surf = pygame.image.load(path).convert_alpha()
  surf = pygame.transform.scale(surf, (width, height))
  surf_mask = pygame.mask.from_surface(surf)
  surf_bounding_rects: list[pygame.Rect] = surf_mask.get_bounding_rects() # type: ignore
  if len(surf_bounding_rects) > 0:
      return surf.subsurface(surf_bounding_rects[0])
  else:
      return surf

def detect_events(events) -> list[pygame.event.Event]:
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    return events