import pygame
from typing import Any, Union
from ..constants import *


class Doodle(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, img_shoot: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.images = [image, pygame.transform.flip(image, True, False)]
        self.imgs_shoot = [img_shoot, pygame.transform.flip(img_shoot, True, False)]
        self.imgs_dead = [pygame.transform.flip(image, False, True), pygame.transform.flip(image, True, True)]

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.layer = 10

        self.radius = self.rect.height // 2

        self.rect.center = (HALF_WIDTH, HEIGHT*2//3)

        self.speed_y = 0

        self.acce_y = GRAVITY
        self.jump_speed = -JUMP_SPEED

        self.direction = 0

        self.shoot_time = 0
        self.shooting = False

        self.dead = False

    def update(self, move=0):
        now = pygame.time.get_ticks()
        if self.shooting and now - self.shoot_time > SHOOT_TIME:
            shift = SHOOT_SHIFT if self.direction == 0 else -SHOOT_SHIFT
            self.relocate(
                self.images[self.direction],
                self.rect.centerx+shift, self.rect.bottom
            )
            self.shooting = False

        if move > 0:
            self.flip_lr(0)
            self.rect.x += move
        if move < 0:
            self.flip_lr(1)
            self.rect.x += move

        self.speed_y += self.acce_y
        self.rect.y += round(self.speed_y)

        if self.rect.centerx < 0:
            self.rect.centerx = WIDTH
        if self.rect.centerx > WIDTH:
            self.rect.centerx = 0

    def jump(self):
        self.speed_y = self.jump_speed

    def jump_spring(self):
        self.speed_y = self.jump_speed * 1.5

    def shoot(self, img_bullet: pygame.Surface, sprites: list[Union[pygame.sprite.Group, Any]]):
        if not self.shooting:
            shift = SHOOT_SHIFT if self.direction == 0 else -SHOOT_SHIFT
            self.relocate(
                self.imgs_shoot[self.direction],
                self.rect.centerx-shift, self.rect.bottom
            )

        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top)
        for sprite in sprites:
            sprite.add(bullet)

        self.shoot_time = pygame.time.get_ticks()
        self.shooting = True

    def touch_monster(self):
        self.dead = True
        self.speed_y = 0
        self.image = self.imgs_dead[self.direction]

    def flip_lr(self, flip_direction: int):
        if flip_direction != self.direction:
            self.direction = flip_direction
            if self.dead:
                self.image = self.imgs_dead[self.direction]
            elif self.shooting:
                self.image = self.imgs_shoot[self.direction]
            else:
                self.image = self.images[self.direction]

    def relocate(self, image: pygame.Surface, x: int, y: int):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.layer = 9

        self.radius = self.rect.height // 2

        self.speed_y = -BULLET_SPEED

    def update(self, move=0):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
