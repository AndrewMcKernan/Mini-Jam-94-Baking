import os, sys
import pygame
import random
from constants import *
from draw_text import drawText
from sprites import *

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pygame.font.init()  # for writing text to the screen
pygame.mixer.init()  # for sound

pygame.display.set_caption("Mini Jam 94: Baking")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

ZOOMED_MAP = pygame.surface.Surface((ZOOMED_MAP_WIDTH, ZOOMED_MAP_HEIGHT))
camera = pygame.Rect((ZOOMED_MAP_WIDTH // 2 - WIDTH // 2 - 200, ZOOMED_MAP_HEIGHT // 2 - HEIGHT // 2 + 500), (WIDTH, HEIGHT))

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)
ZOOMED_BACKGROUND = pygame.Rect(0, 0, ZOOMED_MAP_WIDTH, ZOOMED_MAP_HEIGHT)


EGG_IMAGE = pygame.image.load(os.path.join('assets', 'egg.png')).convert()
EGG_IMAGE.set_colorkey(TRANSPARENT)

SUGAR_IMAGE = pygame.image.load(os.path.join('assets', 'sugar.png')).convert()
SUGAR_IMAGE.set_colorkey(TRANSPARENT)

OIL_IMAGE = pygame.image.load(os.path.join('assets', 'oil.png')).convert()
OIL_IMAGE.set_colorkey(TRANSPARENT)

GOOP_IMAGE = pygame.image.load(os.path.join('assets', 'goop.png')).convert()
GOOP_IMAGE.set_colorkey(TRANSPARENT)

APPLE_IMAGE = pygame.image.load(os.path.join('assets', 'bad_apple.png')).convert()
APPLE_IMAGE.set_colorkey(TRANSPARENT)

FLY_IMAGE = pygame.image.load(os.path.join('assets', 'fly.png')).convert()
FLY_IMAGE.set_colorkey(TRANSPARENT)

CAKE_IMAGE = pygame.image.load(os.path.join('assets', 'cake.png')).convert()
CAKE_IMAGE.set_colorkey(TRANSPARENT)

COOKIE_IMAGE = pygame.image.load(os.path.join('assets', 'cookie.png')).convert()
COOKIE_IMAGE.set_colorkey(TRANSPARENT)

MUFFIN_IMAGE = pygame.image.load(os.path.join('assets', 'muffin.png')).convert()
MUFFIN_IMAGE.set_colorkey(TRANSPARENT)

MOUSE_IMAGE = pygame.image.load(os.path.join('assets', 'mouse.png')).convert()
MOUSE_IMAGE.set_colorkey(TRANSPARENT)

VICTORY_IMAGE = pygame.image.load(os.path.join('assets', 'victory.png')).convert()
VICTORY_IMAGE.set_colorkey(TRANSPARENT)

VICTORY_IMAGE_SHADOW = pygame.image.load(os.path.join('assets', 'victory_shadow.png')).convert()
VICTORY_IMAGE_SHADOW.set_colorkey(TRANSPARENT)

DEFEAT_IMAGE = pygame.image.load(os.path.join('assets', 'defeat.png')).convert()
DEFEAT_IMAGE.set_colorkey(TRANSPARENT)

DEFEAT_IMAGE_SHADOW = pygame.image.load(os.path.join('assets', 'defeat_shadow.png')).convert()
DEFEAT_IMAGE_SHADOW.set_colorkey(TRANSPARENT)

PLAYER_PHASE_IMAGE = pygame.image.load(os.path.join('assets', 'player_turn.png')).convert()
PLAYER_PHASE_IMAGE.set_colorkey(TRANSPARENT)

PLAYER_PHASE_IMAGE_SHADOW = pygame.image.load(os.path.join('assets', 'player_turn_shadow.png')).convert()
PLAYER_PHASE_IMAGE_SHADOW.set_colorkey(TRANSPARENT)

ENEMY_PHASE_IMAGE = pygame.image.load(os.path.join('assets', 'enemy_turn.png')).convert()
ENEMY_PHASE_IMAGE.set_colorkey(TRANSPARENT)

ENEMY_PHASE_IMAGE_SHADOW = pygame.image.load(os.path.join('assets', 'enemy_turn_shadow.png')).convert()
ENEMY_PHASE_IMAGE_SHADOW.set_colorkey(TRANSPARENT)

WATER_TECTURE_IMAGE = pygame.image.load(os.path.join('assets', 'water.png')).convert()
WATER_TECTURE_IMAGE.set_colorkey(TRANSPARENT)

WOOD_TEXTURE_IMAGE = pygame.image.load(os.path.join('assets', 'wood-16x16.png')).convert()
WOOD_TEXTURE_IMAGE.set_colorkey(TRANSPARENT)

BOWL_IMAGE = pygame.image.load(os.path.join('assets', 'bowl_200x139.png')).convert()
BOWL_IMAGE.set_colorkey(TRANSPARENT)

TERRAIN_IMAGES = dict()
TERRAIN_IMAGES[0] = CAKE_IMAGE
TERRAIN_IMAGES[1] = COOKIE_IMAGE
TERRAIN_IMAGES[2] = MUFFIN_IMAGE

MOUSE_SURFACE = pygame.transform.scale(MOUSE_IMAGE, (200, 200))

VICTORY_SURFACE = pygame.transform.scale(VICTORY_IMAGE, (150 * 4, 83 * 4))
VICTORY_SHADOW_SURFACE = pygame.transform.scale(VICTORY_IMAGE_SHADOW, (150 * 4, 83 * 4))

DEFEAT_SURFACE = pygame.transform.scale(DEFEAT_IMAGE, (150 * 4, 83 * 4))
DEFEAT_SHADOW_SURFACE = pygame.transform.scale(DEFEAT_IMAGE_SHADOW, (150 * 4, 83 * 4))

PLAYER_PHASE_SURFACE = pygame.transform.scale(PLAYER_PHASE_IMAGE, (150 * 4, 83 * 4))
PLAYER_PHASE_SHADOW_SURFACE = pygame.transform.scale(PLAYER_PHASE_IMAGE_SHADOW, (150 * 4, 83 * 4))

ENEMY_PHASE_SURFACE = pygame.transform.scale(ENEMY_PHASE_IMAGE, (150 * 4, 83 * 4))
ENEMY_PHASE_SHADOW_SURFACE = pygame.transform.scale(ENEMY_PHASE_IMAGE_SHADOW, (150 * 4, 83 * 4))

WOOD_SURFACE = pygame.transform.scale(WOOD_TEXTURE_IMAGE, (80, 80))

BOWL_SURFACE = pygame.transform.scale(BOWL_IMAGE, (TILE_WIDTH * 3, TILE_HEIGHT * 3))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
DESC_FONT = pygame.font.SysFont('lucidaconsole', 20)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 25)
BABY_FONT = pygame.font.SysFont('lucidaconsole', 23)

all_sprites = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()

victory_area_1 = {
        (5, 3),
        (5, 4),
        (5, 5),
        (6, 3),
        (6, 4),
        (6, 5),
        (7, 3),
        (7, 4),
        (7, 5),
}

victory_area_1_base = (5, 3)

victory_area_2 = {
        (14, 3),
        (14, 4),
        (14, 5),
        (15, 3),
        (15, 4),
        (15, 5),
        (16, 3),
        (16, 4),
        (16, 5),
}

victory_area_2_base = (14, 3)


def determine_legal_target_faster(attack_range, cell):
    i = attack_range
    legal_squares = set()
    legal_squares.add(cell)
    while abs(i) <= attack_range:
        legal_squares.add((cell[0] + i, cell[1]))
        for n in range(attack_range - abs(i)):
            legal_squares.add((cell[0] + i, cell[1] + (n + 1)))
            legal_squares.add((cell[0] + i, cell[1] - (n + 1)))
        i -= 1
    return legal_squares


def determine_legal_movement_faster(movement, cell, enemy=False):
    i = movement
    legal_squares = set()
    legal_squares.add(cell)
    while abs(i) <= movement:
        cell_to_check = (cell[0] + i, cell[1])
        if is_there_a_path(cell, cell_to_check, movement, set(), enemy):
            legal_squares.add(cell_to_check)
        for n in range(movement-abs(i)):
            cell_to_check = (cell[0] + i, cell[1] + (n + 1))
            if is_there_a_path(cell, cell_to_check, movement, set(), enemy):
                legal_squares.add(cell_to_check)
            cell_to_check = (cell[0] + i, cell[1] - (n + 1))
            if is_there_a_path(cell, cell_to_check, movement, set(), enemy):
                legal_squares.add(cell_to_check)
        i -= 1
    return legal_squares


def get_unvisited_neighbors(cell, visited):
    unvisited_neighbors = set()
    check_cell = (cell[0] + 1, cell[1])
    if check_cell not in visited:
        unvisited_neighbors.add(check_cell)
    check_cell = (cell[0] - 1, cell[1])
    if check_cell not in visited:
        unvisited_neighbors.add(check_cell)
    check_cell = (cell[0], cell[1] + 1)
    if check_cell not in visited:
        unvisited_neighbors.add(check_cell)
    check_cell = (cell[0], cell[1] - 1)
    if check_cell not in visited:
        unvisited_neighbors.add(check_cell)
    return unvisited_neighbors


def is_there_a_path(source, dest, movement_range, visited, enemy):
    visited.add(source)
    if source[0] == dest[0] and source[1] == dest[1]:
        # we can't end on the same space as another unit, even if it is an ally.
        return no_unit_at_grid_coordinates(source)
    elif movement_range == 0:
        return False

    move_x = True
    if dest[0] < source[0]:
        left = True
    elif dest[0] > source[0]:
        left = False
    else:
        move_x = False

    move_y = True
    if dest[1] < source[1]:
        up = True
    elif dest[1] > source[1]:
        up = False
    else:
        move_y = False

    if move_x:
        if left:
            next_cell = (source[0] - 1, source[1])
            if no_unit_at_grid_coordinates(next_cell):
                if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                    return True
            else:
                sprite_there = get_unit_at_grid_coordinates(next_cell)
                if isinstance(sprite_there, Unit) and not sprite_there.hostile and not enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                # enemies can move through each other
                if isinstance(sprite_there, Unit) and sprite_there.hostile and enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                else:
                    # we cannot move here at all. We must try another path.
                    visited.add(next_cell)
                    for neighbor in get_unvisited_neighbors(source, visited):
                        if is_there_a_path(neighbor, dest, movement_range-1, visited, enemy):
                            return True
        else:
            next_cell = (source[0] + 1, source[1])
            if no_unit_at_grid_coordinates(next_cell):
                if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                    return True
            else:
                sprite_there = get_unit_at_grid_coordinates(next_cell)
                if isinstance(sprite_there, Unit) and not sprite_there.hostile and not enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                # enemies can move through each other
                if isinstance(sprite_there, Unit) and sprite_there.hostile and enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                else:
                    # we cannot move here at all. We must try another path.
                    visited.add(next_cell)
                    for neighbor in get_unvisited_neighbors(source, visited):
                        if is_there_a_path(neighbor, dest, movement_range-1, visited, enemy):
                            return True
    if move_y:
        if up:
            next_cell = (source[0], source[1] - 1)
            if no_unit_at_grid_coordinates(next_cell):
                if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                    return True
            else:
                sprite_there = get_unit_at_grid_coordinates(next_cell)
                if isinstance(sprite_there, Unit) and not sprite_there.hostile and not enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                # enemies can move through each other
                if isinstance(sprite_there, Unit) and sprite_there.hostile and enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                else:
                    # we cannot move here at all. We must try another path.
                    visited.add(next_cell)
                    for neighbor in get_unvisited_neighbors(source, visited):
                        if is_there_a_path(neighbor, dest, movement_range-1, visited, enemy):
                            return True
        else:
            next_cell = (source[0], source[1] + 1)
            if no_unit_at_grid_coordinates(next_cell):
                if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                    return True
            else:
                sprite_there = get_unit_at_grid_coordinates(next_cell)
                if isinstance(sprite_there, Unit) and not sprite_there.hostile and not enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                # enemies can move through each other
                if isinstance(sprite_there, Unit) and sprite_there.hostile and enemy:
                    if is_there_a_path(next_cell, dest, movement_range - 1, visited, enemy):
                        return True
                else:
                    # we cannot move here at all. We must try another path.
                    visited.add(next_cell)
                    for neighbor in get_unvisited_neighbors(source, visited):
                        if is_there_a_path(neighbor, dest, movement_range-1, visited, enemy):
                            return True
    else:
        # https://youtu.be/6M-NkQAo-3E?t=20
        # if we make it here, it's not a valid path. I think.
        return False


def no_unit_at_grid_coordinates(coordinates):
    xy = coordinates_to_xy(coordinates)
    sprite = MouseSprite(xy)
    mouse_colliding = pygame.sprite.spritecollide(sprite, all_sprites, False)
    if len(mouse_colliding) < 1:
        return True
    return False


def get_unit_at_grid_coordinates(coordinates):
    xy = coordinates_to_xy(coordinates)
    sprite = MouseSprite(xy)
    mouse_colliding = pygame.sprite.spritecollide(sprite, all_sprites, False)
    if len(mouse_colliding) == 1:
        return mouse_colliding[0]
    elif len(mouse_colliding) > 1:
        # multiple, shouldn't be allowed but could happen. Just grab the first one I guess.
        return mouse_colliding[0]
    else:
        return None


def draw_cursor(x, y):
    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + 5, y + 5), (x + 5 + TILE_WIDTH // 3, y + 5))  # top left right line
    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + 5, y + 5), (x + 5, y + 5 + TILE_HEIGHT // 3))  # top left down line

    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + TILE_WIDTH - 5, y + 5), (x + TILE_WIDTH - TILE_WIDTH // 3 - 5, y + 5))  # top right left line
    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + TILE_WIDTH - 5, y + 5), (x + TILE_WIDTH - 5, y + 5 + TILE_HEIGHT // 3))  # top right down line

    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + 5, y + TILE_HEIGHT - 5), (x + 5 + TILE_WIDTH // 3, y + TILE_HEIGHT - 5))  # bottom left right line
    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + 5, y + TILE_HEIGHT - 5), (x + 5, y + TILE_HEIGHT - TILE_HEIGHT // 3 - 5))  # bottom left up line

    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + TILE_WIDTH - 5, y + TILE_HEIGHT - 5), (x + TILE_WIDTH - TILE_WIDTH // 3 - 5, y + TILE_HEIGHT - 5))  # bottom right left line
    pygame.draw.line(ZOOMED_MAP, YELLOW, (x + TILE_WIDTH - 5, y + TILE_HEIGHT - 5), (x + TILE_WIDTH - 5, y + TILE_HEIGHT - TILE_HEIGHT // 3 - 5))  # bottom right up line


def coordinates_to_xy(coordinates):
    return coordinates[0] * TILE_WIDTH, coordinates[1] * TILE_HEIGHT


def mouse_pos_to_grid_coords(mouse_pos):
    return (mouse_pos[0] + camera.x) // TILE_WIDTH, (mouse_pos[1] + camera.y) // TILE_HEIGHT


def mouse_xy_to_map_xy(mouse_pos):
    return mouse_pos[0] + camera.x, mouse_pos[1] + camera.y


def draw_window(cursor_xy, fps, sprite_to_display, moving_sprite_mode, potential_cells_to_move, selecting_sprite_action_mode,
                action_menu_sprites_added, sprite_targeting_mode, potential_cells_to_target, victory, defeat,
                show_player_phase_indicator, show_enemy_phase_indicator, description_to_display, active_allied_sprites,
                all_allied_sprites):
    pygame.draw.rect(ZOOMED_MAP, GRAY, pygame.Rect(0, 0, ZOOMED_MAP_WIDTH, ZOOMED_MAP_HEIGHT))

    bottom_left_rect = pygame.Rect(0, HEIGHT - 200, 200, 200)
    middle_rect = pygame.Rect(200, HEIGHT - 150, WIDTH - 400, 150)
    bottom_right_rect = pygame.Rect(WIDTH - 200, HEIGHT - 200, 200, 200)

    for i in range(GRID_WIDTH):
        for n in range(GRID_HEIGHT):
            ZOOMED_MAP.blit(WOOD_SURFACE, coordinates_to_xy((i, n)))

    ZOOMED_MAP.blit(BOWL_SURFACE, coordinates_to_xy(victory_area_1_base))
    surface = pygame.Surface((TILE_WIDTH * 3, TILE_HEIGHT * 3))
    surface.set_alpha(90)
    surface.fill(YELLOW)
    ZOOMED_MAP.blit(surface, coordinates_to_xy(victory_area_1_base))

    ZOOMED_MAP.blit(BOWL_SURFACE, coordinates_to_xy(victory_area_2_base))
    surface = pygame.Surface((TILE_WIDTH * 3, TILE_HEIGHT * 3))
    surface.set_alpha(90)
    surface.fill(YELLOW)
    ZOOMED_MAP.blit(surface, coordinates_to_xy(victory_area_2_base))

    all_sprites.draw(ZOOMED_MAP)

    for sprite in all_allied_sprites.sprites():
        if sprite not in active_allied_sprites:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(200)
            surface.fill(GRAY)
            ZOOMED_MAP.blit(surface, coordinates_to_xy(sprite.get_grid_coordinates()))

    if moving_sprite_mode:
        for cell in potential_cells_to_move:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(128)
            surface.fill(BLUE)
            ZOOMED_MAP.blit(surface, coordinates_to_xy(cell))

    if selecting_sprite_action_mode:
        widest_action = 0
        for action_name in sprite_to_display.actions.keys():
            text_render = CELL_FONT.render(action_name, True, WHITE)
            if text_render.get_width() > widest_action:
                widest_action = text_render.get_width()
        action_menu_surface = pygame.Surface(
            (widest_action + 4, (CELL_FONT.get_height() + 4) * len(sprite_to_display.actions.keys())))
        action_menu_surface.set_alpha(192)
        action_menu_surface.fill(BLACK)
        rect = pygame.Rect(2, 2, widest_action, CELL_FONT.get_height())
        sprite_rect = pygame.Rect(sprite_to_display.rect.x + sprite_to_display.rect.width + 5, sprite_to_display.rect.y + 5, widest_action, CELL_FONT.get_height())
        for action_name in sprite_to_display.actions.keys():
            drawText(action_menu_surface, action_name, WHITE, rect, CELL_FONT, True)
            if not action_menu_sprites_added:
                add_sprite_to_group(MenuItem(sprite_rect, action_name, sprite_to_display.actions[action_name][1]), menu_sprites)
            rect = pygame.Rect(2, rect.y + CELL_FONT.get_height() + 2, widest_action, CELL_FONT.get_height())
            sprite_rect = pygame.Rect(sprite_to_display.rect.x + sprite_to_display.rect.width + 5, sprite_rect.y + CELL_FONT.get_height(), widest_action, CELL_FONT.get_height())
        ZOOMED_MAP.blit(action_menu_surface, (sprite_to_display.rect.x + sprite_to_display.rect.width + 5, sprite_to_display.rect.y + 5))

    if sprite_targeting_mode:
        for cell in potential_cells_to_target:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(128)
            surface.fill(RED)
            ZOOMED_MAP.blit(surface, coordinates_to_xy(cell))

    draw_cursor(cursor_xy[0], cursor_xy[1])

    WIN.blit(ZOOMED_MAP, (0, 0), camera)

    pygame.draw.rect(WIN, BLACK, bottom_left_rect)
    WIN.blit(MOUSE_SURFACE, (bottom_left_rect.x, bottom_left_rect.y))
    pygame.draw.rect(WIN, BLACK, bottom_right_rect)
    drawText(WIN, "Victory Condition: Begin your turn with at least one allied unit and no enemy units in all yellow areas.", WHITE, bottom_right_rect, BABY_FONT, True)
    pygame.draw.rect(WIN, BLACK, middle_rect)
    if description_to_display is not None:
        drawText(WIN, description_to_display, WHITE, middle_rect, TEXT_FONT, True)
    if sprite_to_display is None:
        pass
    elif description_to_display is None:
        drawText(WIN, sprite_to_display.unitType.name, WHITE, middle_rect, TEXT_FONT, True)
        next_rect = pygame.Rect(middle_rect.x, middle_rect.y + TEXT_FONT.get_height() + 3, middle_rect.width, middle_rect.height)
        drawText(WIN, "HP: " + str(sprite_to_display.hp) + "/" + str(sprite_to_display.max_hp), WHITE, next_rect, TEXT_FONT, True)
        next_rect = pygame.Rect(next_rect.x, next_rect.y + TEXT_FONT.get_height() + 3, next_rect.width,
                                next_rect.height)
        drawText(WIN, "Movement: " + str(sprite_to_display.movement) + ", Damage: " + str(sprite_to_display.damage), WHITE, next_rect, TEXT_FONT, True)

    drawText(WIN, fps, WHITE, pygame.Rect(5, 5, 300, 300), TEXT_FONT, True)

    if victory:
        WIN.blit(VICTORY_SHADOW_SURFACE,
                 (WIDTH // 2 - VICTORY_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2 + 10))
        WIN.blit(VICTORY_SURFACE, (WIDTH // 2 - VICTORY_SURFACE.get_width() // 2, HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2))
        drawText(WIN, "Use the left or right mouse button to restart!", WHITE, pygame.Rect(WIDTH // 2 - VICTORY_SURFACE.get_width() // 2, HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2 + 270, 500, 500), TEXT_FONT, True)

    elif defeat:
        WIN.blit(DEFEAT_SHADOW_SURFACE,
                 (WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2 + 10))
        WIN.blit(DEFEAT_SURFACE, (WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2, HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2))
        drawText(WIN, "Use the left or right mouse button to restart!", WHITE, pygame.Rect(WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2, HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2 + 270, 500, 500), TEXT_FONT, True)

    elif show_player_phase_indicator:
        WIN.blit(PLAYER_PHASE_SHADOW_SURFACE,
                 (WIDTH // 2 - PLAYER_PHASE_SHADOW_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - PLAYER_PHASE_SHADOW_SURFACE.get_height() // 2 + 10))
        WIN.blit(PLAYER_PHASE_SURFACE,
                 (WIDTH // 2 - PLAYER_PHASE_SURFACE.get_width() // 2, HEIGHT // 2 - PLAYER_PHASE_SURFACE.get_height() // 2))

    elif show_enemy_phase_indicator:
        WIN.blit(ENEMY_PHASE_SHADOW_SURFACE,
                 (WIDTH // 2 - ENEMY_PHASE_SHADOW_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - ENEMY_PHASE_SHADOW_SURFACE.get_height() // 2 + 10))
        WIN.blit(ENEMY_PHASE_SURFACE,
                 (WIDTH // 2 - ENEMY_PHASE_SURFACE.get_width() // 2, HEIGHT // 2 - ENEMY_PHASE_SURFACE.get_height() // 2))

    pygame.display.update()


def add_sprite_to_group(sprite, group):
    group.add(sprite)
    # do not add the sprite twice if the group given is all_sprites
    if not group == all_sprites:
        all_sprites.add(sprite)


def move_camera(mouse_pos):
    if mouse_pos[0] < 10:
        if camera.x > CAMERA_SPEED:
            camera.x -= CAMERA_SPEED
        else:
            camera.x = 0
    elif mouse_pos[0] > WIDTH - 10:
        if camera.x < ZOOMED_MAP_WIDTH - WIDTH - CAMERA_SPEED:
            camera.x += CAMERA_SPEED
        else:
            camera.x = ZOOMED_MAP_WIDTH - WIDTH
    if mouse_pos[1] < 10:
        if camera.y > CAMERA_SPEED:
            camera.y -= CAMERA_SPEED
        else:
            camera.y = 0
    elif mouse_pos[1] > HEIGHT - 10:
        if camera.y < ZOOMED_MAP_HEIGHT - HEIGHT - CAMERA_SPEED:
            camera.y += CAMERA_SPEED
        else:
            camera.y = ZOOMED_MAP_HEIGHT - HEIGHT


def victory_condition(allied_sprites, enemy_sprites):

    for enemy in enemy_sprites:
        if enemy.get_grid_coordinates() in victory_area_1:
            return False
    for enemy in enemy_sprites:
        if enemy.get_grid_coordinates() in victory_area_2:
            return False
    first_area_secure = False
    for ally in allied_sprites:
        if ally.get_grid_coordinates() in victory_area_1:
            first_area_secure = True
    if first_area_secure:
        for ally in allied_sprites:
            if ally.get_grid_coordinates() in victory_area_2:
                return True
    return False


def get_random_terrain_image():
    return TERRAIN_IMAGES[random.randint(0, 2)]


def generate_terrain():
    # bottom of the map
    for i in range(GRID_WIDTH):
        for n in range(4):
            xy = coordinates_to_xy((i, 22 + n))
            water_terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(water_terrain, terrain_sprites)

    # bottom left wall
    for i in range(8):
        xy = coordinates_to_xy((i, 21))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # bottom right wall
    for i in range(13):
        xy = coordinates_to_xy((13 + i, 21))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # bottom left bit of water
    for i in range(3):
        xy = coordinates_to_xy((3 + i, 20))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # bottom left chunk of water
    for i in range(3):
        for n in range(8):
            xy = coordinates_to_xy((3 + i, 18 - n))
            terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # small buildings right of the bottom left chunk of water
    for i in range(3):
        xy = coordinates_to_xy((6, 18 - i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # middle row of blocking buildings
    for i in range(3):
        xy = coordinates_to_xy((9 + i, 12))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # large chunk of water on the bottom right, p1
    for i in range(4):
        for n in range(7):
            xy = coordinates_to_xy((15 + i, 17 - n))
            terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # large chunk of water on the bottom right, p2
    for i in range(3):
        for n in range(3):
            xy = coordinates_to_xy((19 + i, 17 - n))
            terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # large chunk of water on the bottom right, p3
    for i in range(3):
        for n in range(3):
            xy = coordinates_to_xy((23 + i, 17 - n))
            terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # long, thin row of buildings on the right
    for i in range(11):
        xy = coordinates_to_xy((22, 12 - i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p1
    for i in range(5):
        xy = coordinates_to_xy((3, 4 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p2
    for i in range(3):
        xy = coordinates_to_xy((4, 6 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p3
    for i in range(2):
        xy = coordinates_to_xy((5, 7 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p4
    for i in range(1):
        xy = coordinates_to_xy((6, 8 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p5
    for i in range(2):
        xy = coordinates_to_xy((7, 7 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p6
    for i in range(3):
        xy = coordinates_to_xy((8, 6 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p7
    for i in range(7):
        xy = coordinates_to_xy((9, 2 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p8
    for i in range(9):
        for n in range(2):
            xy = coordinates_to_xy((10 + n, i))
            terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p9
    for i in range(7):
        xy = coordinates_to_xy((12, 2 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p10
    for i in range(3):
        xy = coordinates_to_xy((13, 6 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p11
    for i in range(2):
        xy = coordinates_to_xy((14, 7 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p12
    for i in range(1):
        xy = coordinates_to_xy((15, 8 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p13
    for i in range(2):
        xy = coordinates_to_xy((16, 7 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p14
    for i in range(3):
        xy = coordinates_to_xy((17, 6 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # main body of water, left side p15
    for i in range(5):
        xy = coordinates_to_xy((18, 4 + i))
        terrain = Terrain(WATER_TECTURE_IMAGE, TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # square building, top left
    for i in range(2):
        for n in range(2):
            xy = coordinates_to_xy((3 + n, i))
            terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 1
    for i in range(2):
        xy = coordinates_to_xy((4, 4 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 2
    for i in range(1):
        xy = coordinates_to_xy((5 + i, 6))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 3
    for i in range(1):
        xy = coordinates_to_xy((6 + i, 7))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 4
    for i in range(1):
        xy = coordinates_to_xy((7 + i, 6))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 5
    for i in range(6):
        xy = coordinates_to_xy((8, i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 6
    for i in range(2):
        xy = coordinates_to_xy((9, i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 7
    for i in range(2):
        for n in range(2):
            xy = coordinates_to_xy((12 + n, i))
            terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 7
    for i in range(4):
        xy = coordinates_to_xy((13, 2 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 8
    for i in range(1):
        xy = coordinates_to_xy((14, 6 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 9
    for i in range(1):
        xy = coordinates_to_xy((15, 7 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 10
    for i in range(1):
        xy = coordinates_to_xy((16, 6 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # water rim, part 11
    for i in range(2):
        xy = coordinates_to_xy((17, 4 + i))
        terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
        add_sprite_to_group(terrain, terrain_sprites)

    # square building, upper right
    for i in range(2):
        for n in range(2):
            xy = coordinates_to_xy((17 + n, i))
            terrain = Terrain(get_random_terrain_image(), TILE_WIDTH, TILE_HEIGHT, xy[0], xy[1])
            add_sprite_to_group(terrain, terrain_sprites)


def place_enemies(enemy_units):
    xy = coordinates_to_xy((1, 1))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((5, 3))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((7, 3))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((7, 2))
    enemy = FlySoldier(FLY_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.FLY, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((2, 7))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((3, 9))
    enemy = FlySoldier(FLY_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.FLY, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((4, 10))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((5, 9))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((0, 14))
    enemy = FlySoldier(FLY_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.FLY, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((0, 13))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((14, 3))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((16, 2))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((20, 1))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((24, 1))
    enemy = FlySoldier(FLY_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.FLY, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((16, 9))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((17, 10))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((20, 6))
    enemy = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((21, 13))
    enemy = FlySoldier(FLY_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.FLY, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)

    xy = coordinates_to_xy((21, 14))
    enemy = AppleSoldier(APPLE_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.BAD_APPLE, xy[0], xy[1])
    add_sprite_to_group(enemy, enemy_units)


def place_allies(allied_units):
    xy = coordinates_to_xy((9, 18))
    ally = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((10, 18))
    ally = SugarSoldier(SUGAR_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.SUGAR, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((11, 18))
    ally = SugarSoldier(SUGAR_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.SUGAR, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((12, 18))
    ally = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((9, 17))
    ally = OilSoldier(OIL_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.OIL, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((10, 17))
    ally = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((11, 17))
    ally = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((12, 17))
    ally = OilSoldier(OIL_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.OIL, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((10, 16))
    ally = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)

    xy = coordinates_to_xy((11, 16))
    ally = OilSoldier(OIL_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.OIL, xy[0], xy[1])
    add_sprite_to_group(ally, allied_units)


def game():
    pygame.mixer.music.load(os.path.join('assets', 'xDeviruchi - Exploring The Unknown (Loop).wav'))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    pygame.event.set_grab(True)
    restart = False
    for sprite in all_sprites.sprites():
        sprite.kill()
    clock = pygame.time.Clock()
    title_mode = True
    run = True
    zoomed = False
    frames = 0
    frames_string = ''
    time_ms = 0
    game_begin_time = pygame.time.get_ticks()  # the time that the game actually began
    start_time = pygame.time.get_ticks()  # the time that the maze we're on began
    cursor_grid_coordinates = (0, 0)
    # idk what a reasonable starting value is.
    cursor_xy_coordinates = (WIDTH // 2, HEIGHT // 2)
    pygame.mouse.set_pos(cursor_xy_coordinates)
    potential_cells_to_move = set()
    potential_cells_to_target = set()

    camera_mode = True
    moving_sprite_mode = False
    selecting_sprite_action_mode = False
    selected_action_name = ''
    sprite_targeting_mode = False

    action_menu_sprites_added = False

    player_turn = True
    start_of_player_turn = True
    show_player_phase_start = True
    show_enemy_phase_start = False
    defeated = False
    victory = False

    enemy_move_start_time = pygame.time.get_ticks()

    generate_terrain()

    allied_units = pygame.sprite.Group()
    active_allied_units = pygame.sprite.Group()
    place_allies(allied_units)

    active_hostile_units = pygame.sprite.Group()
    enemy_units = pygame.sprite.Group()
    place_enemies(enemy_units)


    sprite_to_display = None
    sprite_moving_current_coordinates = None
    description_to_display = None

    while run:
        clock.tick(FPS)
        move_camera(pygame.mouse.get_pos())

        if len(active_hostile_units.sprites()) < 1 and not player_turn:
            # I think this if statement can just be combined with the below one, but whatever
            start_of_player_turn = True

        if start_of_player_turn:
            # add all allied units into the active group
            show_player_phase_start = True
            if victory_condition(allied_units.sprites(), enemy_units.sprites()):
                victory = True
                show_player_phase_start = False
                print("MISSION COMPLETE BABY")
                # We have won.
                pygame.mixer.music.load(os.path.join('assets', 'xDeviruchi - Take some rest and eat some food! (Loop).wav'))
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)

            if len(allied_units) < 1:
                pygame.mixer.music.load(os.path.join('assets', 'xDeviruchi - The Icy Cave (Loop).wav'))
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)
                print("MISSION FAILED, WE'LL GET EM NEXT TIME")
                defeated = True
                show_player_phase_start = False
            active_allied_units.add(allied_units)
            start_of_player_turn = False
            player_turn = True

        if len(active_allied_units.sprites()) < 1 and player_turn:
            player_turn = False
            active_hostile_units.add(enemy_units)
            show_enemy_phase_start = True
            if len(active_hostile_units) < 1:
                start_of_player_turn = True
                show_enemy_phase_start = False
            enemy_move_start_time = pygame.time.get_ticks()

        enemy_turn_length = 1000  # ms
        # move an enemy unit every 2 seconds
        if not defeated and not player_turn and len(active_hostile_units.sprites()) > 0 and enemy_move_start_time < pygame.time.get_ticks() - enemy_turn_length:
            show_enemy_phase_start = False
            enemy_move_start_time = pygame.time.get_ticks()
            sprite = active_hostile_units.sprites()[0]

            # from https://stackoverflow.com/questions/55579764/pygame-how-to-find-the-nearest-sprite-in-an-array-and-lock-onto-it
            pos = pygame.math.Vector2(sprite.rect.x + sprite.rect.width // 2, sprite.rect.y + sprite.rect.height // 2)
            if len(allied_units.sprites()) > 0:
                targeted_unit = min([e for e in allied_units], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.x + e.rect.width // 2, e.rect.y + e.rect.height // 2)))
            else:
                # just do this to get through the turn
                targeted_unit = sprite
            legal_moves = determine_legal_movement_faster(sprite.movement, sprite.get_grid_coordinates(), True)
            targeted_unit_coordinates = targeted_unit.get_grid_coordinates()
            adjacent_squares = {(targeted_unit_coordinates[0] + 1, targeted_unit_coordinates[1]),
                                (targeted_unit_coordinates[0] - 1, targeted_unit_coordinates[1]),
                                (targeted_unit_coordinates[0], targeted_unit_coordinates[1] + 1),
                                (targeted_unit_coordinates[0], targeted_unit_coordinates[1] - 1)}
            moved = False
            for square in adjacent_squares:
                if square in legal_moves:
                    sprite.move_to_grid_coordinates(square)
                    if sprite.actions["Attack"][0](targeted_unit):
                        # attack success
                        moved = True
                        break
                    else:
                        sprite.actions["Wait"][0](sprite)
                        # don't wait if all this unit did was Wait
                        enemy_move_start_time -= enemy_turn_length
                        moved = True
                        break
            if not moved:
                sprite.actions["Wait"][0](sprite)
                # don't wait if all this unit did was Wait
                enemy_move_start_time -= enemy_turn_length
            active_hostile_units.remove(sprite)

        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == pygame.MOUSEMOTION:
                # if we are hovering over a menu item, display the description in the bottom section
                mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, menu_sprites, False)
                if len(mouse_colliding) > 1:
                    # lol what
                    description_to_display = None
                elif len(mouse_colliding) == 1:
                    # move into target mode
                    description_to_display = mouse_colliding[0].description
                else:
                    # no menu item was selected
                    description_to_display = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                # these are the values of event.button depending on which is pressed:
                # 1 - left click
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                # 5 - scroll down
                # see https://stackoverflow.com/questions/34287938/how-to-distinguish-left-click-right-click-mouse-clicks-in-pygame
                if event.button == 1:
                    # left click
                    if show_player_phase_start:
                        show_player_phase_start = False
                    if victory or defeated:
                        restart = True
                        run = False
                    if camera_mode:
                        cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                        mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                        mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, all_sprites, False)
                        if len(mouse_colliding) > 1:
                            # lol what, I guess pick the first allied unit in here?
                            for sprite in mouse_colliding:
                                if isinstance(sprite, Unit) and not sprite.hostile:
                                    potential_cells_to_move = determine_legal_movement_faster(
                                        sprite_to_display.movement, sprite_to_display.get_grid_coordinates())
                                    camera_mode = False
                                    moving_sprite_mode = True
                        elif len(mouse_colliding) == 1 and not isinstance(mouse_colliding[0], Terrain) and not isinstance(mouse_colliding[0], MenuItem):
                            # display the unit information on the bottom screen
                            sprite_to_display = mouse_colliding[0]
                            if not sprite_to_display.hostile and active_allied_units.has(sprite_to_display):
                                potential_cells_to_move = determine_legal_movement_faster(sprite_to_display.movement, sprite_to_display.get_grid_coordinates())
                                camera_mode = False
                                moving_sprite_mode = True
                        else:
                            # no unit is being hovered
                            sprite_to_display = None
                    elif moving_sprite_mode:
                        cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                        if cursor_grid_coordinates in potential_cells_to_move:
                            # they can move here, move them to the next phase
                            action_menu_sprites_added = False
                            for sprite in menu_sprites.sprites():
                                sprite.kill()
                            sprite_moving_current_coordinates = sprite_to_display.get_grid_coordinates()
                            sprite_to_display.move_to_grid_coordinates(cursor_grid_coordinates)
                            moving_sprite_mode = False
                            selecting_sprite_action_mode = True
                        else:
                            # do nothing
                            pass
                    elif selecting_sprite_action_mode:
                        mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                        mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, menu_sprites, False)
                        if len(mouse_colliding) > 1:
                            # lol what
                            raise TypeError("This should not have happened, unless my logic is flawed")
                        elif len(mouse_colliding) == 1:
                            # move into target mode
                            selecting_sprite_action_mode = False
                            selected_action_name = mouse_colliding[0].name
                            potential_cells_to_target = determine_legal_target_faster(sprite_to_display.get_action_range(selected_action_name),
                                                                               sprite_to_display.get_grid_coordinates())
                            sprite_targeting_mode = True
                        else:
                            # no menu item was selected
                            pass
                    elif sprite_targeting_mode:
                        for sprite in menu_sprites:
                            sprite.kill()
                        mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                        cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                        mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, all_sprites, False)
                        if cursor_grid_coordinates in potential_cells_to_target and len(mouse_colliding) == 1:
                            # attempt to target the selected sprite
                            result = sprite_to_display.actions[selected_action_name][0](mouse_colliding[0])
                            if result:
                                # the target was successful, move on
                                sprite_targeting_mode = False
                                camera_mode = True
                                active_allied_units.remove(sprite_to_display)
                                sprite_to_display = None
                            else:
                                # the target was not successful, do not move on
                                sound = pygame.mixer.Sound(os.path.join('assets', 'error.wav'))
                                sound.set_volume(0.1)
                                sound.play()
                                pass
                        elif len(mouse_colliding) > 1:
                            print(mouse_colliding)
                            raise TypeError("Multiple sprites were targeted - how???")
                        else:
                            sound = pygame.mixer.Sound(os.path.join('assets', 'error.wav'))
                            sound.set_volume(0.1)
                            sound.play()
                            pass
                if event.button == 3:
                    # right click
                    if victory:
                        restart = True
                        run = False
                    if camera_mode:
                        show_player_phase_start = False
                        sprite_to_display = None
                    elif moving_sprite_mode:
                        moving_sprite_mode = False
                        camera_mode = True
                        potential_cells_to_move.clear()
                    elif selecting_sprite_action_mode:
                        sprite_to_display.move_to_grid_coordinates(sprite_moving_current_coordinates)
                        cursor_grid_coordinates = sprite_moving_current_coordinates
                        for sprite in menu_sprites:
                            sprite.kill()
                        selecting_sprite_action_mode = False
                        moving_sprite_mode = True
                    elif sprite_targeting_mode:
                        cursor_grid_coordinates = sprite_to_display.get_grid_coordinates()
                        potential_cells_to_target.clear()
                        sprite_targeting_mode = False
                        action_menu_sprites_added = False
                        for sprite in menu_sprites.sprites():
                            sprite.kill()
                        selecting_sprite_action_mode = True
                # as per the jam restrictions, these are the only allowed buttons

            # escape should be allowed, right?
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    continue
        if not run:
            continue
        draw_window(coordinates_to_xy(cursor_grid_coordinates), frames_string, sprite_to_display, moving_sprite_mode,
                    potential_cells_to_move, selecting_sprite_action_mode, action_menu_sprites_added,
                    sprite_targeting_mode, potential_cells_to_target, victory, defeated, show_player_phase_start,
                    show_enemy_phase_start, description_to_display, active_allied_units, allied_units)
        if not action_menu_sprites_added:
            action_menu_sprites_added = True

        frames += 1
        current_time_ms = pygame.time.get_ticks() % 1000
        if time_ms > current_time_ms:
            frames_string = repr(frames)
            frames = 0
        time_ms = current_time_ms
    if restart:
        game()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game()
