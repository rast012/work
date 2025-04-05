import pygame
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Ball")

# Ball properties
BALL_RADIUS = 25
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
BALL_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
STEP = 20  # Movement step in pixels
MOVE_DELAY = 0.05  # Minimum delay (in seconds) between moves

# Main loop
running = True
keys = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
clock = pygame.time.Clock()
last_move_time = time.time()

while running:
    screen.fill(BACKGROUND_COLOR)  # Clear screen
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)  # Draw ball
    pygame.display.flip()  # Update display
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in keys:
                keys[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in keys:
                keys[event.key] = False
    
    # Move ball continuously while key is pressed, with time delay limit
    current_time = time.time()
    if current_time - last_move_time >= MOVE_DELAY:
        if keys[pygame.K_UP] and ball_y>= 0:
            ball_y -= STEP
        if keys[pygame.K_DOWN] and ball_y<= HEIGHT:
            ball_y += STEP
        if keys[pygame.K_LEFT] and ball_x>= 0:
            ball_x -= STEP
        if keys[pygame.K_RIGHT] and ball_x<= WIDTH:
            ball_x += STEP
        last_move_time = current_time
    
    clock.tick(60)  # Limit FPS to 60

pygame.quit()
