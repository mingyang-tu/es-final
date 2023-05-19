import pygame
from .constants import *


def data2event(data):
    movement = 0
    if data["shot"] > 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}))
    if data["jump"] > 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
    if data["left"] > 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
        movement -= MOV_SPEED
    if data["right"] > 0:
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
        movement += MOV_SPEED
    # elif data == "RETURN":
    #     pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
    #     return 0
    return movement
