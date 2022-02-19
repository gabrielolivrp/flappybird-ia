from argparse import ArgumentParser
from game import game

if __name__ == '__main__':
    parser = ArgumentParser(
        description='A simulation of the neural network with genetic algorithms in the game flappy bird'
    )
    parser.add_argument('--population', '-p', type=int)
    parser.add_argument('--model', '-m', type=str)
    parser.add_argument('--training', '-t', action='store_true')
    args = parser.parse_args()

    if not args.training and args.model is None:
        print('[error]: model argument is required')
        exit(1)

    game(training=args.training, model=args.model, population=args.population)
