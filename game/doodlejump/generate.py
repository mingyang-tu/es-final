import pygame
import random
from typing import Any, Union
from .constants import *
from .sprites.platform import Platform, Spring
from .sprites.monster import Monster


def draw_image(surf: pygame.Surface, image: pygame.Surface, x: int, y: int):
    rect = image.get_rect()
    rect.centerx = x
    rect.centery = y
    surf.blit(image, rect)


def draw_text(surf: pygame.Surface, font_name: str, text: str,
              size: int, color: tuple[int, int, int], x: int, y: int,
              centerx: bool = False, centery: bool = False):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if centerx:
        text_rect.centerx = x
    else:
        text_rect.x = x
    if centery:
        text_rect.centery = y
    else:
        text_rect.y = y
    surf.blit(text_surface, text_rect)


def generate_init_platform(assets: dict, sprites: list[Union[pygame.sprite.Group, Any]], y: int):
    space = WIDTH // 9
    for i in range(5):
        platform = Platform(assets["green_pf"], (0, HEIGHT), "green")
        platform.rect.x = i * space * 2
        platform.rect.y = y
        for sprite in sprites:
            sprite.add(platform)


def generate_platform(assets: dict, sprites: list[Union[pygame.sprite.Group, Any]],
                      y_range: tuple[int, int], difficulty: int):
    if difficulty > 1:
        if random.random() < ALL_BLUE_PROB or difficulty == 5:
            blue_prob = 1.
        else:
            blue_prob = BLUE_PROB
    else:
        blue_prob = 0.

    if difficulty > 4:
        difficulty = random.randint(2, 4)

    if difficulty == 1:
        spring_prob = SPRING_PROB / 2
    else:
        spring_prob = SPRING_PROB

    platforms = {"green": assets["green_pf"], "blue": assets["blue_pf"]}

    for i in range(y_range[0], y_range[1], -100):
        min_i = max(i-100, y_range[1])
        for _ in range(5 - difficulty):
            if random.random() > blue_prob:
                pf = "green"
            else:
                pf = "blue"
            platform = Platform(platforms[pf], (min_i, i), pf)
            for sprite in sprites:
                sprite.add(platform)
            if random.random() < spring_prob:
                position = random.randint(platform.rect.left+10, platform.rect.right-10), platform.rect.top+1
                spring = Spring(
                    assets["spring"],
                    assets["compressed_spring"],
                    position,
                    (platform.rect.left, platform.rect.right),
                    platform.speed_x if platform.type == "blue" else 0
                )
                for sprite in sprites:
                    sprite.add(spring)


def generate_monster(assets: dict, sprites: list[Union[pygame.sprite.Group, Any]],
                     y_range: tuple[int, int]):

    for i in range(y_range[0], y_range[1], -MONSTER_SPACE):
        min_i = max(i-MONSTER_SPACE, y_range[1])
        if (i - min_i < MONSTER_SPACE / 2) or (random.random() > MONSTER_PROB):
            continue
        monster = Monster(assets["monsters"], (min_i, i))
        for sprite in sprites:
            sprite.add(monster)
