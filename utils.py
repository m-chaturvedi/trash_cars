try:
    import pygame
    import pdb
    import os
    import sys
    import logging
    import webcolors
    from car_config import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


class UpdateStatus:
    top_surface = None
    font_color = webcolors.name_to_rgb("red")
    font_size = 36
    static_text = "NUMBER OF CARS "
    top_color = None

    def __init__(self, top_surface, TOP_SCREEN_COLOR):
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




