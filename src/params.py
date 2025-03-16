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
    
    TOWER_TARGET_RADIUS = 500
    # TODO: refine
    TOWER_MIN_RADIUS = 270

    SAVING_LIMIT = 200
    
    MIN_GOLD_FOR_MINE = 70
    # TODO: refine
    ENEMY_UNIT_SAFETY_DIST = 300
    
    # PlanStrategy
    TOWER_SHARE = 0.3
    BARRACKS_AMOUNT = 3
    
    # ReactStrategy
    TARGET_MINES = 3
    TARGET_TOWERS = 3
    TARGET_KNIGHTS_BARRACKS = 1
    TARGET_GIANTS_BARRACKS = 1
    
    ENEMY_KNIGHT_SAFETY_DIST = 400
    MIN_QUEEN_HEALTH = 10
    