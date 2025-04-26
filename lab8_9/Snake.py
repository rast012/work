import pygame, random

# ─── “Database” ──────────────────────────────────────────────────────────────
users = set()
user_data = {}  # maps username → {'level': int, 'score': int, 'state': {...}}

# ─── Level definitions ────────────────────────────────────────────────────────
class Point:
    def __init__(self, x, y): self.x, self.y = x, y

levels = {
    1: {'walls': [], 'speed': 5},
    2: {'walls': [Point(x, 5) for x in range(5, 15)],     'speed': 8},
    3: {'walls': [Point(5, y) for y in range(5, 15)] +
             [Point(15, y) for y in range(5, 15)],         'speed': 12},
    # add more...
}

# ─── Prompt for user and load or init ────────────────────────────────────────
current_user = input("Enter username: ").strip()
if current_user in users:
    record = user_data[current_user]
    level, score = record['level'], record['score']
    saved = record.get('state')
else:
    users.add(current_user)
    level, score = 1, 0
    saved = None

# ─── Pygame init ──────────────────────────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT, CELL = 600, 600, 20
GRID_W, GRID_H = WIDTH//CELL, HEIGHT//CELL
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ─── Snake & Food ─────────────────────────────────────────────────────────────
class Snake:
    def __init__(self):
        self.body = [Point(10,11), Point(10,12), Point(10,13)]
        self.dx, self.dy = 1, 0
    def move(self):
        for i in range(len(self.body)-1,0,-1):
            self.body[i].x, self.body[i].y = \
                self.body[i-1].x, self.body[i-1].y
        self.body[0].x += self.dx; self.body[0].y += self.dy
    def draw(self):
        pygame.draw.rect(screen, (255,0,0),
                         (self.body[0].x*CELL, self.body[0].y*CELL, CELL, CELL))
        for s in self.body[1:]:
            pygame.draw.rect(screen, (255,255,0),
                             (s.x*CELL, s.y*CELL, CELL, CELL))
    def check_food(self, food):
        h = self.body[0]
        if h.x==food.pos.x and h.y==food.pos.y:
            self.body.append(Point(h.x,h.y)); return True
        return False
    def check_death(self, walls):
        h=self.body[0]
        if h.x<1 or h.x>=GRID_W-1 or h.y<1 or h.y>=GRID_H-1: return True
        for s in self.body[1:]:
            if h.x==s.x and h.y==s.y: return True
        for w in walls:
            if h.x==w.x and h.y==w.y: return True
        return False

class Food:
    def __init__(self, snake_body):
        while True:
            x,y = random.randint(1,GRID_W-2), random.randint(1,GRID_H-2)
            if not any(s.x==x and s.y==y for s in snake_body): break
        self.pos = Point(x,y)
        self.weight = random.choice([1,2,5])
        self.color = {(1):(0,255,0),(2):(0,0,255),(5):(255,0,0)}[self.weight]
        self.created = pygame.time.get_ticks()
        self.lifetime = 5000
    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x*CELL, self.pos.y*CELL, CELL, CELL))

# ─── Game (re)set ─────────────────────────────────────────────────────────────
def reset_game():
    global snake, food, FPS, score
    snake = Snake()
    food = Food(snake.body)
    score = 0
    FPS = levels[level]['speed']

# load saved state or fresh
if saved:
    snake = Snake()
    snake.body = [Point(p.x,p.y) for p in saved['snake']]
    snake.dx, snake.dy = saved['dx'], saved['dy']
    food = Food(snake.body)
    food.pos = Point(saved['food'].x, saved['food'].y)
    food.weight, food.color = saved['food_weight'], saved['food_color']
    FPS = levels[level]['speed']
else:
    reset_game()

paused = False

# ─── Save shortcut ────────────────────────────────────────────────────────────
def save_state():
    user_data[current_user] = {
        'level': level, 'score': score,
        'state': {
            'snake': list(snake.body),
            'dx': snake.dx, 'dy': snake.dy,
            'food': food.pos,
            'food_weight': food.weight,
            'food_color': food.color
        }
    }
    print(f"Saved: {current_user} → level {level}, score {score}")

# ─── Main loop ────────────────────────────────────────────────────────────────
running = True
while running:
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_p:
                paused = not paused
            if paused and e.key==pygame.K_s:
                save_state()
            if not paused:
                if e.key==pygame.K_RIGHT and snake.dx!=-1: snake.dx, snake.dy = 1,0
                if e.key==pygame.K_LEFT  and snake.dx!=1:  snake.dx, snake.dy = -1,0
                if e.key==pygame.K_DOWN  and snake.dy!=-1: snake.dx, snake.dy = 0,1
                if e.key==pygame.K_UP    and snake.dy!=1:  snake.dx, snake.dy = 0,-1

    draw_grid_chess = lambda: None  # reuse your grid-draw
    screen.fill((200,200,200))
    draw_grid_chess()
    # draw walls
    for w in levels[level]['walls']:
        pygame.draw.rect(screen, (100,100,100),
                         (w.x*CELL, w.y*CELL, CELL, CELL))

    if paused:
        f=pygame.font.SysFont(None,36)
        screen.blit(f.render("PAUSED — S to save, P to resume",True,(0,0,0)),(100,280))
        pygame.display.flip()
        clock.tick(5)
        continue

    snake.move()
    if snake.check_death(levels[level]['walls']):
        reset_game(); continue

    if snake.check_food(food):
        score += food.weight
        if score//3+1 > level and level+1 in levels:
            level += 1
            FPS = levels[level]['speed']
        food = Food(snake.body)

    if pygame.time.get_ticks()-food.created > food.lifetime:
        food = Food(snake.body)

    snake.draw()
    food.draw()

    txt = pygame.font.SysFont(None,24).render(
        f"{current_user} Score:{score} Level:{level}", True, (0,0,0))
    screen.blit(txt, (5,5))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
