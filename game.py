import pygame
import logging
import keras
from scenario import Scenario
from scenario.bird import Bird

# init pygame and config logging
pygame.init()
logging.basicConfig(
    level=logging.INFO, 
    filename='info.log',
    format='%(asctime)s, %(message)s'
)

# global variables
generation = 1


def best_of_generation(birds):
    s = 0
    for bird in birds:
        s += bird.score

    for bird in birds:
        bird.fitness = bird.score / s

    fitness, score = -1, -1
    best = None
    for bird in birds:
        if fitness < bird.fitness:
            fitness = bird.fitness
            best = bird

        if score < bird.score:
            score = bird.score

    logger(best)

    return best, score, fitness


def next_generation(screen, birds, population):
    best, _, _ = best_of_generation(birds)
    return Bird.create_generation(screen, population, copy_bird=best)


def logger(bird):
    global generation
    keras.backend.clear_session()
    path_model = f'./training/model-{generation}.h5'
    bird.save_brain(path_model)
    logging.info(f'{generation}, {bird.score}, {bird.fitness}, {path_model}')


def game(training, model, population=10):
    global generation

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption('Flappy bird')
    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    bird = pygame.sprite.GroupSingle()
    scenario = Scenario(screen)

    birds = []
    bird_number = 1
    best_score = 0

    if training:
        birds = Bird.create_generation(screen, population)
        bird.add(birds[0])
    else:
        bird.add(Bird(screen, screen.get_width() / 3, screen.get_height() / 2))
        bird.sprite.load_brain(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if training:
                    best_of_generation(birds)
                running = False

        scenario.run()
        scenario.pipes.update()
        scenario.grounds.update()
        bird.update()
        scenario.pipes.draw(screen)
        bird.draw(screen)
        scenario.grounds.draw(screen)

        bird.sprite.think(screen, scenario.pipes.sprites())

        if pygame.sprite.spritecollide(bird.sprite, scenario.pipes, False) or bird.sprite.collided:
            if training:
                bird.empty()
                scenario.reset()
                if bird_number == population:
                    birds = next_generation(screen, birds, population)
                    bird.add(birds[0])
                    bird_number = 1
                    generation += 1
                    best_score = 0
                else:
                    bird.add(birds[bird_number])
                    bird_number += 1
            else:
                running = False
                print('game over')

        if best_score < bird.sprite.score:
            best_score = bird.sprite.score

        if training:
            screen.blit(
                font.render(f'Generation: {generation}', True, (0, 0, 0)), 
                dest=(10, 20)
            )
            screen.blit(
                font.render(f'Population: {population}', True, (0, 0, 0)), 
                dest=(10, 35)
            )
            screen.blit(
                font.render(f'Bird number: {bird_number}', True, (0, 0, 0)),
                dest=(10, 50)
            )
            screen.blit(
                font.render(f'The best score: {best_score}', True, (0, 0, 0)), 
                dest=(10, 65)
            )

        screen.blit(
            font.render(f'Score: {bird.sprite.score}', True, (0, 0, 0)), 
            dest=(10, 5)
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
