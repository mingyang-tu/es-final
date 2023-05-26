import pygame
import os
import sys
import socket
import threading
import json

from .constants import *
from .sprites.doodle import Doodle
from .pages.game_over import game_over
from .pages.menu import menu
from .pages.pause import pause
from .generate import (
    generate_platform,
    generate_init_platform,
    generate_monster,
    draw_text,
    draw_connected
)
from .collide import (
    jump_platform,
    touch_monster,
    kill_monster
)
from .user_events import data2event


def load_assets(assets_root):
    assets = dict()
    assets["background"] = pygame.image.load(os.path.join(assets_root, "background.png")).convert()
    assets["transparent_bg"] = assets["background"].copy()
    assets["transparent_bg"].set_alpha(200)
    assets["green_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "green.png")).convert_alpha()
    assets["blue_pf"] = pygame.image.load(os.path.join(assets_root, "platforms", "blue.png")).convert_alpha()
    assets["doodle"] = pygame.image.load(os.path.join(assets_root, "doodles", "doodle.png")).convert_alpha()
    assets["doodle_shoot"] = pygame.image.load(os.path.join(assets_root, "doodles", "doodle_shoot.png")).convert_alpha()
    assets["button"] = pygame.image.load(os.path.join(assets_root, "buttons", "button.png")).convert_alpha()
    assets["selected_button"] = pygame.image.load(os.path.join(
        assets_root, "buttons", "selected_button.png")).convert_alpha()
    assets["spring"] = pygame.image.load(os.path.join(assets_root, "springs", "spring.png")).convert_alpha()
    assets["compressed_spring"] = pygame.image.load(os.path.join(
        assets_root, "springs", "compressed_spring.png")).convert_alpha()
    assets["bullet"] = pygame.image.load(os.path.join(assets_root, "bullet.png")).convert_alpha()
    assets["monsters"] = [
        pygame.image.load(os.path.join(assets_root, "monsters", f"monster{i}.png")).convert_alpha()
        for i in range(1, 4)
    ]

    assets["font"] = os.path.join(assets_root, "Gochi_Hand", "GochiHand-Regular.ttf")

    return assets


class Game:
    def __init__(self, host, port, assets_root="./doodlejump/assets/"):
        self.host = host
        self.port = port
        self.status = {
            "connected": False,
            "move": 0,
            "shot": False,
            "up": False,
            "down": False,
            "enter": False
        }
        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Doodle Jump")
        self.clock = pygame.time.Clock()

        self.assets = load_assets(assets_root)

        # initial settings
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()
        self.doodle = Doodle(self.assets["doodle"], self.assets["doodle_shoot"])

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.gameover = False
        self.showmenu = False
        self.touch_monster = False

    def update(self):
        ############### TODO ###############
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        s.settimeout(1)
        print(f'Bind {self.host}:{self.port}')
        while self.running:
            try:
                data, addr = s.recvfrom(1024)
                print("Data: ", data, end="\r")
                self.status["connected"] = True
                data2event(json.loads(data), self.status)
            except socket.timeout:
                self.status["connected"] = False
                print("Not received...", end="\r")
            except:
                pass
        s.close()
        print("\nServer closed.")
        ############### TODO ###############

    def init_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platform_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.monster_sprites = pygame.sprite.Group()

        self.doodle = Doodle(self.assets["doodle"], self.assets["doodle_shoot"])
        self.all_sprites.add(self.doodle)

        generate_init_platform(self.assets, [self.all_sprites, self.platform_sprites], HEIGHT-50)
        generate_platform(
            self.assets,
            [self.all_sprites, self.platform_sprites],
            (HEIGHT-100, -STAGE_LENGTH-BUFFER_LENGTH),
            1
        )
        generate_monster(
            self.assets,
            [self.all_sprites, self.monster_sprites],
            (-STAGE_LENGTH-BUFFER_LENGTH+MONSTER_SPACE, -STAGE_LENGTH-BUFFER_LENGTH)
        )

        self.camera_move = 0
        self.stage = 1
        self.score = 0
        self.gameover = False
        self.showmenu = False
        self.touch_monster = False

    def run(self):
        thread = threading.Thread(target=self.update)
        thread.start()

        self.showmenu = True
        last_enter = True

        while self.running:
            if self.gameover:
                close = game_over(
                    self.screen,
                    self.clock,
                    self.assets,
                    self.all_sprites,
                    self.doodle,
                    self.score,
                    self.status
                )
                self.gameover = False
                if close == 0:
                    self.init_game()
                    last_enter = True
                elif close == 1:
                    self.showmenu = True
                elif close == -1 or close == 2:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            if self.showmenu:
                close = menu(self.screen, self.clock, self.assets, self.status)
                if close == 0:
                    self.init_game()
                    last_enter = True
                elif close == -1 or close == 1:
                    break
                else:
                    raise ValueError("Unexpected value of [close]")

            self.clock.tick(FPS)

        # get inputs
            if (self.status["enter"] and not last_enter) or not self.status["connected"]:
                close = pause(self.screen, self.clock, self.assets, self.all_sprites, self.score, self.status)
                if close == 0:
                    pass
                elif close == 1:
                    self.showmenu = True
                elif close == -1:
                    self.running = False
                else:
                    raise ValueError("Unexpected value of [close]")
            if self.status["shot"]:
                self.doodle.shoot(self.assets["bullet"], [self.all_sprites, self.bullet_sprites])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.running:
                break

        # update game
            last_enter = self.status["enter"]

            self.all_sprites.update(self.status["move"])

            if not self.touch_monster:
                jump_platform(self.doodle, self.platform_sprites)
                self.score += kill_monster(self.monster_sprites, self.bullet_sprites)
                if touch_monster(self.doodle, self.monster_sprites):
                    self.touch_monster = True

            if self.doodle.rect.y > HEIGHT:
                self.gameover = True

            # move camera
            if self.doodle.rect.bottom < HALF_HEIGHT:
                diff = HALF_HEIGHT - self.doodle.rect.bottom
                self.camera_move += diff
                self.score += diff
                for sprite in self.all_sprites:
                    sprite.rect.y += diff
                if self.camera_move > STAGE_LENGTH:
                    self.stage += 1
                    bot = self.camera_move-STAGE_LENGTH-BUFFER_LENGTH
                    generate_platform(
                        self.assets,
                        [self.all_sprites, self.platform_sprites],
                        (bot, bot-STAGE_LENGTH),
                        self.stage
                    )
                    generate_monster(
                        self.assets,
                        [self.all_sprites, self.monster_sprites],
                        (bot, bot-STAGE_LENGTH)
                    )
                    self.camera_move = 0

        # display
            self.screen.blit(self.assets["background"], (0, 0))
            self.all_sprites.draw(self.screen)
            draw_text(self.screen, self.assets["font"], str(self.score), 32, BLACK, 10, 0)
            draw_connected(self.screen, self.assets["font"], self.status)
            pygame.display.update()

        self.running = False
        thread.join()
        print("Server thread exited.")
        pygame.quit()
        sys.exit()
