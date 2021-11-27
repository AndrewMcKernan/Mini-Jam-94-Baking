import pygame
from enum import Enum


class UnitType(Enum):
    EGG = 1


class Unit(pygame.sprite.Sprite):
    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        if not isinstance(unit_type, UnitType):
            raise TypeError("Unit Type must be set to a UnitType enum.")
        self.unitType = unit_type


# not sure if these two classes are really needed.
class AlliedUnit(Unit):
    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False


class HostileUnit(Unit):
    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
