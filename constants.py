WIDTH, HEIGHT = 1920, 1080  # dimensions of screen

GRID_WIDTH = 72

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3  # directional codes for walls

MOVEMENT_OPTIONS = (UP, DOWN, LEFT, RIGHT)

ZOOM_FACTOR = 3

FRAMES_PER_MOVE = 5

ZOOMED_MAP_WIDTH = WIDTH * ZOOM_FACTOR
ZOOMED_MAP_HEIGHT = HEIGHT * ZOOM_FACTOR

TILE_WIDTH = ZOOMED_MAP_WIDTH // GRID_WIDTH
TILE_HEIGHT = TILE_WIDTH

GRID_HEIGHT = ZOOMED_MAP_HEIGHT // TILE_HEIGHT

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

FPS = 30  # more needs to be done here when frames are dropped - at this point, it will simply slow down the game.

CAMERA_SPEED = 40 # moves this many pixels per frame