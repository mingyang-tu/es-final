import pygame
from .constants import *


def data2event(data, status):
    for event in ["shot", "enter", "up", "down"]:
        status[event] = data[event] > 0

    movement = 0
    if data["left"] > 0:
        movement -= MOV_SPEED
    if data["right"] > 0:
        movement += MOV_SPEED
    status["move"] = movement
