import pygame


class Ground(pygame.sprite.Sprite):
    height = 100

    def __init__(self, screen, x):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load('./resources/ground.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, 
            (screen.get_width(), Ground.height)
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = screen.get_height() - Ground.height
        self.velocity = 5

    def update(self):
        self.rect.x -= self.velocity
