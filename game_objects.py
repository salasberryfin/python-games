import pygame
pygame.init()


class Screen(object):

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

class Board(object):

    def __init__(self, x_start, y_start, thickness, display):
        self.x_start = x_start
        self.y_start = y_start
        self.thickness = thickness
        self.width = display[0] - 2*x_start - thickness + 1
        self.height = display[1] - 2*y_start - thickness + 1

    def rect(self):
        return pygame.Rect(self.x_start,
                           self.y_start,
                           self.width,
                           self.height)

class Player(object):
    
    def __init__ (self, mvt, display, width=5, height=5):
        self.mvt = mvt
        self.x_start = display[0]/2
        self.y_start = display[1]/2
        self.width = width
        self.height = height

    def rect(self):
        return pygame.Rect(self.x_start,
                           self.y_start,
                           self.width,
                           self.height)

class GameObjects(dict):

    def __init__(self, *args, **kwargs):
        super(GameObjects, self).__init__(*args, **kwargs)
        self.__dict__ = self


def create():
    screen = Screen(520, 340, 60)
    display = screen.display()
    clock = screen.clock()
    player = Player((0, 0), screen.size())
    player_rect = player.rect()
    board = Board(5, 5, 2, screen.size())
    rect = board.rect()
    
    return GameObjects(screen=screen,
                       display=display,
                       clock=clock,
                       player=player,
                       player_rect=player_rect,
                       board=board,
                       rect=rect)

