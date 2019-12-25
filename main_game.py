import sys, pygame
import random
import game_objects

BACKGROUND = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
SPEED = 3
STOP = 0, 0
MVT = {pygame.K_LEFT:   [-SPEED, 0],
       pygame.K_RIGHT:  [SPEED, 0],
       pygame.K_DOWN:   [0, SPEED],
       pygame.K_UP:     [0, -SPEED]}


def boundaries(rect, board):
    if rect.left <= board.x_start + board.thickness:
        rect.right = board.x_start + board.width
    elif rect.right >= board.x_start + board.width:
        rect.left = board.x_start + board.thickness
    if rect.top <= board.y_start + board.thickness:
        rect.bottom = board.y_start + board.height
    elif rect.bottom >= board.y_start + board.height:
        rect.top = board.y_start + board.thickness

    return (rect.left, rect.right, rect.top, rect.bottom)


def check_game_over(snake):
    head = (snake[0].rect.x, snake[0].rect.y)
    snake_body = [(piece.rect.x, piece.rect.y) for piece in snake[1:]]
    if head in snake_body:
        print("Game Over")
        return True


def check_eat_food(food, snake):
    head = snake[0].rect
    midx = (head.right + head.left) // 2
    midy = (head.bottom + head.top) // 2
    if midx <= food.right and midx >= food.left and midy <= food.bottom and midy >= food.top:
        return True


def generate_food(board):
    return board.food()


def loop(objects):
    objects.snake.head_mvt = MVT.get(random.choice(list(MVT.keys())))
    food = generate_food(objects.board)
    while True:
        objects.clock.tick(objects.screen.fps)
        objects.display.fill(BACKGROUND)
        pygame.draw.rect(objects.display, WHITE, objects.rect, 2)
        pygame.draw.rect(objects.display, RED, food)

        objects.snake.parts[0].rect = objects.snake.parts[0].rect.move(
            objects.snake.head_mvt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                objects.snake.head_mvt = MVT.get(event.key, STOP)

        head = objects.snake.parts[0].rect
        updated_bounds = boundaries(head, objects.board)
        head.left, head.right, head.top, head.bottom = updated_bounds

        if check_game_over(objects.snake.parts):
            sys.exit()

        if check_eat_food(food, objects.snake.parts):
            food = generate_food(objects.board)
            if objects.snake.head_mvt == MVT.get(pygame.K_LEFT):
                objects.snake.grow(
                    objects.snake.parts[len(objects.snake.parts) - 1].rect.x
                    + objects.snake.width,
                    objects.snake.parts[len(objects.snake.parts) - 1].rect.y)
            elif objects.snake.head_mvt == MVT.get(pygame.K_RIGHT):
                objects.snake.grow(objects.snake.parts[len(objects.snake.parts) - 1].rect.x
                                   - objects.snake.width, 
                                   objects.snake.parts[len(objects.snake.parts) - 1].rect.y)
            elif objects.snake.head_mvt == MVT.get(pygame.K_DOWN):
                objects.snake.grow(objects.snake.parts[len(objects.snake.parts) - 1].rect.x, 
                                   objects.snake.parts[len(objects.snake.parts) - 1].rect.y
                                   - objects.snake.height)
            elif objects.snake.head_mvt == MVT.get(pygame.K_UP):
                objects.snake.grow(objects.snake.parts[len(objects.snake.parts) - 1].rect.x, 
                                   objects.snake.parts[len(objects.snake.parts) - 1].rect.y
                                   + objects.snake.height)

        for piece in objects.snake.parts:
            pygame.draw.rect(objects.display, WHITE, piece.rect)

        updated_parts = []
        for re in objects.snake.parts:
            updated_parts.append((re.rect.x, re.rect.y))

        for i in range(1, len(objects.snake.parts)):
            objects.snake.parts[i].rect.x = updated_parts[i - 1][0]
            objects.snake.parts[i].rect.y = updated_parts[i - 1][1]

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    objects = game_objects.create()
    loop(objects)
