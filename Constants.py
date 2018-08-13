SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MAP_WIDTH = 64
MAP_HEIGHT = 64
TILE_WIDTH = 64
TILE_HEIGHT = 32

MIN_SCROLL_X = -100
MIN_SCROLL_Y = -(MAP_HEIGHT * TILE_HEIGHT)/2 - 100
MAX_SCROLL_X = (MAP_WIDTH * TILE_WIDTH) - 400
MAX_SCROLL_Y = (MAP_HEIGHT * TILE_HEIGHT)/2 - 200


UI_ICON_SIZE = 64



VALID_CONSTRUCTION_SPOTS = {'1', '2'}

BUILD_MODE_ROAD = 1
BUILD_MODE_LANDFILL = 2
BUILD_MODE_DELETE = 3

COST_OF_ROAD = 50
COST_OF_LANDFILL = 100

RANDOM_CHANCE_OF_GARBAGE_GET = 1

FERTILE_CONSTANT = 8.2
DEATH_CONSTANT = 9
SECONDS_BETWEEN_GROWTH = 1
RATE_OF_TRASH = 1

GARBAGE_PER_LANDFILL_TILE = 15

SECONDS_PER_MONTH = 60
