import pygame
from ..constants import *
from ..generate import draw_text, draw_image, draw_connected


def pause(surf: pygame.Surface, clock: pygame.time.Clock, assets: dict, all_sprites: pygame.sprite.LayeredUpdates,
          score: int, status: dict):
    selected = 0
    texts = ["Resume", "Menu"]

    button_x = HALF_WIDTH
    text_y = 150

    last_enter = True
    last_up = False

    while True:
        clock.tick(FPS)

        if status["enter"] and not last_enter:
            return selected
        if status["up"] and not last_up:
            selected += 1
            selected %= len(texts)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        last_enter = status["enter"]
        last_up = status["up"]

        all_sprites.draw(surf)
        surf.blit(assets["transparent_bg"], (0, 0))
        draw_text(surf, assets["font"], str(score), 32, BLACK, 10, 0)
        draw_text(
            surf, assets["font"],
            "Paused",
            32, BLACK, HALF_WIDTH, text_y, centerx=True
        )
        button_y = text_y + 100
        for i in range(len(texts)):
            if i == selected:
                image = assets["selected_button"]
            else:
                image = assets["button"]
            draw_image(surf, image, button_x, button_y)
            draw_text(
                surf, assets["font"],
                texts[i],
                24, BLACK, button_x, button_y, centerx=True, centery=True
            )
            button_y += 75
        draw_connected(surf, assets["font"], status)
        pygame.display.update()
