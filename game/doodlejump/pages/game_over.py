import pygame
from ..constants import *
from ..sprites.doodle import Doodle
from ..generate import draw_text, draw_image


def game_over(surf: pygame.Surface, clock: pygame.time.Clock, assets: dict,
              all_sprites: pygame.sprite.LayeredUpdates, doodle: Doodle, score: int):
    drop, target_pos = HEIGHT * 2, HEIGHT // 3
    camera_y = drop + target_pos

    def _draw_moving_text():
        draw_text(
            surf, assets["font"],
            "Game Over !",
            32, RED, HALF_WIDTH, camera_y-50, centerx=True
        )
        draw_text(
            surf, assets["font"],
            f"Your score: {score}",
            32, BLACK, HALF_WIDTH, camera_y, centerx=True
        )

    # dropping animation
    while True:
        if (doodle.rect.y > HEIGHT + 100) and (camera_y <= target_pos):
            break
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        all_sprites.update()
        if camera_y > target_pos:
            for sprite in all_sprites:
                sprite.rect.y -= GG_SPEED
            camera_y -= GG_SPEED
        else:
            doodle.rect.y -= GG_SPEED

        surf.blit(assets["background"], (0, 0))
        all_sprites.draw(surf)
        _draw_moving_text()
        pygame.display.update()

    for sprite in all_sprites:
        sprite.kill()

    # choices
    selected = 0
    texts = ["Play Again", "Menu", "Exit"]

    button_x = HALF_WIDTH

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected -= 1
                    selected %= len(texts)
                elif event.key == pygame.K_DOWN:
                    selected += 1
                    selected %= len(texts)
                elif event.key == pygame.K_RETURN:
                    return selected

        surf.blit(assets["background"], (0, 0))
        _draw_moving_text()
        button_y = camera_y + 100
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
        draw_text(
            surf, assets["font"],
            "Use [up], [down], [enter] to select.",
            18, BLACK, HALF_WIDTH, HEIGHT-50, centerx=True
        )
        pygame.display.update()
