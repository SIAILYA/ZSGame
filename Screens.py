import pygame


class LoadingScreen:
    def __init__(self, screen: pygame.display):
        self.screen = screen

    def render(self):
        fon = pygame.transform.scale(pygame.image.load("images/fon.jpg"), size)
        self.screen.blit(fon, (0, 0))