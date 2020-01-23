from random import random

from pygame import *

from Configuration import Screen
from Entities import *
from Saves import load_settings, save
from Screens import MenuScreen


pygame.init()
pygame.display.set_caption('Zombie bombie')
screen = pygame.display.set_mode(Screen.size, pygame.RESIZABLE)

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

menu = MenuScreen(screen)
menu.render(all_sprites)

background = pygame.transform.scale(pygame.image.load("images/backgrounds/background_start.jpg"), Screen.size)
screen.blit(background, (0, 0))
cursor = Cursor(0, 0)
all_sprites.add(cursor)
pygame.display.flip()

enter_game = False
loaded = False

while not enter_game:
    menu.update(-1, -1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enter_game = True
            menu.enter_game()

        if event.type == pygame.MOUSEBUTTONUP:
            if menu.check_press(cursor) == 'new_game':
                enter_game = True
                menu.enter_game()
            elif menu.check_press(cursor) == 'resume':
                enter_game = True
                menu.enter_game()
            elif menu.check_press(cursor) == 'settings':
                pass
            elif menu.check_press(cursor) == 'exit':
                raise SystemExit

        if event.type == pygame.MOUSEMOTION:
            cursor.update(event.pos[0], event.pos[1])

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

running = True
flag = False
left_move = False
right_move = False
up_move = 10
down_move = 0
is_jump = False

# ------Game sprite initialization-------
if not loaded:
    background = pygame.transform.scale(pygame.image.load("images/backgrounds/background.jpg"), Screen.size)
    screen.blit(background, (0, 0))

    bullets = pygame.sprite.Group()
    zombies = pygame.sprite.Group()
    buildings = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    floor = Floor()
    all_sprites.add(floor)
    obstacles.add(floor)

    hero = Hero(Screen.width * 0.5, Screen.height * 0.8)
    all_sprites.add(hero)

    box1 = Box(Screen.width * 0.2, Screen.height * 0.8)
    all_sprites.add(box1)
    buildings.add(box1)

    box2 = Box(Screen.width * 0.8, hero.rect.y)
    all_sprites.add(box2)
    buildings.add(box2)

    cursor.kill()
    all_sprites.add(cursor)

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

            if event.key == pygame.K_3:
                if random() <= 0.5:
                    zombie = Zombie(0, Screen.height * 0.8)
                else:
                    zombie = Zombie(Screen.width, Screen.height * 0.8)
                all_sprites.add(zombie)
                zombies.add(zombie)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                is_jump = True

            if event.key == pygame.K_d:
                right_move = False

            if event.key == pygame.K_a:
                left_move = False

        if event.type == pygame.MOUSEMOTION:
            cursor.update(event.pos[0], event.pos[1])

    if is_jump:
        if up_move >= -10:
            neg = 0.9
            if up_move <= 0:
                neg = -1
            hero.rect.y -= (up_move ** 2 * 0.1 * neg)
            up_move -= 1
        else:
            is_jump = False
            hero.rect.y -= 3
            up_move = 9

    hero_cords = hero.rect.x, hero.rect.y
    hero.update(left_move, right_move)
    zombies.update(hero_cords, bullets, buildings)
    buildings.update(screen, zombies)
    bullets.update()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
