import os, sys
import pygame
from constants import *
from draw_text import drawText

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


#BUDDY_IMAGE = pygame.image.load(os.path.join('assets', 'septo.png')).convert()
#BUDDY_IMAGE.set_colorkey(TRANSPARENT)

MAP_IMAGES = dict()

#pygame.mixer.music.load(os.path.join('assets', 'Spy.mp3'))
#pygame.mixer.music.set_volume(0.1)
#pygame.mixer.music.play(-1)

#BUDDY = pygame.transform.scale(BUDDY_IMAGE, (BUDDY_WIDTH, BUDDY_HEIGHT))
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


def draw_window(cursor_xy, fps):
    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

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

    pygame.display.update()


def game():
    restart = False
    clock = pygame.time.Clock()
    title_mode = True
    run = True
    zoomed = False
    frames = 0
    frames_string = ''
    time_ms = 0
    game_begin_time = pygame.time.get_ticks()  # the time that the game actually began
    start_time = pygame.time.get_ticks()  # the time that the maze we're on began
    text_needing_acknowledgement = []  # structured like [ (COLOR, 'text')) ]
    cursor_coordinates = (0, 0)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # handle events
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    continue
                if event.key == pygame.K_w:
                    print(cursor_coordinates)
                    if cursor_coordinates[1] > 0:
                        cursor_coordinates = (cursor_coordinates[0], cursor_coordinates[1] - 1)
                if event.key == pygame.K_a:
                    print(cursor_coordinates)
                    if cursor_coordinates[0] > 0:
                        cursor_coordinates = (cursor_coordinates[0] - 1, cursor_coordinates[1])
                if event.key == pygame.K_s:
                    print(cursor_coordinates)
                    if cursor_coordinates[1] < GRID_HEIGHT:
                        cursor_coordinates = (cursor_coordinates[0], cursor_coordinates[1] + 1)
                if event.key == pygame.K_d:
                    print(cursor_coordinates)
                    if cursor_coordinates[0] < GRID_WIDTH:
                        cursor_coordinates = (cursor_coordinates[0] + 1, cursor_coordinates[1])

        draw_window(coordinates_to_xy(cursor_coordinates), frames_string)

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
