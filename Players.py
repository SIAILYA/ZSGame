import pygame
from math import atan, pi
from constantes import *
import time

clock = pygame.time.Clock()


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        hero_pic = pygame.image.load("images/main_hero.png")
        hero_pic = pygame.transform.rotozoom(hero_pic, 0, hero_const)
        self.image = hero_pic
        self.rect = hero_pic.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self, left_move=None, right_move=None):
        if left_move:
            self.rect.x -= 2

        if right_move:
            self.rect.x += 2


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, x, y, time=10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.rotozoom(self.image, 0, hero_const * 0.8)
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
        if not self.speed_x:
            self.speed_x = (self.rect.x - x) / time
            self.speed_y = (self.rect.y - y) / time

    def update(self, *args):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/zombie.gif")
        self.image = pygame.transform.rotozoom(self.image, 0, hero_const * 0.1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 4

    def update(self, hero_cords, bullets, buildings):
        if not pygame.sprite.spritecollide(self, buildings, False):
            if hero_cords[0] > self.rect.x:
                self.rect.x += 1
            else:
                self.rect.x -= 1
        if pygame.sprite.spritecollide(self, bullets, True):
            self.hp -= 1
            if self.hp == 0:
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect = self.image.get_rect()
                self.kill()


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        box_pic = pygame.image.load("images/box.png")
        box_pic = pygame.transform.rotozoom(box_pic, 0, 0.1)
        self.image = box_pic
        self.rect = box_pic.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.hp = 5000

    def update(self, screen, zombies):
        font = pygame.font.Font(None, 50)
        text = font.render(str(self.hp // 100), 1, (100, 255, 100))
        screen.blit(text, (self.rect.x, self.rect.y))
        if pygame.sprite.spritecollide(self, zombies, False):
            self.hp -= 1
            if self.hp == 0:
                self.kill()
