# Приводим код к стандарту PEP8
import pygame
import random

# Константы
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Цвета
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = RED

    def randomize_position(self):
        return (
            random.randint(0, GRID_WIDTH - 1) * CELL_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE,
        )

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.body_color,
            (*self.position, CELL_SIZE, CELL_SIZE)
        )


class Snake(GameObject):
    def __init__(self):
        super().__init__((WIDTH // 2, HEIGHT // 2))
        self.body_color = GREEN
        self.positions = [self.position]
        self.length = 4
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None

    def update_direction(self):
        if self.next_direction:
            opposite_direction = (
                -self.direction[0], -self.direction[1]
            )
            if self.next_direction != opposite_direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        new_head = (
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        )

        if (
            new_head in self.positions
            or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT)
        ):
            return False

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(
                surface, self.body_color,
                (*pos, CELL_SIZE, CELL_SIZE)
            )

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.length = 4
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None
        return 10


def handle_keys(snake):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.next_direction = (0, -CELL_SIZE)
    elif keys[pygame.K_DOWN]:
        snake.next_direction = (0, CELL_SIZE)
    elif keys[pygame.K_LEFT]:
        snake.next_direction = (-CELL_SIZE, 0)
    elif keys[pygame.K_RIGHT]:
        snake.next_direction = (CELL_SIZE, 0)


def main():
    """Главная функция запуска игры."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    initial_speed = 10
    speed = initial_speed

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.update_direction()
        if not snake.move():
            speed = snake.reset()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            speed += 1

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()


if __name__ == "__main__":
    main()

