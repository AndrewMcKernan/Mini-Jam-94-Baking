import os, sys
import pygame
from constants import *
from draw_text import drawText
from sprites import AlliedUnit, HostileUnit, UnitType, MouseSprite

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

pygame.font.init()  # for writing text to the screen
pygame.mixer.init()  # for sound

pygame.display.set_caption("Mini Jam 94: Baking")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

ZOOMED_MAZE = pygame.surface.Surface((ZOOMED_MAZE_WIDTH, ZOOMED_MAZE_HEIGHT))
camera = pygame.Rect((ZOOMED_MAZE_WIDTH // 2 - WIDTH // 2, ZOOMED_MAZE_HEIGHT // 2 - HEIGHT // 2), (WIDTH, HEIGHT))

BACKGROUND = pygame.Rect(0, 0, WIDTH, HEIGHT)
ZOOMED_BACKGROUND = pygame.Rect(0, 0, ZOOMED_MAZE_WIDTH, ZOOMED_MAZE_HEIGHT)


EGG_IMAGE = pygame.image.load(os.path.join('assets', 'egg.png')).convert()
EGG_IMAGE.set_colorkey(TRANSPARENT)

MOUSE_IMAGE = pygame.image.load(os.path.join('assets', 'mouse.png')).convert()
MOUSE_IMAGE.set_colorkey(TRANSPARENT)

MAP_IMAGES = dict()

#pygame.mixer.music.load(os.path.join('assets', 'Spy.mp3'))
#pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play(-1)

EGG_SURFACE = pygame.transform.scale(EGG_IMAGE, (TILE_WIDTH, TILE_HEIGHT))
MOUSE_SURFACE = pygame.transform.scale(MOUSE_IMAGE, (200, 200))
#ZOOMED_BUDDY = pygame.transform.scale(BUDDY_IMAGE, (ZOOMED_BUDDY_WIDTH, ZOOMED_BUDDY_HEIGHT))

TEXT_FONT = pygame.font.SysFont('lucidaconsole', 40)
DESC_FONT = pygame.font.SysFont('lucidaconsole', 20)
CELL_FONT = pygame.font.SysFont('lucidaconsole', 10)


def draw_cursor(x, y):
    pygame.draw.line(WIN, YELLOW, (x + 5, y + 5), (x + 5 + TILE_WIDTH // 3, y + 5))  # top left right line
    pygame.draw.line(WIN, YELLOW, (x + 5, y + 5), (x + 5, y + 5 + TILE_HEIGHT // 3))  # top left down line

    pygame.draw.line(WIN, YELLOW, (x + TILE_WIDTH - 5, y + 5), (x + TILE_WIDTH - TILE_WIDTH // 3 - 5, y + 5))  # top right left line
    pygame.draw.line(WIN, YELLOW, (x + TILE_WIDTH - 5, y + 5), (x + TILE_WIDTH - 5, y + 5 + TILE_HEIGHT // 3))  # top right down line

    pygame.draw.line(WIN, YELLOW, (x + 5, y + TILE_HEIGHT - 5), (x + 5 + TILE_WIDTH // 3, y + TILE_HEIGHT - 5))  # bottom left right line
    pygame.draw.line(WIN, YELLOW, (x + 5, y + TILE_HEIGHT - 5), (x + 5, y + TILE_HEIGHT - TILE_HEIGHT // 3 - 5))  # bottom left up line

    pygame.draw.line(WIN, YELLOW, (x + TILE_WIDTH - 5, y + TILE_HEIGHT - 5), (x + TILE_WIDTH - TILE_WIDTH // 3 - 5, y + TILE_HEIGHT - 5))  # bottom right left line
    pygame.draw.line(WIN, YELLOW, (x + TILE_WIDTH - 5, y + TILE_HEIGHT - 5), (x + TILE_WIDTH - 5, y + TILE_HEIGHT - TILE_HEIGHT // 3 - 5))  # bottom right up line


def coordinates_to_xy(coordinates):
    return coordinates[0] * TILE_WIDTH, coordinates[1] * TILE_HEIGHT

def mouse_pos_to_grid_coords(mouse_pos):
    return mouse_pos[0] // TILE_WIDTH, mouse_pos[1] // TILE_HEIGHT


def draw_window(cursor_xy, fps, allied_units, sprite_to_display):
    pygame.draw.rect(WIN, GRAY, pygame.Rect(0, 0, WIDTH, HEIGHT))

    bottom_left_rect = pygame.Rect(0, HEIGHT - 200, 200, 200)
    middle_rect = pygame.Rect(200, HEIGHT - 150, WIDTH - 400, 150)
    bottom_right_rect = pygame.Rect(WIDTH - 200, HEIGHT - 200, 200, 200)


    x = 0
    while x < WIDTH:
        pygame.draw.line(WIN, RED, (x, 0), (x, HEIGHT))
        x += TILE_WIDTH
    y = 0
    while y < HEIGHT:
        pygame.draw.line(WIN, RED, (0, y), (WIDTH, y))
        y += TILE_HEIGHT

    draw_cursor(cursor_xy[0], cursor_xy[1])

    drawText(WIN, fps, WHITE, pygame.Rect(5, 5, 300, 300), TEXT_FONT, True)

    allied_units.draw(WIN)

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

    pygame.display.update()


all_sprites = pygame.sprite.Group()


def add_sprite_to_group(sprite, group):
    group.add(sprite)
    # do not add the sprite twice if the group given is all_sprites
    if not group == all_sprites:
        all_sprites.add(sprite)


def game():
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

    starting_xy = coordinates_to_xy((GRID_WIDTH // 2, GRID_HEIGHT // 2))

    egg_soldier = AlliedUnit(EGG_IMAGE, TILE_WIDTH, TILE_HEIGHT, UnitType.EGG, starting_xy[0], starting_xy[1])

    allied_units = pygame.sprite.Group()
    add_sprite_to_group(egg_soldier, allied_units)
    sprite_to_display = None

    while run:
        clock.tick(FPS)
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
                    cursor_grid_coordinates = mouse_pos_to_grid_coords(pygame.mouse.get_pos())
                    mouse_sprite = MouseSprite(pygame.mouse.get_pos())
                    mouse_colliding = pygame.sprite.spritecollide(mouse_sprite, all_sprites, False)
                    if len(mouse_colliding) > 1:
                        # lol what
                        pass
                    elif len(mouse_colliding) == 1:
                        # display the unit information on the bottom screen
                        sprite_to_display = mouse_colliding[0]
                    else:
                        # no unit is being hovered
                        sprite_to_display = None
                if event.button == 3:
                    # right click
                    sprite_to_display = None
                # as per the jam restrictions, these are the only allowed buttons

            # escape should be allowed, right?
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    continue
        if not run:
            continue
        draw_window(coordinates_to_xy(cursor_grid_coordinates), frames_string, allied_units, sprite_to_display)

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
