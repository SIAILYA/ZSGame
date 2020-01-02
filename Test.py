import pygame
import random
import time
import math

w = 1200
h = 600
fps = 60
a = -10
b = 15
bulletspeedx = 5
bulletspeedy = 5
wp = 25
hp = 50
wb = 10
hb = 10
fixspeed = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((wb, hb))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.right < 0 or self.rect.top > h or self.rect.left > w:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(w / 2, w)
        self.rect.y = random.randrange(10, h)
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > h + 10 or self.rect.left < -10 or self.rect.right > w + 10:
            self.rect.x = random.randrange(w - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 8)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((wp, hp))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.bottom = h - (hp / 2)
        self.speedy = 0
        self.i = 0
        self.isjump = False
        self.a = 0
        self.b = 0
        self.t = 0
        self.c = 0

    def update(self):
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        self.speedx = 0
        if self.isjump == False:
            self.speedy = b
        if key[pygame.K_LEFT] and key[pygame.K_LSHIFT]:
            self.speedx = -12
        elif key[pygame.K_LEFT]:
            self.speedx = -10
        if key[pygame.K_RIGHT] and key[pygame.K_LSHIFT]:
            self.speedx = 12
        elif key[pygame.K_RIGHT]:
            self.speedx = 10

        if self.rect.right > w - 40:
            self.rect.right = w - 40
        if self.rect.left < 0 + 40:
            self.rect.left = 0 + 40
        if self.rect.bottom > h - 40:
            self.rect.bottom = h - 40
            player.i = 0

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.speedy == a:
            self.i += 1
        if self.i == 15:
            self.isjump = False
            self.i -= 3
        if self.i == 0:
            self.isjump = True

    def Shoot(self):
        posx = pygame.mouse.get_pos()[0]
        posy = pygame.mouse.get_pos()[1]

        if posx > self.rect.centerx:
            self.a = posx - self.rect.right
            self.b = self.rect.centery - posy
            self.c = math.hypot(self.a, self.b)
            self.t = self.c / fixspeed
            speedx = self.a / self.t
            speedy = -self.b / self.t
            bullet = Bullet(self.rect.right, self.rect.centery, speedx, speedy)
            sprites.add(bullet)
            bullets.add(bullet)

        else:
            bullet = Bullet(self.rect.left, self.rect.centery)
            sprites.add(bullet)
            bullets.add(bullet)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

for i in range(2):
    mob = Mob()
    sprites.add(mob)
    mobs.add(mob)

# Цикл игры
running = True
while running:

    clock.tick(fps)

    # Ввод процесса (события)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player.Shoot()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player.isjump:
                    player.speedy = a
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.speedy = b
                player.isjump = False

    # Обновление
    sprites.update()

    playerhits = pygame.sprite.spritecollide(player, mobs, False)
    bullethits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    if playerhits:
        running = False
    for hit in bullethits:
        mob = Mob()
        sprites.add(mob)
        mobs.add(mob)

    # Рендеринг
    screen.fill(GREEN)
    sprites.draw(screen)
    pygame.display.flip()

pygame.quit()