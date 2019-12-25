import sys, pygame
import random
import game_objects

BACKGROUND = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
STOP = 0, 0


def boundaries(head, board):
    rect = head.rect
    if rect.left <= board.x_start + board.thickness:
        rect.right = board.x_start + board.width
    elif rect.right >= board.x_start + board.width:
        rect.left = board.x_start + head.width
        # rect.left = board.x_start + board.thickness
    if rect.top <= board.y_start + board.thickness:
        rect.bottom = board.y_start + board.height
    elif rect.bottom >= board.y_start + board.height:
        rect.top = board.y_start + head.height
        # rect.top = board.y_start + board.thickness

    return (rect.left, rect.right, rect.top, rect.bottom)


def check_game_over(snake):
    """Checks if snake hit itself."""
    head = (snake.parts[0].rect.x, snake.parts[0].rect.y)
    snake_body = [(piece.rect.x, piece.rect.y) for piece in snake.parts[1:]]
    if head in snake_body:
        print(f"Game Over!\nYour final score is {snake.score}")
        return True


def update_speed(snake):
    """Periodically updates snake speed."""
    if snake.score % 20 == 0:
        snake.accelerate()
        print(f"Increasing speed to {snake.speed}")


def check_eat_food(food, snake):
    """Checks if snake hit food."""
    head = snake[0].rect
    midx = (head.right + head.left) // 2
    midy = (head.bottom + head.top) // 2
    if ( midx <= food.right + food.width / 2 and
         midx >= food.left - food.width / 2 and
         midy <= food.bottom + food.height / 2 and
         midy >= food.top - food.height / 2 ):
        return True


def generate_food(board):
    """Generates new food objects to be drawn in the screen."""
    rand = random.randint(0, 10)
    if rand == random.randint(0, 10):
        return {"shape": board.food(),
                "color": GREEN,
                "score": 10}

    return {"shape": board.food(),
            "color": RED,
            "score": 5}


def loop(objects):
    """Main game loop.

    objects -- list of game objects:
        Player, Screen, Clock, etc.
    """
    snake = objects.snake
    snake.head_mvt = snake.mvt_mat.get(
        random.choice(list(snake.mvt_mat.keys())))
    food = generate_food(objects.board)
    while True:
        objects.clock.tick(objects.screen.fps)
        objects.display.fill(BACKGROUND)
        pygame.draw.rect(objects.display, WHITE, objects.rect, 2)
        pygame.draw.rect(objects.display, food["color"], food["shape"])

        snake.parts[0].rect = snake.parts[0].rect.move(
            snake.head_mvt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                snake.head_mvt = snake.mvt_mat.get(event.key, STOP)

        # head = snake.parts[0].rect
        head = snake.parts[0]
        updated_bounds = boundaries(head, objects.board)
        head.left, head.right, head.top, head.bottom = updated_bounds

        if check_game_over(snake):
            sys.exit()

        if check_eat_food(food["shape"], snake.parts):
            snake.score += food["score"]
            update_speed(snake)
            print(f"Current score: {snake.score}") 
            food = generate_food(objects.board)
            if snake.head_mvt == snake.mvt_mat.get(pygame.K_LEFT):
                snake.grow(snake.parts[len(snake.parts) - 1].rect.x + snake.width, 
                           snake.parts[len(snake.parts) - 1].rect.y)
            elif snake.head_mvt == snake.mvt_mat.get(pygame.K_RIGHT):
                snake.grow(snake.parts[len(snake.parts) - 1].rect.x - snake.width, 
                           snake.parts[len(snake.parts) - 1].rect.y)
            elif snake.head_mvt == snake.mvt_mat.get(pygame.K_DOWN):
                snake.grow(snake.parts[len(snake.parts) - 1].rect.x,
                           snake.parts[len(snake.parts) - 1].rect.y - snake.height)
            elif snake.head_mvt == snake.mvt_mat.get(pygame.K_UP):
                snake.grow(snake.parts[len(snake.parts) - 1].rect.x, 
                           snake.parts[len(snake.parts) - 1].rect.y + snake.height)

        for piece in snake.parts:
            pygame.draw.rect(objects.display, WHITE, piece.rect)

        updated_parts = []
        for snake_part in snake.parts:
            updated_parts.append((snake_part.rect.x, snake_part.rect.y))

        for i in range(1, len(snake.parts)):
            snake.parts[i].rect.x = updated_parts[i - 1][0]
            snake.parts[i].rect.y = updated_parts[i - 1][1]

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    objects = game_objects.create()
    loop(objects)
