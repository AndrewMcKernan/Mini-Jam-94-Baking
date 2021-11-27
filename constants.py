WIDTH, HEIGHT = 1920, 1080  # dimensions of screen

GRID_WIDTH = 24

TILE_WIDTH = WIDTH // GRID_WIDTH
TILE_HEIGHT = TILE_WIDTH

GRID_HEIGHT = HEIGHT // TILE_HEIGHT

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3  # directional codes for walls

ZOOM_FACTOR = 3

FRAMES_PER_MOVE = 5

ZOOMED_MAZE_WIDTH = WIDTH * ZOOM_FACTOR
ZOOMED_MAZE_HEIGHT = HEIGHT * ZOOM_FACTOR

# colours
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
BLACK = (0, 0, 0)
PINK = (219, 13, 188)
ORANGE = (232, 121, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TRON = (0, 162, 232)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
TRANSPARENT = (217, 34, 232)

FPS = 60  # more needs to be done here when frames are dropped - at this point, it will simply slow down the game.