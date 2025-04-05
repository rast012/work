import pygame, random

# Color presets
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((HEIGHT, WIDTH))

CELL = 20  # Cell size in pixels

def draw_grid():
    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(HEIGHT // 2):
        for j in range(WIDTH // 2):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"{self.x}, {self.y}"

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
    def move(self):
        # Move body segments to follow the head
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        # Update head position
        self.body[0].x += self.dx
        self.body[0].y += self.dy
    def draw(self):
        # Draw head in red and body segments in yellow
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))
    def check_collision(self, food):
        # Check if the snake's head collides with the food
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # Increase snake length
            self.body.append(Point(head.x, head.y))
            return True
        return False

class Food:
    def __init__(self):
        # Get grid dimensions based on cell size
        grid_width = WIDTH // CELL
        grid_height = HEIGHT // CELL
        # Randomly place the food within the grid
        self.pos = Point(random.randint(0, grid_width - 1), random.randint(0, grid_height - 1))
        # Assign a random weight (affects size and potential score value)
        self.weight = random.choice([1, 2, 5])
        # Set the lifetime for the food in milliseconds (e.g., 5 seconds)
        self.lifetime = 5000  
        # Record the creation time to track when food should disappear
        self.created_time = pygame.time.get_ticks()
    def draw(self):
        # Adjust food size based on weight (heavier food appears larger)
        size = CELL + (self.weight - 1) * 5
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, size, size))

FPS = 5
clock = pygame.time.Clock()

food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Change snake direction based on key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    draw_grid_chess()
    snake.move()

    # Check if snake eats the food; if yes, generate new food
    if snake.check_collision(food):
        food = Food()

    # Check if the food's lifetime has expired; if so, create a new food
    if pygame.time.get_ticks() - food.created_time > food.lifetime:
        food = Food()

    snake.draw()
    food.draw()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
