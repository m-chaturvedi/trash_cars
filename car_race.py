###############################################i#########################################
###################################### car_race.py ######################################
try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    import numpy as np
    import utils
    from car import *
    import pdb
    import webcolors
    import logging
    from car_config import *
    # Imports constants/colors from Pygame
    from pygame.locals import *
except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)


def create_events():
    pygame.time.set_timer(CAR_CREATION_EVENT, TIME_BETWEEN_CAR_CREATION_MS)
    pygame.time.set_timer(CREATE_LOG_EVENT, TIME_BETWEEN_LOGGING_MS)

def start_pygame_create_surfaces():
    pygame.init()
    create_events()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("TrashCars")
    full_surface = pygame.Surface(screen.get_size())
    # converting to single pixel format
    full_surface = full_surface.convert()

    top_surface = full_surface.subsurface(TOP_SCREEN)
    top_surface.fill(TOP_SCREEN_COLOR)
    bottom_surface = full_surface.subsurface(BOTTOM_SCREEN)
    bottom_surface.fill(BOTTOM_SCREEN_COLOR)

    screen.blit(top_surface, (0,0))
    screen.blit(bottom_surface, BOTTOM_SCREEN[0])
    pygame.display.update()
    return screen, clock, full_surface, top_surface, bottom_surface


if __name__ == '__main__':
    if USING_NN:
        use_nn = utils.UseNN()

    screen, clock, full_surface, top_surface, bottom_surface = start_pygame_create_surfaces()
    car = Car(bottom_surface)
    car_sprites = pygame.sprite.RenderPlain(car)
    user_car = Car(bottom_surface, user_car=True)
    user_car_sprite = pygame.sprite.RenderPlain(user_car)

    pygame.display.flip()

    status = utils.UpdateStatus(top_surface)
    screen.blit(full_surface, status.rect, status.rect)

    while True:
        clock.tick(CLOCK_TICKS)

        for event in pygame.event.get():
            if event.type == QUIT:
                utils.logging.info("QUIT EVENT TRIGGERED")
                pygame.time.wait(1000)
                if not USING_NN:
                    utils.print_log()
                sys.exit(0)
            elif event.type == CREATE_LOG_EVENT:
                if not USING_NN:
                    utils.create_log(car_sprites,user_car)
                else:
                    motion = use_nn.use(car_sprites, user_car)
                    if motion == MOVE_UP: user_car.move_up()
                    if motion == MOVE_DOWN: user_car.move_down()
                    if motion == NO_MOVE: user_car.set_still()
            elif event.type == CAR_COLLISION_EVENT:
                status.update_text(COLLISION_MSG, static_msg=False)
                screen.blit(top_surface, (0,0))
                screen.blit(full_surface, status.rect, status.rect)
                pygame.event.post(pygame.event.Event(QUIT))
            elif event.type == CAR_CREATION_EVENT:
                new_car =  Car(bottom_surface)
                utils.logging.info("CAR_CREATION_EVENT TRIGGERED")
                new_car.add(car_sprites)
                status.update_text(Car.total_cars)
                screen.blit(top_surface, (0,0))
                screen.blit(full_surface, status.rect, status.rect)
                # pygame.display.flip()
            elif event.type == KEYDOWN and not USING_NN:
                if event.key == K_UP:
                    user_car.move_up()
                if event.key == K_DOWN:
                    user_car.move_down()
            elif event.type == KEYUP and not USING_NN:
                if event.key == K_UP or event.key == K_DOWN:
                    user_car.set_still()

        screen.blit(full_surface, user_car.rect, user_car.rect)
        for car_sprite in car_sprites.sprites():
            screen.blit(full_surface, car_sprite.rect, car_sprite.rect)

        car_sprites.update()
        user_car.update()
        car_sprites.draw(screen)
        user_car_sprite.draw(screen)
        Car.remove_if_outside(car_sprites)
        user_car.check_collision(car_sprites)
        pygame.display.update()
