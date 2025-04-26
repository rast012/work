import pygame, random
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 20  # Pixel size for grid cells
GRID_WIDTH = WIDTH // CELL # In pixels
GRID_HEIGHT = HEIGHT // CELL # In pixels

# Initial game variables
score = 0
level = 1
FPS = 5  # Initial speed ie, the longer the snake, faster the game

def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            pygame.draw.rect(screen, colors[(i+j)%2], (i*CELL, j*CELL, CELL, CELL))

# Point class for positions
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake stuff
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
    def move(self):
        # Move segments to follow head
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        # Update head position
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x*CELL, head.y*CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x*CELL, segment.y*CELL, CELL, CELL))

    def check_collision_with_food(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            # Grow snake
            self.body.append(Point(head.x, head.y))
            return True
        return False

    def check_death(self):
        head = self.body[0]
        # Out of bounds (walls are borders)
        if head.x < 1 or head.x >= GRID_WIDTH-1 or head.y < 1 or head.y >= GRID_HEIGHT-1:
            return True
        # Colliding with itself
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

# Food sutff
class Food:
    def __init__(self, snake_body):
        # Avoid walls: only choose from 1 to GRID_WIDTH-2 and similar for height
        valid = False
        while not valid:
            x = random.randint(1, GRID_WIDTH)
            y = random.randint(1, GRID_HEIGHT)
            valid = True
            # Ensure food is not on the snake
            for segment in snake_body:
                if segment.x == x and segment.y == y:
                    valid = False
                    break
        self.pos = Point(x, y)
        self.weight = random.choice([1, 2, 5])
        # Set color based on weight
        if self.weight == 1:
            self.color = colorGREEN
        elif self.weight == 2:
            self.color = colorBLUE
        else:
            self.color = colorRED
        self.lifetime = 5000  # ms food lasts
        self.created_time = pygame.time.get_ticks()

    def draw(self):
        # Size constant, only color changes
        pygame.draw.rect(screen, self.color, (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL))

clock = pygame.time.Clock()

def reset_game():
    global snake, food, score, level, FPS
    snake = Snake()
    food = Food(snake.body)
    score = 0
    level = 1
    FPS = 5

reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Prevent snake from reversing
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    draw_grid_chess()
    snake.move()

    # Check death conditions: border and self-collision
    if snake.check_death():
        reset_game()
        continue

    # Check food collision
    if snake.check_collision_with_food(food):
        score += food.weight  # Increase score by food weight
        # Level up: for every 3 points increase level and speed
        if score // 3 + 1 > level:
            level += 1
            FPS += 2
        food = Food(snake.body)

    # Replace food if lifetime expired
    if pygame.time.get_ticks() - food.created_time > food.lifetime:
        food = Food(snake.body)

    snake.draw()
    food.draw()

    # Display score and level
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"Score: {score}  Level: {level}", True, colorBLACK)
    screen.blit(text, (5, 5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
