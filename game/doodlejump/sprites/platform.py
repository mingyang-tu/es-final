import pygame
import random
from ..constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, y_range: tuple[int, int], type: str):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.type = type

        self.rect = self.image.get_rect()
        self.layer = 1

        self.rect.centerx = random.randint(0, WIDTH)
        self.rect.centery = random.randint(*y_range)

        if random.random() < SPECIAL_BLUE_PROB:
            self.blue_speed = random.choice(SPECIAL_BLUE)
        else:
            self.blue_speed = BLUE_SPEED

        if random.random() >= 0.5:
            self.speed_x = self.blue_speed
        else:
            self.speed_x = -self.blue_speed

    def update(self, move=0):
        if self.type == "blue":
            self.rect.x += self.speed_x
            if self.rect.left <= 0:
                self.speed_x = self.blue_speed
            elif self.rect.right >= WIDTH:
                self.speed_x = -self.blue_speed

        if self.rect.top > HEIGHT:
            self.kill()


class Spring(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, compressed: pygame.Surface, position: tuple[int, int], left_right: tuple[int, int], speed_x: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = compressed
        self.uncompressed = image

        self.rect = self.image.get_rect()
        self.layer = 0

        self.rect.centerx = position[0]
        self.rect.bottom = position[1]

        self.left, self.right = left_right

        self.blue_speed = abs(speed_x)
        self.speed_x = speed_x

    def relocate(self, image: pygame.Surface):
        self.image = image
        new_pos = self.rect.centerx, self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.centerx = new_pos[0]
        self.rect.bottom = new_pos[1]

    def update(self, move=0):
        if self.speed_x != 0:
            self.rect.x += self.speed_x
            self.left += self.speed_x
            self.right += self.speed_x
            if self.left <= 0:
                self.speed_x = self.blue_speed
            elif self.right >= WIDTH:
                self.speed_x = -self.blue_speed

        if self.rect.bottom > HEIGHT:
            self.kill()
