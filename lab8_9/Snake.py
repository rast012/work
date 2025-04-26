import pygame
import random
import json
import os

# --- Constants ---
WIDTH, HEIGHT, CELL = 600, 600, 20
GRID_W, GRID_H = WIDTH // CELL, HEIGHT // CELL
DB_FILE = 'db.txt' # File to store game progress

# --- Data Structures ---
class Point:
    """Represents a point on the grid."""
    def __init__(self, x, y):
        self.x, self.y = x, y

    def to_dict(self):
        """Convert Point object to a dictionary for JSON serialization."""
        return {'x': self.x, 'y': self.y}

    @staticmethod
    def from_dict(d):
        """Create a Point object from a dictionary."""
        return Point(d['x'], d['y'])

# --- File Handling ---
def load_data(filename=DB_FILE):
    """Loads user data from a JSON file."""
    if not os.path.exists(filename):
        return {} # Return empty dict if file doesn't exist
    try:
        with open(filename, 'r') as f:
            # Handle empty file case
            content = f.read()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading data from {filename}: {e}. Starting fresh.")
        return {} # Return empty dict on error

def save_data(data, filename=DB_FILE):
    """Saves user data to a JSON file."""
    try:
        # Prepare data for JSON (convert Point objects)
        data_to_save = {}
        for user, record in data.items():
            state_to_save = None
            if record.get('state'):
                state = record['state']
                state_to_save = {
                    'snake': [p.to_dict() for p in state['snake']],
                    'dx': state['dx'],
                    'dy': state['dy'],
                    'food': state['food'].to_dict(),
                    'food_weight': state['food_weight'],
                    'food_color': state['food_color']
                }
            data_to_save[user] = {
                'level': record['level'],
                'score': record['score'],
                'state': state_to_save # Store the converted state
            }

        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=4) # Use indent for readability
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

# --- Level definitions ---
levels = {
    1: {'walls': [], 'speed': 5},
    2: {'walls': [Point(x, 5) for x in range(5, 15)], 'speed': 8},
    3: {'walls': [Point(5, y) for y in range(5, 15)] +
                 [Point(15, y) for y in range(5, 15)], 'speed': 12},
    # add more levels...
}

# --- Load data and prompt for user ---
user_data = load_data() # Load existing data
current_user = input(f"Enter username (existing: {', '.join(user_data.keys())}): ").strip()

level = 1
score = 0
saved_state_dict = None # Will hold the state dictionary if loaded

if current_user in user_data:
    record = user_data[current_user]
    level = record.get('level', 1)
    score = record.get('score', 0)
    saved_state_dict = record.get('state') # Get the saved state dict (or None)
    print(f"Welcome back {current_user}! Loading level {level}, score {score}.")
    if saved_state_dict:
        print("Restoring saved position.")
    else:
        print("Starting level fresh.")
else:
    print(f"Welcome {current_user}! Starting new game.")
    # Add new user to data structure immediately for saving later
    user_data[current_user] = {'level': level, 'score': score, 'state': None}


# --- Pygame init ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Snake Game - {current_user}")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 36)

# --- Snake & Food Classes ---
class Snake:
    def __init__(self):
        # Default starting position
        self.body = [Point(GRID_W // 2, GRID_H // 2 + 1),
                     Point(GRID_W // 2, GRID_H // 2),
                     Point(GRID_W // 2, GRID_H // 2 - 1)]
        self.dx, self.dy = 0, 1 # Start moving down

    def move(self):
        # Move body segments
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x, self.body[i].y = self.body[i-1].x, self.body[i-1].y
        # Move head
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def grow(self):
         # Add new segment at the position of the last segment before moving
         # This needs careful timing or just append a copy of the tail
         self.body.append(Point(self.body[-1].x, self.body[-1].y))

    def draw(self):
        # Draw head
        pygame.draw.rect(screen, (0, 100, 0), # Darker green head
                         (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        # Draw body
        for segment in self.body[1:]:
            pygame.draw.rect(screen, (0, 200, 0), # Brighter green body
                             (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_food(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.grow()
            return True
        return False

    def check_death(self, walls):
        head = self.body[0]
        # Check wall collision
        if head.x < 0 or head.x >= GRID_W or head.y < 0 or head.y >= GRID_H:
            print("Death: Hit screen boundary!")
            return True
        # Check self collision
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                print("Death: Hit self!")
                return True
        # Check collision with level walls
        for wall in walls:
            if head.x == wall.x and head.y == wall.y:
                print("Death: Hit level wall!")
                return True
        return False

class Food:
    def __init__(self, snake_body, walls):
        self.generate_new_pos(snake_body, walls)
        self.weight = random.choice([1, 2, 5])
        self.color = {(1): (0, 255, 0), (2): (0, 0, 255), (5): (255, 0, 0)}[self.weight]
        self.created_time = pygame.time.get_ticks()
        self.lifetime = 7000 # Food lasts 7 seconds

    def generate_new_pos(self, snake_body, walls):
         """Generates a new position for food, avoiding snake and walls."""
         while True:
            x = random.randint(0, GRID_W - 1)
            y = random.randint(0, GRID_H - 1)
            on_snake = any(segment.x == x and segment.y == y for segment in snake_body)
            on_wall = any(wall.x == x and wall.y == y for wall in walls)
            if not on_snake and not on_wall:
                self.pos = Point(x, y)
                break

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def is_expired(self):
        """Check if the food has been on screen too long."""
        return pygame.time.get_ticks() - self.created_time > self.lifetime

# --- Game State Functions ---
def reset_game_state():
    """Resets snake and food for the current level, keeps level/score."""
    global snake, food, FPS
    print(f"Resetting positions for Level {level}")
    snake = Snake() # Create a new snake at default position
    # Ensure food doesn't spawn on the new snake or walls
    food = Food(snake.body, levels[level]['walls'])
    FPS = levels[level]['speed']

def save_current_state(full_state=True):
    """Updates user_data and saves it to the file.
       If full_state is False, only saves level and score (e.g., on death/quit).
    """
    global user_data
    state_to_save = None
    if full_state:
         state_to_save = {
            'snake': list(snake.body), # Store copies of points
            'dx': snake.dx,
            'dy': snake.dy,
            'food': food.pos, # Store copy of point
            'food_weight': food.weight,
            'food_color': food.color
        }
         print(f"Saving full state for {current_user}: Level {level}, Score {score}")
    else:
        print(f"Saving progress for {current_user}: Level {level}, Score {score}")


    user_data[current_user] = {
        'level': level,
        'score': score,
        'state': state_to_save # Store None if not full_state
    }
    save_data(user_data, DB_FILE) # Persist changes immediately

# --- Initialize Game Elements ---
snake = Snake()
food = Food(snake.body, levels[level]['walls']) # Initial food
FPS = levels[level]['speed']

# Load saved state if available
if saved_state_dict:
    try:
        # Restore snake
        snake.body = [Point.from_dict(p_dict) for p_dict in saved_state_dict['snake']]
        snake.dx = saved_state_dict['dx']
        snake.dy = saved_state_dict['dy']
        # Restore food
        food.pos = Point.from_dict(saved_state_dict['food'])
        food.weight = saved_state_dict['food_weight']
        food.color = saved_state_dict['food_color']
        # Note: Food timer is not saved/restored, it will get a fresh lifetime
        food.created_time = pygame.time.get_ticks()
        FPS = levels[level]['speed'] # Ensure FPS matches loaded level
        print("Successfully restored snake and food positions.")
    except (KeyError, TypeError) as e:
        print(f"Error restoring saved state: {e}. Resetting level.")
        # If state is corrupted or incomplete, reset positions
        reset_game_state()
        # Clear the corrupted state from user_data to prevent loading next time
        user_data[current_user]['state'] = None
        save_data(user_data, DB_FILE) # Save the cleared state
else:
    # If no saved state, ensure game starts fresh for the loaded level/score
    reset_game_state()


paused = False
running = True

# --- Main Game Loop ---
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quit event detected.")
            save_current_state(full_state=False) # Save level/score on quit
            running = False
        if event.type == pygame.KEYDOWN:
            # Pause toggle
            if event.key == pygame.K_p:
                paused = not paused
                print(f"Game {'Paused' if paused else 'Resumed'}")
            # Manual Save (only when paused)
            if paused and event.key == pygame.K_s:
                save_current_state(full_state=True) # Save full state manually
            # Movement (only when not paused)
            if not paused:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx, snake.dy = 1, 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx, snake.dy = -1, 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx, snake.dy = 0, 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx, snake.dy = 0, -1

    if not running: # Exit loop immediately if running is set to False
        break

    # --- Game Logic (if not paused) ---
    if not paused:
        snake.move()

        # Check for death
        if snake.check_death(levels[level]['walls']):
            print("Death detected!")
            save_current_state(full_state=False) # Save level/score, clear state
            reset_game_state() # Reset snake/food for current level
            continue # Skip rest of the loop iteration

        # Check for eating food
        if snake.check_food(food):
            score += food.weight
            print(f"Ate food! Score: {score}")
            # Check for level up (example: every 10 points)
            new_level_candidate = score // 10 + 1 # Simple level up logic
            if new_level_candidate > level and new_level_candidate in levels:
                level = new_level_candidate
                FPS = levels[level]['speed']
                print(f"Level Up! Reached Level {level}")
                # Optionally reset positions on level up, or let player continue
                # reset_game_state() # Uncomment to reset pos on level up
            # Generate new food, avoiding snake and walls
            food = Food(snake.body, levels[level]['walls'])

        # Check if food expired
        if food.is_expired():
            print("Food expired.")
            food = Food(snake.body, levels[level]['walls']) # Generate new food

    # --- Drawing ---
    screen.fill((200, 200, 200)) # Light grey background

    # Draw walls for the current level
    current_walls = levels[level]['walls']
    for wall in current_walls:
        pygame.draw.rect(screen, (100, 100, 100), # Dark grey walls
                         (wall.x * CELL, wall.y * CELL, CELL, CELL))

    # Draw snake and food
    snake.draw()
    food.draw()

    # Draw Score and Level
    score_text = font_small.render(
        f"User: {current_user} | Score: {score} | Level: {level}",
        True, (0, 0, 0))
    screen.blit(score_text, (5, 5))

    # Draw Pause message if paused
    if paused:
        pause_text = font_large.render("PAUSED", True, (255, 0, 0))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(pause_text, pause_rect)
        save_text = font_small.render("Press 'S' to Save State | 'P' to Resume", True, (0,0,0))
        save_rect = save_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(save_text, save_rect)


    # --- Update Display ---
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(FPS)

# --- Cleanup ---
print("Exiting game.")
pygame.quit()
