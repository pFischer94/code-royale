import math

class Params:
    WIDTH = 1920
    HEIGHT = 1000
    CENTER = [int(WIDTH / 2), int(HEIGHT / 2)]
    
    # MAX_DIST_TO_MIDDLE = math.dist([0, 0], CENTER)
    # MAX_TOWER_DIST = MAX_DIST_TO_MIDDLE * 0.4
    # MAX_BARRACKS_DIST = MAX_DIST_TO_MIDDLE * 0.6
    
    # if MAX_TOWER_DIST >= MAX_BARRACKS_DIST:
    #     raise Exception("Invalid Params") 
    
    TOWER_SHARE = 0.3
    BARRACKS_AMOUNT = 3
    
    TOWER_TARGET_RADIUS = 350
    
    SAVING_LIMIT = 200