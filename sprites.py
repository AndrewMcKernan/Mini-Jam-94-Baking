import pygame
from enum import Enum


class UnitType(Enum):
    EGG = 1


class MouseSprite(pygame.sprite.Sprite):
    def __init__(self, position_tuple):
        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.rect = pygame.rect.Rect(position_tuple, (1, 1))

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

        if unit_type == UnitType.EGG:
            self.hp = 5
            self.max_hp = 5
            self.movement = 5
        else:
            # this should never happen
            self.hp = 1
            self.max_hp = 1
            self.movement = 0


# not sure if these two classes are really needed.
class AlliedUnit(Unit):
    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False


class HostileUnit(Unit):
    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
