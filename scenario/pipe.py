import pygame
import numpy as np
from scenario.ground import Ground


class Pipe(pygame.sprite.Sprite):
    width = 70
    spacing = 130

    def __init__(self, screen, x, y, width, height, pipe_top=False):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        self.image = pygame.image.load('./resources/pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        if pipe_top:
            self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 5

    def update(self):
        self.rect.x -= self.velocity

    @staticmethod
    def create(screen):
        screen_w = screen.get_width()
        screen_h = screen.get_height()

        delimit = screen_h / 4

        spacing_start = np.random.randint(
            delimit, 
            (screen_h - delimit) - Ground.height
        )

        top = Pipe(
            screen, 
            screen_w, 
            0,
            Pipe.width,
            spacing_start, 
            pipe_top=True
        )
        bottom_top = spacing_start + Pipe.spacing
        bottom_bottom = (screen_h - Ground.height) - bottom_top
        if bottom_top >= (screen_h - Ground.height):
            bottom_top = screen_h
            bottom_bottom = 0

        bottom = Pipe(
            screen, 
            screen_w, 
            bottom_top, 
            Pipe.width, 
            bottom_bottom
        )

        return top, bottom
