import pygame
from .constants import *


def data2event(data):
    if data == "UP":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP}))
        return 0
    elif data == "DOWN":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN}))
        return 0
    elif data == "LEFT":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT}))
        return -MOV_SPEED
    elif data == "RIGHT":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT}))
        return MOV_SPEED
    elif data == "RETURN":
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RETURN}))
        return 0
    else:
        raise ValueError("Data Error!!")
