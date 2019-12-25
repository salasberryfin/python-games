import pygame
import random
pygame.init()


HEIGHT = 640
WIDTH = 420
RATE = 60

class Screen():

    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

    def display(self):
        return pygame.display.set_mode((self.width,
                                        self.height))

    def size(self):
        return (self.width, self.height)

    def clock(self):
        return pygame.time.Clock()

class Board():

    def __init__(self, x_start, y_start, thickness, display):
        self.x_start = x_start
        self.y_start = y_start
        self.thickness = thickness
        self.width = display[0] - 2 * x_start - thickness + 1
        self.height = display[1] - 2 * y_start - thickness + 1

    def rect(self):
        return pygame.Rect(self.x_start,
                           self.y_start,
                           self.width,
                           self.height)

    def food(self):
        return pygame.Rect(random.randint(self.x_start, self.width),
                           random.randint(self.y_start, self.height),
                           12,
                           12)

class Player():

    def __init__(self, mvt, display, width=8, height=8):
        self.head_mvt = mvt
        self.display = display
        self.width = width
        self.height = height
        head_x = display[0]/2
        head_y = display[1]/2
        self.parts = [self.PlayerPiece(head_x,
                                       head_y,
                                       mvt=mvt)]

    def grow(self, x, y):
        self.parts.append(self.PlayerPiece(x,
                                           y))

    class PlayerPiece():
    
        def __init__(self, x, y, mvt=(0, 0), width=12, height=12):
            self.x_pos = x
            self.y_pos = y
            self.mvt = mvt
            self.width = width
            self.height = height
            self.rect = self.rectangle()

        def rectangle(self):
            return pygame.Rect(self.x_pos,
                               self.y_pos,
                               self.width,
                               self.height)


class GameObjects(dict):

    def __init__(self, *args, **kwargs):
        super(GameObjects, self).__init__(*args, **kwargs)
        self.__dict__ = self


def create():
    screen = Screen(HEIGHT, WIDTH, RATE)
    display = screen.display()
    clock = screen.clock()
    snake = Player((0, 0), screen.size())
    snake_parts = snake.parts
    board = Board(5, 5, 2, screen.size())
    rect = board.rect()
    
    return GameObjects(screen=screen,
                       display=display,
                       clock=clock,
                       snake=snake,
                       snake_parts=snake_parts,
                       board=board,
                       rect=rect)

