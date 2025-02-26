import math

class Params:
    WIDTH = 1920
    HEIGHT = 1000
    MIDDLE = [WIDTH / 2, HEIGHT / 2]
    
    MAX_DIST_TO_MIDDLE = math.dist([0, 0], MIDDLE)
    MAX_TOWER_DIST = MAX_DIST_TO_MIDDLE / 3
    MAX_BARRACKS_DIST = MAX_DIST_TO_MIDDLE / 3 * 2
    
    TOWER_TARGET_RADIUS = 500