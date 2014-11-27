#!/usr/bin/env python
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


if __name__ == '__main__':
    pygame.init()
    pygame.time.set_timer(CAR_CREATION_EVENT, TIME_BETWEEN_CAR_CREATION_MS)

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
                sys.exit(0)
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
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    user_car.move_up()
                if event.key == K_DOWN:
                    user_car.move_down()
            elif event.type == KEYUP:
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
