###############################################i######################################
###################################### utils.py ######################################
try:
    import pygame
    import pdb
    import os
    import sys
    import logging
    import webcolors
    from car_config import *
    import time
    import pickle
    import run_nn
    import numpy as np
    from itertools import chain
    from collections import Counter
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_coords(car_sprites, offset=(0,0)):
    other_car_coords = []
    for car in car_sprites.sprites():
        if car.alive() :
            other_car_coords.append((car.rect.x - offset[0], car.rect.y - offset[1]))
    return other_car_coords

def create_log(car_sprites, user_car):
    other_car_coords = get_coords(car_sprites)
    OTHER_CARS.append(other_car_coords)
    USER_CAR.append((user_car.rect.x, user_car.rect.y, user_car.state))

def print_log():
    log_file = open(PRETTY_FILE, "w+")
    for user_car, other_cars in zip(USER_CAR, OTHER_CARS):
        log_file.write(_print_helper(user_car))
        log_file.write("\n")
        for other_car in other_cars:
            log_file.write(_print_helper(other_car))
        log_file.write("\n")
    log_file.close()

    with open(PICKLE_FILE, 'w') as f:
        pickle.dump([OTHER_CARS, USER_CAR], f)

def _print_helper(car):
    if len(car) == 2:
        return repr(car[0]).rjust(6) + repr(car[1]).rjust(6)
    return repr(car[0]).rjust(6) + repr(car[1]).rjust(6) + repr(car[2]).rjust(6)

# This function has been taken from a Pyagame tutorial
# at https://www.pygame.org/docs/tut/tom/games6.html.
def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    return image, image.get_rect()

class UseNN:
    nnet = None
    motion_list = []
    def __init__(self):
        self.nnet, self.D = run_nn.run_nn()

    def use(self, car_sprites, user_car):
        coords_list = [user_car.rect.y - TOP_SCREEN[1][1], TOP_SCREEN[1][1]
                       + BOTTOM_SCREEN[1][1] - user_car.rect.y] \
                      +\
                      list(chain.from_iterable(get_coords
                                               (car_sprites,
                                                offset=(user_car.rect.x, user_car.rect.y))))

        coords_ar = coords_list + NN_FILLER_VALUE*((self.D - len(coords_list))/2)

        coords_ar = np.squeeze(np.array(coords_ar))
        pred_motion = np.rint(np.squeeze(self.nnet.use(coords_ar)))

        if len(UseNN.motion_list) == NUM_PRED_BEFORE_DECISION: UseNN.motion_list = []
        UseNN.motion_list.append(pred_motion)

        if len(UseNN.motion_list) == NUM_PRED_BEFORE_DECISION:
            return Counter(UseNN.motion_list).most_common(1)[0][0]
        else:
            return user_car.state


class UpdateStatus:
    top_surface = None
    font_color = webcolors.name_to_rgb("red")
    font_size = 36
    static_text = "NUMBER OF CARS "
    top_color = None

    def __init__(self, top_surface):
        self.top_surface = top_surface
        self.font = pygame.font.Font(None, self.font_size)
        text = self.font.render(GAME_START_MSG, 1, self.font_color)
        self.rect = text.get_rect()
        self.rect.centerx = top_surface.get_rect().centerx
        self.rect.centery = top_surface.get_rect().centery
        self.top_surface.blit(text, self.rect)
        self.top_color = TOP_SCREEN_COLOR

    def update_text(self, msg, static_msg=True):
        if static_msg:
            text = self.font.render(self.static_text + str(msg), 1, self.font_color)
        else:
            text = self.font.render(str(msg), 1, self.font_color)
        self.rect = text.get_rect()
        self.rect.centerx = self.top_surface.get_rect().centerx
        self.rect.centery = self.top_surface.get_rect().centery
        self.top_surface.fill(self.top_color)
        self.top_surface.blit(text, self.rect)




