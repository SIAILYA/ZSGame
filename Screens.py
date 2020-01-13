import pygame
from Configuration import Screen


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, picture):
        pygame.sprite.Sprite.__init__(self)
        sprite_pic = pygame.image.load(f"images/{picture}")
        sprite_pic = pygame.transform.rotozoom(sprite_pic, 0, 1 / Screen.divider)
        self.image = sprite_pic
        self.rect = sprite_pic.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y
        self.hp = 5000


class MenuScreen:
    def __init__(self, screen: pygame.display):
        self.screen = screen

    def render(self):
        fon = pygame.transform.scale(pygame.image.load("images/fon.jpg"), Screen.size)
        self.screen.blit(fon, (0, 0))
        buttons = pygame.sprite.Group()
        for button in [('ng_button.png', Screen.width // 2, 100 / Screen.divider),
                       ('r_button.png', Screen.width // 2, 200 / Screen.divider),
                       ('s_button.png', Screen.width // 2, 300 / Screen.divider)]:
            sprite_button = Button(button[1], button[2], button[0])
            buttons.add(sprite_button)
        buttons.draw(self.screen)

    def update(self):
        pygame.display.flip()