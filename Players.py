import pygame
from math import atan, pi

class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, x, y, time=10):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        if x > player_x:
            self.image = pygame.transform.rotate(self.image, 360 - atan((y - player_y) /
                                                                        (x - player_x)) * 180 / pi)
        else:
            self.image = pygame.transform.rotate(self.image, 180 - atan((y - player_y) /
                                                                        (x - player_x)) * 180 / pi)
        self.rect = self.image.get_rect()
        self.rect.y = player_y
        self.rect.x = player_x
        # TODO сделать одинаковую скорость пуль!
        self.speed_x = (self.rect.x - x) / time
        self.speed_y = (self.rect.y - y) / time

    def update(self, *args):
        self.rect.x -= self.speed_x
        self.rect.y -= self.speed_y

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/zombie.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 4

    def update(self, hero_cords, bullets):
        if hero_cords[0] > self.rect.x:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        if pygame.sprite.spritecollide(self, bullets, True):
            self.hp -= 1
            if self.hp == 0:
                self.kill()
