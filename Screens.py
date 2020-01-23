import pygame
from Configuration import Screen
from pygame import font


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, picture, function):
        pygame.sprite.Sprite.__init__(self)
        sprite_pic = pygame.image.load(f"images/buttons/{picture}")
        sprite_pic = pygame.transform.rotozoom(sprite_pic, 0, 1 / Screen.divider)
        self.image = sprite_pic
        self.rect = sprite_pic.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.hp = 5000
        self.function = function


class MenuScreen:
    def __init__(self, screen: pygame.display):
        self.buttons = pygame.sprite.Group()
        self.screen = screen
        self.button_coords = []

    def render(self, all_sprites):
        fon = pygame.transform.scale(pygame.image.load("images/backgrounds/background_start.jpg"), Screen.size)
        self.screen.blit(fon, (0, 0))
        for button in [('ng_button.png', Screen.width // 2, Screen.height * 0.1, 'new_game'),
                       ('r_button.png', Screen.width // 2, Screen.height * 0.26, 'resume'),
                       # ('s_button.png', Screen.width // 2, Screen.height * 0.42, 'settings'),
                       ('e_button.png', Screen.width // 2, Screen.height * 0.42, 'exit')]:
            sprite_button = Button(button[1], button[2], button[0], button[3])
            self.buttons.add(sprite_button)
            all_sprites.add(sprite_button)
            self.button_coords.append(button)
        self.buttons.draw(self.screen)

    def enter_game(self):
        for button in self.buttons:
            button.kill()

    def update(self, x, y):
        pygame.display.flip()
        if Screen.width * 0.4 <= x <= Screen.width * 0.6:
            print(self.button_coords)
            if y >= self.button_coords[2][2]:
                print('das')

    def check_press(self, cursor):
        if pygame.sprite.spritecollide(cursor, self.buttons, False):
            return pygame.sprite.spritecollide(cursor, self.buttons, False)[0].function
        return None
