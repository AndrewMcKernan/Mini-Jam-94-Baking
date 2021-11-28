WIDTH, HEIGHT = 1280, 720  # dimensions of screen

GRID_WIDTH = 26

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3  # directional codes for walls

MOVEMENT_OPTIONS = (UP, DOWN, LEFT, RIGHT)

ZOOM_FACTOR = 3

FRAMES_PER_MOVE = 5

TILE_WIDTH = 80
TILE_HEIGHT = TILE_WIDTH

GRID_HEIGHT = 22 + 4  # 4 on bottom made of water

ZOOMED_MAP_WIDTH = GRID_WIDTH * TILE_WIDTH
ZOOMED_MAP_HEIGHT = GRID_HEIGHT * TILE_HEIGHT

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