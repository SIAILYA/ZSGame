from random import random

from pygame import *
import time
from Configuration import Screen
from Entities import *
from Saves import save, load_settings
from Screens import MenuScreen

# Инициализация пигейма
pygame.init()
pygame.display.set_caption('Zombie bombie')
screen = pygame.display.set_mode(Screen.size, pygame.RESIZABLE)

# Создание фона
background = pygame.transform.scale(pygame.image.load("images/backgrounds/background_start.jpg"), Screen.size)
screen.blit(background, (0, 0))

# Загрузка звука выстрела
gun_shot = pygame.mixer.Sound("sounds/shot.wav")

# Объявление глобальных переменных
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

menu = MenuScreen(screen)
menu.render(all_sprites)
hero = Hero(Screen.width * 0.5, Screen.height * 0.8)
box1 = Box(Screen.width * 0.2, Screen.height * 0.8)
box2 = Box(Screen.width * 0.8, Screen.height * 0.8)
cursor = Cursor(0, 0)
all_sprites.add(cursor)

score = 0

pygame.display.flip()

enter_game = False

# Меню игры
while not enter_game:
    menu.update(-1, -1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enter_game = True
            running = False
            menu.enter_game()

        if event.type == pygame.MOUSEBUTTONUP:
            if menu.check_press(cursor) == 'new_game':
                enter_game = True
                running = True
                menu.enter_game()
            elif menu.check_press(cursor) == 'resume':
                enter_game = True
                running = True
                # Загрузка статистики
                hero.score, box1.hp, box2.hp = load_settings()
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
    # Выставление фпс
    clock.tick(120)

flag = False
left_move = False
right_move = False
up_move = 10
down_move = 0
is_jump = False

# ------Game sprite initialization-------
background = pygame.transform.scale(pygame.image.load("images/backgrounds/background.jpg"), Screen.size)
screen.blit(background, (0, 0))

# Объявление шрифта
font = pygame.font.Font(None, 40)
text = font.render(str(score), 1, (255, 255, 255))
screen.blit(text, (Screen.width * 0.2, Screen.height * 0.2))

# Создание групп под спрайты
bullets = pygame.sprite.Group()
zombies = pygame.sprite.Group()
buildings = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
main_hero = pygame.sprite.Group()

# Создание спрайтов и добавление их в группы
floor = Floor()
all_sprites.add(floor)
obstacles.add(floor)

main_hero.add(hero)
all_sprites.add(hero)

all_sprites.add(box1)
buildings.add(box1)

all_sprites.add(box2)
buildings.add(box2)

cursor.kill()
all_sprites.add(cursor)

# Время кулдауна
last_time_ms = int(round(time.time() * 1000))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save([hero.score, box1.hp, box2.hp])
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and hero:
                x, y = event.pos
                gun_shot.play()
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

    diff_time_ms = int(round(time.time() * 1000)) - last_time_ms

    if diff_time_ms >= 1200000 / (hero.score + 200):
        last_time_ms = int(round(time.time() * 1000))
        if random() <= 0.5:
            zombie = Zombie(0, Screen.height * 0.8)
        else:
            zombie = Zombie(Screen.width, Screen.height * 0.8)

        all_sprites.add(zombie)
        zombies.add(zombie)

    hero_cords = hero.rect.x, hero.rect.y
    hero.update(left_move, right_move)
    zombies.update(hero_cords, bullets, buildings, screen, main_hero, zombies, all_sprites, hero)

    bullets.update()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    buildings.update(screen, zombies)
    text = font.render("Score:" + " " + str(hero.score), 1, (255, 0, 0))
    screen.blit(text, (Screen.width * 0.02, Screen.height * 0.02))
    pygame.display.flip()
    clock.tick(230)

pygame.quit()
