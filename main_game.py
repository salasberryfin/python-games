import sys, pygame
import game_objects
import background

BACKGROUND = 0, 0, 0
WHITE = 255, 255, 255
SPEED = 1
STOP = 0, 0
MVT = {pygame.K_LEFT:   [-SPEED, 0],
       pygame.K_RIGHT:  [SPEED, 0],
       pygame.K_DOWN:   [0, SPEED],
       pygame.K_UP:     [0, -SPEED]}


def boundaries(rect, board):
    if rect.left <= board.x_start + board.thickness:
        rect.left = board.x_start + board.thickness
    elif rect.right >= board.x_start + board.width:
        rect.right = board.x_start + board.width
    if rect.top <= board.y_start + board.thickness:
        rect.top = board.y_start + board.thickness
    elif rect.bottom >= board.y_start + board.height:
        rect.bottom = board.y_start + board.height

    return (rect.left, rect.right, rect.top, rect.bottom)


def loop(objects):
    while 1:
        objects.clock.tick(objects.screen.fps)
        # background.draw()
        objects.display.fill(BACKGROUND)
        pygame.draw.rect(objects.display, WHITE, objects.rect, 2)

        objects.player_rect = objects.player_rect.move(objects.player.mvt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                objects.player.mvt = MVT.get(event.key, STOP)
            elif event.type == pygame.KEYUP:
                objects.player.mvt = STOP

        updated_bounds = boundaries(objects.player_rect, objects.board)
        objects.player_rect.left, objects.player_rect.right, objects.player_rect.top, objects.player_rect.bottom = updated_bounds
        pygame.draw.rect(objects.display, WHITE, objects.player_rect)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    objects = game_objects.create()
    loop(objects)
