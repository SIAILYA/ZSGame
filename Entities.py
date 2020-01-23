import pygame
from math import atan, pi
import time
from Configuration import Screen
from Сonstantes import *
clock = pygame.time.Clock()

pygame.init()
hurt = pygame.mixer.Sound("sounds/hurt.wav")


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        hero_pic = pygame.image.load("images/entities/main_hero.png")
        self.hero_pic = pygame.transform.rotozoom(hero_pic, 0, hero_const)
        self.hero_pic_l = pygame.transform.flip(self.hero_pic, 1, 0)
        self.image = self.hero_pic
        self.rect = hero_pic.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.direction = 0
        self.score = 0
        self.hp = 1000

    def update(self, left_move=None, right_move=None):
        if left_move:
            self.rect.x -= 2
            self.image = self.hero_pic_l
        if right_move:
            self.rect.x += 2
            self.image = self.hero_pic


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, x, y, time=10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/entities/bullet.png")
        self.image = pygame.transform.rotozoom(self.image, 0, bullet_const)
        try:
            if x > player_x:
                self.image = pygame.transform.rotate(self.image, 360 - atan((y - player_y) /
                                                                            (x - player_x)) * 180 / pi)
            else:
                self.image = pygame.transform.rotate(self.image, 180 - atan((y - player_y) /
                                                                            (x - player_x)) * 180 / pi)
        except ZeroDivisionError:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.y = player_y
        self.rect.x = player_x
        # TODO сделать одинаковую скорость пуль!
        self.speed_x = 0
        if not self.speed_x:
            self.speed_x = (self.rect.x - x) / time
            self.speed_y = (self.rect.y - y) / time

    def update(self, *args):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.main = pygame.image.load("images/entities/zombie.gif")
        self.main = pygame.transform.rotozoom(self.main, 0, Screen.width / 1366 / 3.5)
        self.rect = self.main.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 4
        self.image = self.main

    def update(self, hero_cords, bullets, buildings, screen, hero, zombies):
        if not pygame.sprite.spritecollide(self, buildings, False):
            if hero_cords[0] > self.rect.x:
                self.rect.x += 1
            else:
                self.rect.x -= 1
        if pygame.sprite.spritecollide(self, bullets, True):
            self.hp -= 1
            hurt.play()
            damaged = pygame.transform.rotozoom(pygame.image.load(f"images/entities/zombie_damaged{4 - self.hp}.png"),
                                                0, Screen.width / 1366 / 3.5)
            self.image = damaged
            if self.hp == 0:
                hero.score += 5
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect()
                self.kill()

        if pygame.sprite.spritecollideany(self, buildings):
            pygame.sprite.spritecollideany(self, buildings).hp -= 1
            if pygame.sprite.spritecollideany(self, buildings).hp == 0:
                pygame.sprite.spritecollideany(self, buildings).kill()

        if pygame.sprite.spritecollideany(self, hero):
            pygame.sprite.spritecollideany(self, hero).hp -= 1
            if pygame.sprite.spritecollideany(self, hero).hp == 0:
                pygame.sprite.spritecollideany(self, hero).kill()
                font = pygame.font.Font(None, 100)
                text = font.render("You died", 1, (100, 255, 100))
                screen.blit(text, (Screen.width * 0.4, Screen.height * 0.2))


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        box_pic = pygame.image.load("images/entities/box.png")
        box_pic = pygame.transform.rotozoom(box_pic, 0, 0.2 / Screen.divider)
        self.image = box_pic
        self.rect = box_pic.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.hp = 5000

    def update(self, screen, zombies):
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.hp // 100), 1, (100, 255, 100))
        screen.blit(text, (self.rect.x, self.rect.y))


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        floor_pic = pygame.image.load("images/backgrounds/floor.png")
        floor_pic = pygame.transform.rotozoom(floor_pic, 0, 1 / Screen.divider)
        self.image = floor_pic
        self.rect = floor_pic.get_rect()
        self.rect.x = 0
        self.rect.y = Screen.height - self.rect.height


class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.mouse.set_visible(False)
        pygame.sprite.Sprite.__init__(self)
        cursor_pic = pygame.image.load("images/entities/cursor.png")
        cursor_pic = pygame.transform.rotozoom(cursor_pic, 0, 0.5)
        self.image = cursor_pic
        self.rect = cursor_pic.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2

    def update(self, x, y):
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
