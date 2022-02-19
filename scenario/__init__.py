import pygame
from scenario.pipe import Pipe
from scenario.ground import Ground


class Scenario(object):
    def __init__(self, screen):
        self.screen = screen
        self.grounds = None
        self.pipes = None
        self._count_pipe = 0
        self.background_img = None
        self._setup()

    def _remove_pipes(self):
        self.pipes.remove(self._first_pipe())
        self.pipes.remove(self._first_pipe())

    def _first_pipe(self):
        return self.pipes.sprites().__getitem__(0)

    def _add_pipe(self):
        self.pipes.add(Pipe.create(self.screen))

    def _first_ground(self):
        return self.grounds.sprites().__getitem__(0)

    def _remove_ground(self):
        self.grounds.remove(self._first_ground())

    def _add_ground(self, x=None):
        self.grounds.add(
            Ground(self.screen, self.screen.get_width() if x is None else x))

    def reset(self):
        self._count_pipe = 0
        self.pipes.empty()

    def run(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background_img, (0, 0))

        if len(self.pipes.sprites()) > 0:
            if self._first_pipe().rect.x + Pipe.width <= 0:
                self._remove_pipes()

        if self._count_pipe == 0:
            self._count_pipe = 50
            self._add_pipe()

        if self._first_ground().rect.x + self.screen.get_width() <= 0:
            self._remove_ground()
            self._add_ground()

        self._count_pipe -= 1

    def _setup(self):
        self.background_img = pygame.image.load('./resources/background.png')
        self.grounds = pygame.sprite.Group()
        self.pipes = pygame.sprite.Group()
        self._add_ground(0)
        self._add_ground()
        