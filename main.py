from Players import *
import pygame
from pygame import *
from constantes import *
from random import random


pygame.init()
size = width, height = 1366 // 2, 768 // 2
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption('Zombie bombie')

screen.fill((0, 0, 0))
hero = Hero(width * 0.5, height * 0.8)
hero_pic = pygame.image.load("images/main_hero.png")
hero_pic = pygame.transform.rotozoom(hero_pic, 0, hero_const)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
pygame.display.flip()
running = True
flag = False
v = 100
clock = pygame.time.Clock()

left_move = False
right_move = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            player_x, player_y = hero.x, hero.y
            bullet = Bullet(player_x, player_y, x, y)
            all_sprites.add(bullet)
            bullets.add(bullet)

        if event.type == pygame.MOUSEBUTTONUP:
            flag = False

        if event.type == pygame.MOUSEMOTION and flag:
            pos = event.pos
            hero.x += pos[0] - x
            hero.y += pos[1] - y
            x = pos[0]
            y = pos[1]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right_move = True

            if event.key == pygame.K_a:
                left_move = True

            if event.key == pygame.K_4:
                zombie = Zombie(width * random(), height * 0.8)
                all_sprites.add(zombie)
                zombies.add(zombie)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right_move = False

            if event.key == pygame.K_a:
                left_move = False

    if left_move:
        hero.x -= 2
    if right_move:
        hero.x += 2

    screen.fill((171, 205, 255))
    screen.blit(hero_pic, (hero.x, hero.y))
    hero_cords = hero.x, hero.y
    all_sprites.draw(screen)
    all_sprites.update(hero_cords, bullets)
    pygame.display.flip()
    clock.tick(120)
pygame.quit()