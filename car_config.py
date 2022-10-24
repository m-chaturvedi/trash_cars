###############################################i###########################################
###################################### car_config.py ######################################
try:
    import sys
    import webcolors
    # Imports constants/colors from Pygame
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


SCREEN_SIZE = (1200,600)
TOP_SCREEN = ((0,0),(1200,128))
# Arbit way to give subsurface coords. The first tuple gives the top-left point.
# The second tuple gives the size.
BOTTOM_SCREEN = ((0,128), (1200, 472))
TOP_SCREEN_COLOR = webcolors.name_to_rgb("blue")
BOTTOM_SCREEN_COLOR = webcolors.name_to_rgb("yellow")
CLOCK_TICKS = 60

COLLISION_MSG = "COLISSION!! NICE TRY! BYE!"
GAME_START_MSG = "WELCOME TO TRASH CARS!! GAME STARTS!!"
CAR_CREATION_EVENT = USEREVENT + 1
CAR_COLLISION_EVENT = USEREVENT + 2
CREATE_LOG_EVENT = USEREVENT + 3

NUM_PRED_BEFORE_DECISION = 1
NN_TRAIN_FRACTION = 0.99
NN_HIDDEN_LAYER = 3
NN_FILLER_VALUE = [BOTTOM_SCREEN[1][0] + 50, TOP_SCREEN[1][1] + BOTTOM_SCREEN[1][1]/2]

USING_NN = True


SCALE_SPEEDS = 6
TIME_BETWEEN_LOGGING_MS = 500/SCALE_SPEEDS
TIME_BETWEEN_CAR_CREATION_MS = 7000/SCALE_SPEEDS
CAR_SPEED = 3*SCALE_SPEEDS
CAR_BOUNDARIES = 5
AI_CAR_FILE = 'ai_car.png'

USER_CAR_FILE = 'user_car.png'
USER_CAR_NUMBER = -1 # Should be negative
USER_CAR_SPEED = 2*SCALE_SPEEDS
PICKLE_FILE = 'data_1.log'
PRETTY_FILE = 'log_pretty_tmp.log'

OTHER_CARS = []
USER_CAR = []

MOVE_UP = -1
NO_MOVE = 0
MOVE_DOWN = 1
