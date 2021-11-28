import pygame
from enum import Enum
from constants import TILE_WIDTH, TILE_HEIGHT


class UnitType(Enum):
    EGG = 1
    GOOP = 2

class MenuItem(pygame.sprite.Sprite):
    def __init__(self, rect, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = rect
        self.name = name

    def __str__(self):
        return self.name + " " + str(self.rect.x) + "," + str(self.rect.y) + " - " + str(self.rect.width) + ',' + str(self.rect.height)

class Terrain(pygame.sprite.Sprite):
    def __init__(self, image, width, height, start_x=0, start_y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y


class MouseSprite(pygame.sprite.Sprite):
    def __init__(self, xy_position_tuple):
        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.rect = pygame.rect.Rect(xy_position_tuple, (1, 1))

class Unit(pygame.sprite.Sprite):

    def wait(self, target):
        return True

    def get_action_range(self, action_name):
        if action_name == "Wait":
            return 0

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        if not isinstance(unit_type, UnitType):
            raise TypeError("Unit Type must be set to a UnitType enum.")
        self.unitType = unit_type
        self.actions = dict()
        self.actions['Wait'] = self.wait

    def get_grid_coordinates(self):
        return self.rect.x // TILE_WIDTH, self.rect.y // TILE_HEIGHT

    def move_to_grid_coordinates(self, coordinates):
        self.rect.x = coordinates[0] * TILE_WIDTH
        self.rect.y = coordinates[1] * TILE_HEIGHT


class EggSoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 1

    def attack(self, target):
        if not target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp < 0:
            target.kill()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False
        self.hp = 5
        self.max_hp = 5
        self.attack_value = 5
        self.movement = 5
        self.actions['Attack'] = self.attack


class GoopSoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 1

    def attack(self, target):
        if target.hostile:
            return False
        print("Before")
        print(target.hp)
        target.hp -= self.attack_value
        print("After")
        print(target.hp)
        if target.hp < 0:
            target.kill()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
        self.hp = 12
        self.max_hp = 12
        self.attack_value = 3
        self.movement = 2
        self.actions['Attack'] = self.attack


