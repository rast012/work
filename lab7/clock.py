import pygame
import time

# Initialize pygame
pygame.init()

# Load images
background = pygame.image.load("clock.png") 
minute_hand = pygame.image.load("min_hand.png")  
second_hand = pygame.image.load("sec_hand.png") 

# Set screen dimensions
WIDTH, HEIGHT = background.get_size()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock")

# Get the center of the clock
CENTER = (WIDTH // 2, HEIGHT // 2)

# Offset values for fine-tuning rotation alignment
MINUTE_OFFSET = 47  # Adjust this value to fix rotation offset
SECOND_OFFSET = -60  # Adjust this value to fix rotation offset

# rotate hand and position it correctly
def rotate_hand(image, angle, offset):
    rotated_image = pygame.transform.rotate(image, -(angle + offset))  # Ensure clockwise rotation
    rotated_rect = rotated_image.get_rect(center=CENTER)
    return rotated_image, rotated_rect

# Create a clock to control FPS
clock = pygame.time.Clock()

# Main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get precise system time
    current_time = time.localtime()
    minutes = current_time.tm_min
    seconds = current_time.tm_sec
    
    # Calculate angles (clockwise rotation)
    minute_angle = minutes * 6  # 360 degrees / 60 minutes = 6 degrees per minute
    second_angle = seconds * 6  # 360 degrees / 60 seconds = 6 degrees per second
    
    # Rotate hands with offsets
    rotated_minute_hand, minute_rect = rotate_hand(minute_hand, minute_angle, MINUTE_OFFSET)
    rotated_second_hand, second_rect = rotate_hand(second_hand, second_angle, SECOND_OFFSET)
    
    # Draw everything
    screen.blit(background, (0, 0))
    screen.blit(rotated_minute_hand, minute_rect.topleft)
    screen.blit(rotated_second_hand, second_rect.topleft)
    
    pygame.display.flip()
    clock.tick(60)  # Ensures smoother updates (60 FPS)

pygame.quit()