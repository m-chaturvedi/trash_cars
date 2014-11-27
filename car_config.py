try:
    import sys
    import webcolors
    # Imports constants/colors from Pygame
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


SCREEN_SIZE = (1200,512)
TOP_SCREEN = ((0,0),(1200,128))
# Arbit way to give subsurface coords. The first tuple gives the top-left point.
# The second tuple gives the size.
BOTTOM_SCREEN = ((0,128), (1200, 384))
TOP_SCREEN_COLOR = webcolors.name_to_rgb("green")
BOTTOM_SCREEN_COLOR = webcolors.name_to_rgb("yellow")
CLOCK_TICKS = 60
TIME_BETWEEN_CAR_CREATION_MS = 1600

COLLISION_MSG = "COLISSION!! NICE TRY! BYE!"
GAME_START_MSG = "GAME STARTS!!"
CAR_CREATION_EVENT = USEREVENT + 1
CAR_COLLISION_EVENT = USEREVENT + 2


CAR_SPEED = 3
CAR_BOUNDARIES = 5
AI_CAR_FILE = 'ai_car.png'

USER_CAR_FILE = 'user_car.png'
USER_CAR_NUMBER = -1 # Should be negative
USER_CAR_SPEED = 5
