from Players import *
import pygame
from pygame import *
from constantes import *
from random import random


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


pygame.init()
size = width, height = 1366 // 2, 768 // 2
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption('Zombie bombie')

fon = pygame.transform.scale(pygame.image.load("images/fon.jpg"), size)
screen.blit(fon, (0, 0))

hero = Hero(width * 0.5, height * 0.8)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
buildings = pygame.sprite.Group()

pygame.display.flip()
running = True
flag = False
v = 100

clock = pygame.time.Clock()

camera = Camera()

left_move = False
right_move = False
up_move = 10
is_jump = False
down_move = 0

all_sprites.add(hero)

box1 = Box(width * 0.2, height * 0.8)
all_sprites.add(box1)
buildings.add(box1)

box2 = Box(width * 0.8, hero.rect.y)
all_sprites.add(box2)
buildings.add(box2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            player_x, player_y = hero.rect.x, hero.rect.y
            bullet = Bullet(player_x, player_y, x, y)
            all_sprites.add(bullet)
            bullets.add(bullet)

        if event.type == pygame.MOUSEBUTTONUP:
            flag = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right_move = True

            if event.key == pygame.K_a:
                left_move = True

            if event.key == pygame.K_w:
                is_jump = True

            if event.key == pygame.K_3:
                if random() <= 0.5:
                    zombie = Zombie(0, height * 0.8)
                else:
                    zombie = Zombie(width, height * 0.8)
                all_sprites.add(zombie)
                zombies.add(zombie)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right_move = False

            if event.key == pygame.K_a:
                left_move = False

    if is_jump:
        if up_move >= -10:
            neg = 1
            if up_move < 0:
                neg = -1
            hero.rect.y -= up_move ** 2 * 0.1 * neg
            up_move -= 1
        else:
            is_jump = False
            up_move = 10

    screen.blit(fon, (0, 0))
    hero_cords = hero.rect.x, hero.rect.y
    all_sprites.draw(screen)

    hero.update(left_move, right_move)
    zombies.update(hero_cords, bullets, buildings)
    buildings.update(screen, zombies)
    bullets.update()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
