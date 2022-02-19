import pygame
import numpy as np
from scenario.ground import Ground
from network import NeuralNetwork


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, brain=None):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.images = [
            pygame.image.load('./resources/bluebird-upflap.png').convert_alpha(),
            pygame.image.load('./resources/bluebird-midflap.png').convert_alpha(),
            pygame.image.load('./resources/bluebird-downflap.png').convert_alpha()
        ]
        self.current_image = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 0.6
        self.lift = -6
        self.velocity = 0
        self.fitness = 0
        self.score = 0
        self.collided = False
        self.brain = brain
        if self.brain is None:
            self.brain = NeuralNetwork(
                input_dim=4, 
                hidden_neurons=3, 
                output_neurons=2
            )
    def up(self):
        self.velocity = self.lift

    def mutation(self):
        self.brain.mutation(0.5)

    def think(self, screen, pipes):
        target = None

        for index, pipe in enumerate(pipes):
            if pipe.rect.x + pipe.image.get_width() >= self.rect.x:
                target = pipes[index]
                break

        target_y = (target.image.get_height() + (target.spacing / 2))
        target_x = (target.rect.x + (target.width / 2))

        bird_x = self.rect.x + (self.image.get_width() / 2)
        bird_y = self.rect.y + (self.image.get_height() / 2)

        inputs = np.array([
            [
                target_x,
                target_y,
                bird_x,
                bird_y
            ]
        ])

        pygame.draw.line(
            screen, 
            (255, 0, 0),
            (bird_x, bird_y), 
            (target_x, target_y)
        )

        output = self.brain.predict(inputs)

        if output[0] > output[1]:
            self.up()

    def copy_brain(self):
        return self.brain.copy()

    def update(self):
        screen_h = self.screen.get_height()
        bird_h = self.image.get_height()

        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.y + bird_h >= screen_h - Ground.height:
            self.collided = True
            self.rect.y = screen_h - bird_h

        if self.rect.y <= 0:
            self.collided = True
            self.rect.y = 0

        if not self.collided:
            self.current_image = (self.current_image + 1) % 3
            self.image = self.images[self.current_image]
            self.score += 1

    @staticmethod
    def create_generation(screen, n, copy_bird=None):
        group = []

        for i in range(n):
            brain = None
            if copy_bird is not None:
                brain = copy_bird.copy_brain()
            bird = Bird(
                screen, 
                screen.get_width() / 3,
                screen.get_height() / 2, 
                brain=brain
            )
            if copy_bird is not None:
                bird.mutation()
            group.append(bird)
        return group

    def save_brain(self, path):
        return self.brain.save(path)

    def load_brain(self, path):
        self.brain.load(path)
