import pygame
import pygame.event
import pygame.display
import pygame.image
import pygame.transform
import pygame.freetype
import random
import os


class Game():
    pygame.init()
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    TITLE_FONT = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'title.ttf'))
    # Title screen and menu font

    ROLE_FONT = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'role.ttf'))
    # Displays at the "crewmate/impostor" screen, called VCR OSD Mono

    ARIAL = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'text.ttf'))
    # Used for pretty much everything else

    players = []

    def start(self):
        if self.players == []:
            raise ValueError('There are no players.')

        random.choice(self.players).impostor = True

        self.init_window()

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    def init_window(self):
        self.WIN.fill((30, 30, 40))

        for player in Game.players:
            x, y = random.randint(
                100, self.WIDTH-100), random.randint(100, self.HEIGHT-100)

            self.WIN.blit(player.image, (x, y))
            nametag = self.ARIAL.render(
                player.name, size=self.HEIGHT/25, fgcolor=(255, 255, 255))
            self.WIN.blit(nametag[0], ((x-nametag[1][2] //
                          2) + (self.WIDTH//19)//2, y-self.HEIGHT/30))

        pygame.display.update()

    def add_player(self, name: str, color: str):
        for player in self.players:
            if name == player.name:
                raise ValueError(f'Name \'{name}\' has already been used.')
            if color == player.color:
                raise ValueError(f'Color \'{color}\' has already been used.')

        self.players.append(Player(self, name, color))


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
            'assets', 'imgs', self.color.lower()+'.png')), (self.game.WIDTH//19, self.game.HEIGHT//10))

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
    game.add_player('Sam', 'Red')

    game.start()
