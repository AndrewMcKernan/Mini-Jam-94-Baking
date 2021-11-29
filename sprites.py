import pygame
import os
from enum import Enum
from constants import TILE_WIDTH, TILE_HEIGHT


class UnitType(Enum):
    EGG = 1
    GOOP = 2
    SUGAR = 3
    OIL = 4
    BAD_APPLE = 5
    FLY = 6


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, rect, name, description):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1))
        self.rect = rect
        self.name = name
        self.description = description

    def __str__(self):
        return self.name + " " + str(self.rect.x) + "," + str(self.rect.y) + " - " + str(self.rect.width) + ',' + str(
            self.rect.height)


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
        sound = pygame.mixer.Sound(os.path.join('assets', 'wait.wav'))
        sound.set_volume(0.1)
        sound.play()
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
        self.damage = ""
        if not isinstance(unit_type, UnitType):
            raise TypeError("Unit Type must be set to a UnitType enum.")
        self.unitType = unit_type
        self.actions = dict()
        self.actions['Wait'] = (self.wait, "The unit ends its turn, performing no action.")

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
        if not isinstance(target, Unit) or not target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'egg-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False
        self.hp = 5
        self.max_hp = 5
        self.attack_value = 5
        self.movement = 5
        self.damage = "HIGH"
        self.actions['Attack'] = (
            self.attack, "Egg targets an adjacent enemy, dealing " + str(self.attack_value) + " damage.")


class SugarSoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 1
        if action_name == "Heal":
            return 1

    def attack(self, target):
        if not isinstance(target, Unit) or not target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'egg-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def heal(self, target):
        if not isinstance(target, Unit) or target.hostile:
            return False
        target.hp += self.heal_value
        if target.hp > target.max_hp:
            target.hp = target.max_hp

        sound = pygame.mixer.Sound(os.path.join('assets', 'heal.wav'))
        sound.set_volume(0.1)
        sound.play()

        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False
        self.hp = 9
        self.max_hp = 9
        self.attack_value = 1
        self.heal_value = 3
        self.damage = "LOW"
        self.movement = 3
        self.actions['Attack'] = (
            self.attack, "Sugar targets an adjacent enemy, dealing " + str(self.attack_value) + " damage.")
        self.actions['Heal'] = (
            self.heal, "Sugar targets an adjacent ally, healing them for " + str(self.heal_value) + " health.")


class OilSoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 3

    def attack(self, target):
        if not isinstance(target, Unit) or not target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'oil-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = False
        self.hp = 2
        self.max_hp = 2
        self.attack_value = 7
        self.movement = 3
        self.damage = "VERY HIGH"
        self.actions['Attack'] = (
            self.attack, "Oil targets an enemy within " + str(self.get_action_range("Attack")) + ", dealing " +
            str(self.attack_value) + " damage.")


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
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'enemy-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
        self.hp = 12
        self.max_hp = 12
        self.attack_value = 3
        self.damage = "LOW"
        self.movement = 2
        self.actions['Attack'] = (
            self.attack, "The Kitchen Goop targets an adjacent enemy, dealing " + str(self.attack_value) + "damage.")


class AppleSoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 1

    def attack(self, target):
        if target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'enemy-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
        self.hp = 1
        self.max_hp = 1
        self.attack_value = 6
        self.damage = "VERY HIGH"
        self.movement = 4
        self.actions['Attack'] = (
            self.attack, "The Bad Apple targets an adjacent enemy, dealing " + str(self.attack_value) + "damage.")


class FlySoldier(Unit):

    def get_action_range(self, action_name):
        result = Unit.get_action_range(self, action_name)
        if result is not None:
            return result
        if action_name == "Attack":
            return 1

    def attack(self, target):
        if target.hostile:
            return False
        target.hp -= self.attack_value
        if target.hp <= 0:
            target.kill()
        sound = pygame.mixer.Sound(os.path.join('assets', 'enemy-attack.wav'))
        sound.set_volume(0.1)
        sound.play()
        return True

    def __init__(self, image, width, height, unit_type, start_x=0, start_y=0):
        Unit.__init__(self, image, width, height, unit_type, start_x, start_y)
        self.hostile = True
        self.hp = 6
        self.max_hp = 6
        self.attack_value = 3
        self.movement = 7
        self.damage = "LOW"
        self.actions['Attack'] = (
            self.attack, "The Fly targets an adjacent enemy, dealing " + str(self.attack_value) + "damage.")