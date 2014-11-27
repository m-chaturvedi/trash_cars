try:
    import pygame
    import pdb
    import os
    import sys
    import utils
    import random
    from car_config import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)

# Global Variables
CAR_SPEED = 3
CAR_BOUNDARIES = 5
AI_CAR_FILE = 'ai_car.png'

USER_CAR_FILE = 'user_car.png'
USER_CAR_NUMBER = -1 # Should be negative
USER_CAR_SPEED = 5


class Car(pygame.sprite.Sprite) :
    """Cars that will move across the screen
    Returns: car object
    Functions: update, calcnewpos
    Attributes: area, speed, car_num, rect"""

    total_cars = 0
    collision_list = []

    def __init__(self, motion_surface, user_car=False):
        pygame.sprite.Sprite.__init__(self)
        self._newpos = (0,0)
        self.abs_offset_y = motion_surface.get_abs_offset()[1]
        if user_car:
            self._make_user_car(motion_surface)
            utils.logging.info("USER CAR CREATED, # %s", self.car_number)
        else:
            self._make_ai_cars(motion_surface)
            utils.logging.info("CAR #%s CREATED", self.car_number)

    def __del__(self):
        utils.logging.info("CAR #%s KILLED" % self.car_number)

    def _make_ai_cars(self, motion_surface):
        self.image, self.rect = utils.load_png(AI_CAR_FILE)
        self.area = motion_surface.get_rect()
        self.hit = 0
        Car.total_cars += 1
        self.car_number = Car.total_cars
        self.speed = CAR_SPEED
        self.rect.midright = self.area.midright
        self.rect.x += motion_surface.get_abs_offset()[0]
        self.rect.y += motion_surface.get_abs_offset()[1] + self.random_movable_positions_y()
        self.update_motion_plan()

    def _make_user_car(self, motion_surface):
        self.image, self.rect = utils.load_png(USER_CAR_FILE)
        self.area = motion_surface.get_rect()
        self.hit = 0
        self.car_number = USER_CAR_NUMBER
        self.speed = USER_CAR_SPEED
        self.rect.midleft = self.area.midleft
        self.rect.x += motion_surface.get_abs_offset()[0]
        self.rect.y += motion_surface.get_abs_offset()[1]

    @classmethod
    def get_total_num_cars(cls):
        return cls.total_cars

    @classmethod
    def remove_if_outside(cls, car_sprites):
        for car_sprite in car_sprites.sprites():
            if car_sprite.area.left  > car_sprite.rect.right +2:
                utils.logging.info("CAR # %s OUT"% car_sprite.car_number)
                car_sprite.remove()
                car_sprite.kill()

    def _is_user_car(self):
        return self.car_number == USER_CAR_NUMBER

    # Refractor this
    def update(self):
        new_rect = self.rect.move(self._newpos)
        area_bottom = self.area.bottom + self.abs_offset_y
        area_top = self.area.top + self.abs_offset_y

        if ((self.rect.top >= area_top + CAR_BOUNDARIES)
                    and (self.rect.bottom <= area_bottom - CAR_BOUNDARIES)):
            self.rect = self.rect.move(self._newpos)
        else:
            if not (self.rect.top >= area_top + CAR_BOUNDARIES):
                self.rect = self.rect.move((0,1))
            if not (self.rect.bottom <= area_bottom - CAR_BOUNDARIES):
                self.rect = self.rect.move((0,-1))




    def random_movable_positions_y(self):
        half_car_y = self.rect.size[1]/2
        half_area_y = self.area.size[1]/2
        return random.randint( -half_area_y + half_car_y + CAR_BOUNDARIES,
                               half_area_y - half_car_y - CAR_BOUNDARIES)


    def check_collision(self, car_sprites):
        collided_sprites_list = pygame.sprite.spritecollide(self, car_sprites, False)
        if collided_sprites_list:
            assert(len(collided_sprites_list) == 1)
            collided_sprite = collided_sprites_list[0]
            if not (collided_sprite in self.collision_list):
                self.collision_list.append(collided_sprite)
                pygame.event.post(pygame.event.Event(CAR_COLLISION_EVENT))
                utils.logging.info("CAR # %s COLLIDED" % collided_sprite.car_number)

    def update_motion_plan(self):
        # We're moving right to left
        dx = -self.speed
        dy = 0
        self._newpos = (dx, dy)

    def move_up(self):
        dx = 0
        dy = -self.speed
        self._newpos = (dx, dy)

    def move_down(self):
        dx = 0
        dy = +self.speed
        self._newpos = (dx, dy)

    def set_still(self):
        self._newpos = (0,0)
