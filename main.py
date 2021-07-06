from operator import attrgetter
import pygame.transform
import pygame.freetype
import pygame.display
import pygame.image
import pygame.event
import pygame.time
import pygame.rect
import pygame.key
import random
import math
import os


class Button():
    def __init__(self, game, image, pos: int):
        self.game = game
        self.SIZE = game.WIDTH//11

        positions = (
            ((self.game.WIDTH-(self.game.WIDTH//9)),
             self.game.HEIGHT-(self.game.WIDTH//6.5)),
            ((self.game.WIDTH-(self.game.WIDTH//9)),
             self.game.HEIGHT-(self.game.WIDTH//4)),
            ((self.game.WIDTH-(self.game.WIDTH//5)),
             self.game.HEIGHT-(self.game.WIDTH//6.5)),
        )

        self.pos = positions[pos]

        self.icon = pygame.transform.scale(image, (self.SIZE, self.SIZE))
        self.btn = pygame.rect.Rect(
            self.pos[0], self.pos[1], self.SIZE, self.SIZE)

        game.buttons.append(self)


class Game():
    pygame.init()
    players = []
    buttons = []

    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    VEL = 5
    # Player movement speed
    FPS = 60
    # Set this higher for your monitor

    TITLE_FONT = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'title.ttf'))
    # Title screen and menu font

    ROLE_FONT = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'role.ttf'))
    # Displays at the "crewmate/impostor" screen, called VCR OSD Mono

    ARIAL = pygame.freetype.Font(
        os.path.join('assets', 'fonts', 'text.ttf'))
    # Used for pretty much everything else

    def start(self):
        if self.players == []:
            raise ValueError('There are no players.')

        for player in self.players:
            if player.you:
                self.YOU = player

        random.choice(self.players).impostor = True
        # Set impostor

        self.draw_buttons()

        self.YOU.x, self.YOU.y = random.randint(
            100, self.WIDTH-100), random.randint(100, self.HEIGHT-100)

        self.main()

    def main(self):
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.report.btn.collidepoint(event.pos):
                            print('Report clicked')
                        if self.YOU.impostor:
                            if self.sabotage.btn.collidepoint(event.pos):
                                print('Sabotage clicked')
                            elif self.kill.btn.collidepoint(event.pos):
                                self.YOU.kill()
                        else:
                            if self.use.btn.collidepoint(event.pos):
                                print('Use clicked')

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.YOU.y -= self.VEL
            if keys[pygame.K_a]:
                self.YOU.x -= self.VEL
            if keys[pygame.K_s]:
                self.YOU.y += self.VEL
            if keys[pygame.K_d]:
                self.YOU.x += self.VEL

            self.draw_window()

    def draw_window(self):
        self.WIN.fill((30, 30, 40))

        for player in Game.players:
            self.WIN.blit(player.image, (player.x, player.y))

            nametag = self.ARIAL.render(
                player.name, size=self.HEIGHT/25, fgcolor=(255, 255, 255))

            self.WIN.blit(nametag[0], ((player.x-nametag[1][2] //
                          2) + (self.WIDTH//19)//2, player.y-self.HEIGHT/30))

        for button in self.buttons:
            self.WIN.blit(button.icon, button.pos)

        pygame.display.update()

    def draw_buttons(self):
        self.report = Button(self, pygame.image.load(
            os.path.join('assets', 'imgs', 'buttons', 'Report.png')), 1)

        if self.YOU.impostor:
            self.sabotage = Button(self, pygame.image.load(
                os.path.join('assets', 'imgs', 'buttons', 'Sabotage.png')), 0)
            self.kill = Button(self, pygame.image.load(
                os.path.join('assets', 'imgs', 'buttons', 'Kill.png')), 2)
            self.use = None
        else:
            self.use = Button(self, pygame.image.load(
                os.path.join('assets', 'imgs', 'buttons', 'Use.png')), 0)
            self.sabotage = None
            self.kill = None

    def add_player(self, name: str, color: str, you: bool = False):
        for player in self.players:
            if name == player.name:
                raise ValueError(f'Name \'{name}\' has already been used.')
            if color == player.color:
                raise ValueError(f'Color \'{color}\' has already been used.')

        self.players.append(Player(self, name, color, you))


class Player():
    colors = {'Red', 'Blue', 'Cyan', 'Pink', 'Purple', 'Green',
              'Black', 'White', 'Orange', 'Yellow', 'Lime', 'Brown'}

    def __init__(self, game: Game, name, color, you):
        self.x, self.y = Game.WIDTH//2, Game.HEIGHT//2
        self.game = game
        self.name = name
        self.you = you
        if not color in Player.colors:
            raise ValueError(f'Invalid color. Must be one of {Player.colors}.')
        self.color = color
        self.impostor = False

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(
            'assets', 'imgs', 'players', self.color + '.png')), (self.game.WIDTH//19, self.game.HEIGHT//10))

    def __repr__(self):
        return f'Player(\'{self.name}\', {self.color}, impostor={self.impostor})'

    def kill(self):
        nearest = self.get_nearest_player()
        if nearest:
            self.game.players.remove(nearest)

    def get_nearest_player(self):
        ps = self.game.players.copy()
        ps.remove(self)
        try:
            return min(ps, key=lambda p: math.sqrt((self.x-p.x)**2) + ((self.y-p.y)**2))
        except:
            return


if __name__ == '__main__':
    game = Game()
    game.add_player('Bob', 'Blue', you=True)
    game.add_player('Joe', 'Green')

    game.start()
