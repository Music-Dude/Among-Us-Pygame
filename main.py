import pygame
import random
import os


class Game():
    WIDTH, HEIGHT = 1920, 1080
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    players = set()

    def start(self):
        self.init_window()

        random.choice(self.players).imposter = True

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    def init_window(self):
        self.WIN.fill((255, 255, 255))

        for player in Game.players:
            self.WIN.blit(player.image, (random.randint(
                100, self.WIDTH), random.randint(100, self.HEIGHT)))

        pygame.display.update()

    def add_player(self, name: str, color: str):
        for player in self.players:
            if name == player.name:
                raise ValueError(f'Name \'{name}\' has already been used.')
            if color == player.color:
                raise ValueError(f'Color \'{color}\' has already been used.')

        self.players.add(Player(self, name, color))


class Player():
    colors = {'Red', 'Blue', 'Cyan', 'Pink', 'Purple', 'Green',
              'Black', 'White', 'Orange', 'Yellow', 'Lime', 'Brown'}

    def __init__(self, game: Game, name, color):
        self.game = game
        self.name = name
        if not color in Player.colors:
            raise ValueError(f'Invalid color. Must be one of {Player.colors}.')
        self.color = color
        self.impostor = False

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', self.color.lower()+'.png')), (self.game.WIDTH//18, self.game.HEIGHT//10))

    def __repr__(self):
        return f'Player(\'{self.name}\', {self.color}, impostor={self.impostor})'

    def kill(self, player):
        if self.impostor:
            del player
            return True
        else:
            return False


if __name__ == '__main__':
    game = Game()
    game.add_player('Bob', 'Blue')
    game.add_player('Joe', 'Red')
    game.add_player('Jim', 'Green')
    game.add_player('Jeff', 'Lime')
    game.add_player('Sam', 'Yellow')
    game.add_player('William', 'Purple')

    game.start()
