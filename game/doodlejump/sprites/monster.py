import pygame
import random
from ..constants import *


class Monster(pygame.sprite.Sprite):
    def __init__(self, images: list[pygame.Surface], y_range: tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(images)

        self.rect = self.image.get_rect()
        self.layer = 5

        self.radius = self.rect.height // 2

        self.rect.centerx = random.randint(30, WIDTH-30)
        self.rect.centery = random.randint(*y_range)

        self.speed_x = MONSTER_MAX_SPEED
        self.origin_x = self.rect.x

        self.dropping = False
        self.speed_y = 0
        self.acce_y = GRAVITY

    def update(self, move=0):
        self.speed_x += (self.origin_x - self.rect.x) * MONSTER_ACC_CONST
        self.rect.x += round(self.speed_x)

        if self.dropping:
            self.speed_y += self.acce_y
            self.rect.y += round(self.speed_y)

        if self.rect.top > HEIGHT:
            self.kill()
