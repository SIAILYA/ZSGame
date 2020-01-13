from random import random

from pygame import *

from Configuration import Screen
from Players import *
from Screens import MenuScreen

pygame.init()
screen = pygame.display.set_mode(Screen.size, pygame.RESIZABLE)
pygame.display.set_caption('Zombie bombie')

fon = pygame.transform.scale(pygame.image.load("images/fon.jpg"), Screen.size)
screen.blit(fon, (0, 0))

hero = Hero(Screen.width * 0.5, Screen.height * 0.8)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
buildings = pygame.sprite.Group()
menu = MenuScreen(screen)
menu.render()
pygame.display.flip()

enter_game = False

while not enter_game:
    menu.update()

running = False
flag = False
v = 100

clock = pygame.time.Clock()

left_move = False
right_move = False
up_move = 10
is_jump = False
down_move = 0

all_sprites.add(hero)

box1 = Box(Screen.width * 0.2, Screen.height * 0.8)
all_sprites.add(box1)
buildings.add(box1)

box2 = Box(Screen.width * 0.8, hero.rect.y)
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
                    zombie = Zombie(0, Screen.height * 0.8)
                else:
                    zombie = Zombie(Screen.width, Screen.height * 0.8)
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
