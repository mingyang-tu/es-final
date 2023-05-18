import pygame
from .constants import *
from .sprites.doodle import Doodle


def jump_platform(doodle: Doodle, platform_sprites: pygame.sprite.Group):
    if doodle.speed_y > 0:
        hits = pygame.sprite.spritecollide(doodle, platform_sprites, False)
        for hit in hits:
            if doodle.rect.bottom <= hit.rect.bottom:
                if hit.layer == 0:
                    doodle.jump_spring()
                    hit.relocate(hit.uncompressed)
                    return
                elif hit.layer == 1:
                    doodle.jump()


def kill_monster(monster_sprites: pygame.sprite.Group, bullet_sprites: pygame.sprite.Group):
    score = 0
    hits = pygame.sprite.groupcollide(monster_sprites, bullet_sprites, True, True, pygame.sprite.collide_circle)
    for _ in hits:
        score += MONSTER_SCORE
    return score


def touch_monster(doodle: Doodle, monster_sprites: pygame.sprite.Group):
    hits = pygame.sprite.spritecollide(doodle, monster_sprites, False, pygame.sprite.collide_circle)
    for hit in hits:
        if doodle.rect.bottom <= hit.rect.centery:
            hit.dropping = True
            doodle.jump()
        else:
            doodle.touch_monster()
            return True
    return False
