try:
    import sys
    # Imports constants/colors from Pygame
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

COLLISION_MSG = "COLISSION!! NICE TRY! BYE!"
GAME_START_MSG = "GAME STARTS!!"
CAR_CREATION_EVENT = USEREVENT + 1
CAR_COLLISION_EVENT = USEREVENT + 2
