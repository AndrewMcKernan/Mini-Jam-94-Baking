import os, sys
import pygame
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
camera = pygame.Rect((ZOOMED_MAP_WIDTH // 2 - WIDTH // 2, ZOOMED_MAP_HEIGHT // 2 - HEIGHT // 2), (WIDTH, HEIGHT))

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)
ZOOMED_BACKGROUND = pygame.Rect(0, 0, ZOOMED_MAP_WIDTH, ZOOMED_MAP_HEIGHT)


EGG_IMAGE = pygame.image.load(os.path.join('assets', 'egg.png')).convert()
EGG_IMAGE.set_colorkey(TRANSPARENT)

GOOP_IMAGE = pygame.image.load(os.path.join('assets', 'goop.png')).convert()
GOOP_IMAGE.set_colorkey(TRANSPARENT)

FORK_IMAGE = pygame.image.load(os.path.join('assets', 'fork.png')).convert()
FORK_IMAGE.set_colorkey(TRANSPARENT)

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

MAP_IMAGES = dict()

#pygame.mixer.music.load(os.path.join('assets', 'Spy.mp3'))
#pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play(-1)

MOUSE_SURFACE = pygame.transform.scale(MOUSE_IMAGE, (200, 200))

VICTORY_SURFACE = pygame.transform.scale(VICTORY_IMAGE, (150 * 4, 83 * 4))
VICTORY_SHADOW_SURFACE = pygame.transform.scale(VICTORY_IMAGE_SHADOW, (150 * 4, 83 * 4))

DEFEAT_SURFACE = pygame.transform.scale(DEFEAT_IMAGE, (150 * 4, 83 * 4))
DEFEAT_SHADOW_SURFACE = pygame.transform.scale(DEFEAT_IMAGE_SHADOW, (150 * 4, 83 * 4))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
DESC_FONT = pygame.font.SysFont('lucidaconsole', 20)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 25)
BABY_FONT = pygame.font.SysFont('lucidaconsole', 23)

all_sprites = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()

victory_area_1 = {
        (40,20),
        (41,20),
        (41,21),
        (40,21)
}


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
                action_menu_sprites_added, sprite_targeting_mode, potential_cells_to_target, victory, defeat):
    pygame.draw.rect(ZOOMED_MAP, GRAY, pygame.Rect(0, 0, ZOOMED_MAP_WIDTH, ZOOMED_MAP_HEIGHT))

    bottom_left_rect = pygame.Rect(0, HEIGHT - 200, 200, 200)
    middle_rect = pygame.Rect(200, HEIGHT - 150, WIDTH - 400, 150)
    bottom_right_rect = pygame.Rect(WIDTH - 200, HEIGHT - 200, 200, 200)

    x = 0
    while x < ZOOMED_MAP_WIDTH:
        pygame.draw.line(ZOOMED_MAP, RED, (x, 0), (x, ZOOMED_MAP_HEIGHT))
        x += TILE_WIDTH
    y = 0
    while y < ZOOMED_MAP_HEIGHT:
        pygame.draw.line(ZOOMED_MAP, RED, (0, y), (ZOOMED_MAP_WIDTH, y))
        y += TILE_HEIGHT

    draw_cursor(cursor_xy[0], cursor_xy[1])

    all_sprites.draw(ZOOMED_MAP)

    for cell in victory_area_1:
        surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        surface.set_alpha(64)
        surface.fill(YELLOW)
        ZOOMED_MAP.blit(surface, coordinates_to_xy(cell))

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
                add_sprite_to_group(MenuItem(sprite_rect, action_name), menu_sprites)
            rect = pygame.Rect(2, rect.y + CELL_FONT.get_height() + 2, widest_action, CELL_FONT.get_height())
            sprite_rect = pygame.Rect(sprite_to_display.rect.x + sprite_to_display.rect.width + 5, sprite_rect.y + CELL_FONT.get_height(), widest_action, CELL_FONT.get_height())
        ZOOMED_MAP.blit(action_menu_surface, (sprite_to_display.rect.x + sprite_to_display.rect.width + 5, sprite_to_display.rect.y + 5))

    if sprite_targeting_mode:
        for cell in potential_cells_to_target:
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.set_alpha(128)
            surface.fill(RED)
            ZOOMED_MAP.blit(surface, coordinates_to_xy(cell))

    WIN.blit(ZOOMED_MAP, (0, 0), camera)

    pygame.draw.rect(WIN, BLACK, bottom_left_rect)
    WIN.blit(MOUSE_SURFACE, (bottom_left_rect.x, bottom_left_rect.y))
    pygame.draw.rect(WIN, BLACK, bottom_right_rect)
    drawText(WIN, "Victory Condition: Begin your turn with at least one allied unit and no enemy units in all yellow areas.", WHITE, bottom_right_rect, BABY_FONT, True)
    pygame.draw.rect(WIN, BLACK, middle_rect)
    if sprite_to_display is None:
        pass
    else:
        drawText(WIN, sprite_to_display.unitType.name, WHITE, middle_rect, TEXT_FONT, True)
        next_rect = pygame.Rect(middle_rect.x, middle_rect.y + TEXT_FONT.get_height() + 3, middle_rect.width, middle_rect.height)
        drawText(WIN, "HP: " + str(sprite_to_display.hp) + "/" + str(sprite_to_display.max_hp), WHITE, next_rect, TEXT_FONT, True)
        next_rect = pygame.Rect(next_rect.x, next_rect.y + TEXT_FONT.get_height() + 3, next_rect.width,
                                next_rect.height)
        drawText(WIN, "Movement: " + str(sprite_to_display.movement), WHITE, next_rect, TEXT_FONT, True)

    drawText(WIN, fps, WHITE, pygame.Rect(5, 5, 300, 300), TEXT_FONT, True)

    if victory:
        WIN.blit(VICTORY_SHADOW_SURFACE,
                 (WIDTH // 2 - VICTORY_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2 + 10))
        WIN.blit(VICTORY_SURFACE, (WIDTH // 2 - VICTORY_SURFACE.get_width() // 2, HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2))
        drawText(WIN, "Use the left or right mouse button to restart!", WHITE, pygame.Rect(WIDTH // 2 - VICTORY_SURFACE.get_width() // 2, HEIGHT // 2 - VICTORY_SURFACE.get_height() // 2 + 270, 500, 500), TEXT_FONT, True)

    if defeat:
        WIN.blit(DEFEAT_SHADOW_SURFACE,
                 (WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2 + 10,
                  HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2 + 10))
        WIN.blit(DEFEAT_SURFACE, (WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2, HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2))
        drawText(WIN, "Use the left or right mouse button to restart!", WHITE, pygame.Rect(WIDTH // 2 - DEFEAT_SURFACE.get_width() // 2, HEIGHT // 2 - DEFEAT_SURFACE.get_height() // 2 + 270, 500, 500), TEXT_FONT, True)

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


def victory_condition_1(allied_sprites, enemy_sprites):

    for enemy in enemy_sprites:
        if enemy.get_grid_coordinates() in victory_area_1:
            return False
    for ally in allied_sprites:
        if ally.get_grid_coordinates() in victory_area_1:
            return True


def game():
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
    start_of_enemy_turn = False
    defeated = False
    victory = False

    enemy_move_start_time = pygame.time.get_ticks()

    starting_xy = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2))
    starting_xy_goop = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2 - 2))
    starting_xy_fork = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2 - 1))

    egg_soldier = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, starting_xy[0], starting_xy[1])
    goop_soldier = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, starting_xy_goop[0], starting_xy_goop[1])
    fork_terrain = Terrain(FORK_IMAGE, TILE_WIDTH, TILE_HEIGHT, starting_xy_fork[0], starting_xy_fork[1])
    add_sprite_to_group(fork_terrain, terrain_sprites)

    allied_units = pygame.sprite.Group()
    active_allied_units = pygame.sprite.Group()
    active_hostile_units = pygame.sprite.Group()
    enemy_units = pygame.sprite.Group()
    add_sprite_to_group(egg_soldier, allied_units)
    add_sprite_to_group(goop_soldier, enemy_units)
    sprite_to_display = None
    sprite_moving_current_coordinates = None

    while run:
        clock.tick(FPS)
        move_camera(pygame.mouse.get_pos())

        if len(active_hostile_units.sprites()) < 1 and not player_turn:
            # I think this if statement can just be combined with the below one, but whatever
            start_of_player_turn = True

        if start_of_player_turn:
            # add all allied units into the active group

            if victory_condition_1(allied_units.sprites(), enemy_units.sprites()):
                victory = True
                print("MISSION COMPLETE BABY")
                # We have won.
                # TODO: play fanfare sound

            if len(allied_units) < 1:
                # TODO: play sad fanfare sound
                print("MISSION FAILED, WE'LL GET EM NEXT TIME")
                defeated = True
            active_allied_units.add(allied_units)
            start_of_player_turn = False
            player_turn = True
            # TODO: show an indicator that the player turn has started

        if len(active_allied_units.sprites()) < 1 and player_turn:
            player_turn = False
            active_hostile_units.add(enemy_units)
            # TODO: show an indicator that the enemy turn has started

        # move an enemy unit every 2 seconds
        if not defeated and not player_turn and len(active_hostile_units.sprites()) > 0 and enemy_move_start_time < pygame.time.get_ticks() - 2000:
            enemy_move_start_time = pygame.time.get_ticks()
            sprite = active_hostile_units.sprites()[0]

            # from https://stackoverflow.com/questions/55579764/pygame-how-to-find-the-nearest-sprite-in-an-array-and-lock-onto-it
            pos = pygame.math.Vector2(sprite.rect.x + sprite.rect.width // 2, sprite.rect.y + sprite.rect.height // 2)
            targeted_unit = min([e for e in allied_units], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.x + e.rect.width // 2, e.rect.y + e.rect.height // 2)))
            legal_moves = determine_legal_movement_faster(sprite.movement, sprite.get_grid_coordinates(), True)
            targeted_unit_coordinates = targeted_unit.get_grid_coordinates()
            adjacent_squares = {(targeted_unit_coordinates[0] + 1, targeted_unit_coordinates[1]),
                                (targeted_unit_coordinates[0] - 1, targeted_unit_coordinates[1]),
                                (targeted_unit_coordinates[0], targeted_unit_coordinates[1] + 1),
                                (targeted_unit_coordinates[0], targeted_unit_coordinates[1] - 1)}
            for square in adjacent_squares:
                if square in legal_moves:
                    sprite.move_to_grid_coordinates(square)
                    if sprite.actions["Attack"](targeted_unit):
                        # attack success
                        # TODO: play a sound effect
                        break
                    else:
                        sprite.actions["Wait"](sprite)
                        # TODO: play a sound effect
                        break
            active_hostile_units.remove(sprite)

        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
            if event.type == pygame.MOUSEMOTION:
                pass
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
                    if victory or defeated:
                        restart = True
                        run = False
                    if camera_mode:
                        cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                        mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                        mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, all_sprites, False)
                        if len(mouse_colliding) > 1:
                            # lol what
                            pass
                        elif len(mouse_colliding) == 1 and not isinstance(mouse_colliding[0], Terrain):
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
                            pass
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
                            result = sprite_to_display.actions[selected_action_name](mouse_colliding[0])
                            if result:
                                # the target was successful, move on
                                # TODO: play a sound effect based on the action performed
                                sprite_targeting_mode = False
                                camera_mode = True
                                active_allied_units.remove(sprite_to_display)
                                sprite_to_display = None
                            else:
                                # the target was not successful, do not move on
                                # TODO: play a sound effect indicating an improper targeting
                                pass
                        else:
                            # TODO: play a sound effect indicating an improper targeting
                            pass
                if event.button == 3:
                    if victory:
                        restart = True
                        run = False
                    if camera_mode:
                        # right click
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
                        potential_cells_to_target.clear()
                        sprite_targeting_mode = False
                        action_menu_sprites_added = False
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
                    sprite_targeting_mode, potential_cells_to_target, victory, defeated)
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
