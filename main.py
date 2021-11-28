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

MOUSE_IMAGE = pygame.image.load(os.path.join('assets', 'mouse.png')).convert()
MOUSE_IMAGE.set_colorkey(TRANSPARENT)

MAP_IMAGES = dict()

#pygame.mixer.music.load(os.path.join('assets', 'Spy.mp3'))
#pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play(-1)

MOUSE_SURFACE = pygame.transform.scale(MOUSE_IMAGE, (200, 200))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
DESC_FONT = pygame.font.SysFont('lucidaconsole', 20)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 25)

all_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()


def determine_legal_movement(movement, cell):
    # I want to return a set of coordinates that area legal to move into
    # I need to generate all possible combinations of moves, and then apply those moves to ensure they are legal.
    if movement == 0:
        return {(cell)}
    i = movement
    return_set = set()
    while i >= 0:
        possible_cells = get_possible_cells(cell)
        return_set = return_set.union(possible_cells)
        for cells in possible_cells:
            more_cells = determine_legal_movement(movement - 1, cells)
            return_set = return_set.union(more_cells)
        i -= 1
    if 15 in return_set:
        print(movement, cell, return_set)
        raise TypeError("Why")
    return return_set


def get_possible_cells(cell):
    possible_cells = set()
    for option in MOVEMENT_OPTIONS:
        if option == UP:
            # TODO: is this space legal?
            possible_cells.add((cell[0] - 1, cell[1]))
        if option == DOWN:
            # TODO: is this space legal?
            possible_cells.add((cell[0] + 1, cell[1]))
        if option == LEFT:
            # TODO: is this space legal?
            possible_cells.add((cell[0], cell[1] - 1))
        if option == RIGHT:
            # TODO: is this space legal?
            possible_cells.add((cell[0], cell[1] + 1))
    return possible_cells


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
                action_menu_sprites_added, sprite_targeting_mode, potential_cells_to_target):
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

    # allied_units.draw(ZOOMED_MAP)

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


def game():
    pygame.event.set_grab(True)
    restart = False
    all_sprites.empty()
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

    starting_xy = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2))
    starting_xy_goop = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2 - 2))

    egg_soldier = EggSoldier(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, starting_xy[0], starting_xy[1])
    goop_soldier = GoopSoldier(GOOP_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.GOOP, starting_xy_goop[0], starting_xy_goop[1])

    allied_units = pygame.sprite.Group()
    enemy_units = pygame.sprite.Group()
    add_sprite_to_group(egg_soldier, allied_units)
    add_sprite_to_group(goop_soldier, enemy_units)
    sprite_to_display = None
    sprite_moving_current_coordinates = None

    while run:
        clock.tick(FPS)
        move_camera(pygame.mouse.get_pos())
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
                    if camera_mode:
                        cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                        mouse_sprite = MouseSprite(mouse_xy_to_map_xy(pygame.mouse.get_pos()))
                        mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, all_sprites, False)
                        if len(mouse_colliding) > 1:
                            # lol what
                            pass
                        elif len(mouse_colliding) == 1:
                            # display the unit information on the bottom screen
                            sprite_to_display = mouse_colliding[0]
                            if not sprite_to_display.hostile:
                                potential_cells_to_move = determine_legal_movement(sprite_to_display.movement, sprite_to_display.get_grid_coordinates())
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
                            print("here")
                            selecting_sprite_action_mode = False
                            selected_action_name = mouse_colliding[0].name
                            potential_cells_to_target = determine_legal_movement(sprite_to_display.get_action_range(selected_action_name),
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
                            else:
                                # the target was not successful, do not move on
                                # TODO: play a sound effect indicating an improper targeting
                                pass
                        else:
                            # TODO: play a sound effect indicating an improper targeting
                            pass
                if event.button == 3:
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
                    sprite_targeting_mode, potential_cells_to_target)
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
