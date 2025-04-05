import pygame  # Import Pygame library
import math    # Import math module for triangle calculations

pygame.init()  # Initialize Pygame

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create a window for the drawing app
Background = (255, 255, 255)  # Set background color

# Create a base layer to store drawings (persistent canvas)
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(Background)  # Fill with white

# Define colors
colorRED = (255, 0, 0)    # Red color
colorBLUE = (0, 0, 255)   # Blue color
colorBLACK = (0, 0, 0)    # Black color
colorWHITE = Background   # White color (for eraser)

current_color = colorRED  # Set the default drawing color to red
THICKNESS = 5             # Default thickness for drawing

# Default drawing mode is rectangle
draw_mode = "rect"

clock = pygame.time.Clock()  # Create a clock object to control the frame rate
LMBpressed = False  # Flag to track if left mouse button is pressed

# Coordinates for drawing (starting and current positions)
prevX = prevY = currX = currY = 0

def calculate_rect(x1, y1, x2, y2):
    # Calculate rectangle position and size given two corner points
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True  # Main loop control variable
while running:
    # Refresh the screen with the persistent base layer
    screen.blit(base_layer, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit event
            running = False
        
        # Mouse button down: begin drawing
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos  # Save starting position
            
        # Mouse motion with button pressed: show preview of shape
        if event.type == pygame.MOUSEMOTION and LMBpressed:
            currX, currY = event.pos  # Update current position
            # Redraw persistent drawings to avoid trail of temporary shapes
            screen.blit(base_layer, (0, 0))
            
            # Draw preview based on the current drawing mode
            if draw_mode == "rect":
                pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif draw_mode == "circle":
                radius = max(abs(currX - prevX), abs(currY - prevY)) // 2
                pygame.draw.circle(screen, current_color, ((prevX + currX) // 2, (prevY + currY) // 2), radius, THICKNESS)
            elif draw_mode == "eraser":
                pygame.draw.circle(base_layer, colorWHITE, (currX, currY), THICKNESS)
                screen.blit(base_layer, (0, 0))
            elif draw_mode == "brush":
                pygame.draw.circle(base_layer, current_color, (currX, currY), THICKNESS // 2)
                screen.blit(base_layer, (0, 0))
            # Draw square preview: square with side equal to max(|dx|, |dy|)
            elif draw_mode == "square":
                side = max(abs(currX - prevX), abs(currY - prevY))
                sign_x = 1 if currX - prevX >= 0 else -1
                sign_y = 1 if currY - prevY >= 0 else -1
                end_x = prevX + sign_x * side
                end_y = prevY + sign_y * side
                square_rect = pygame.Rect(min(prevX, end_x), min(prevY, end_y), side, side)
                pygame.draw.rect(screen, current_color, square_rect, THICKNESS)
            # Draw right triangle preview: right angle at starting point
            elif draw_mode == "right_triangle":
                points = [(prevX, prevY), (currX, prevY), (prevX, currY)]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)
            # Draw equilateral triangle preview: using prev and curr as base
            elif draw_mode == "equilateral_triangle":
                # Calculate third vertex using formula for equilateral triangle
                vx = (prevX + currX) / 2 - (math.sqrt(3) / 2) * (prevY - currY)
                vy = (prevY + currY) / 2 - (math.sqrt(3) / 2) * (currX - prevX)
                points = [(prevX, prevY), (currX, currY), (vx, vy)]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)
            # Draw rhombus preview: using prev and curr as diagonal endpoints
            elif draw_mode == "rhombus":
                mx = (prevX + currX) / 2
                my = (prevY + currY) / 2
                dx = (currX - prevX) / 2
                dy = (currY - prevY) / 2
                p1 = (mx - dy, my + dx)
                p2 = (mx + dy, my - dx)
                points = [(prevX, prevY), p1, (currX, currY), p2]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)

        # Mouse button released: finalize drawing on base_layer
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos  # Final position
            
            if draw_mode == "rect":
                pygame.draw.rect(base_layer, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif draw_mode == "circle":
                radius = max(abs(currX - prevX), abs(currY - prevY)) // 2
                pygame.draw.circle(base_layer, current_color, ((prevX + currX) // 2, (prevY + currY) // 2), radius, THICKNESS)
            elif draw_mode == "square":
                side = max(abs(currX - prevX), abs(currY - prevY))
                sign_x = 1 if currX - prevX >= 0 else -1
                sign_y = 1 if currY - prevY >= 0 else -1
                end_x = prevX + sign_x * side
                end_y = prevY + sign_y * side
                square_rect = pygame.Rect(min(prevX, end_x), min(prevY, end_y), side, side)
                pygame.draw.rect(base_layer, current_color, square_rect, THICKNESS)
            elif draw_mode == "right_triangle":
                points = [(prevX, prevY), (currX, prevY), (prevX, currY)]
                pygame.draw.polygon(base_layer, current_color, points, THICKNESS)
            elif draw_mode == "equilateral_triangle":
                vx = (prevX + currX) / 2 - (math.sqrt(3) / 2) * (prevY - currY)
                vy = (prevY + currY) / 2 - (math.sqrt(3) / 2) * (currX - prevX)
                points = [(prevX, prevY), (currX, currY), (vx, vy)]
                pygame.draw.polygon(base_layer, current_color, points, THICKNESS)
            elif draw_mode == "rhombus":
                mx = (prevX + currX) / 2
                my = (prevY + currY) / 2
                dx = (currX - prevX) / 2
                dy = (currY - prevY) / 2
                p1 = (mx - dy, my + dx)
                p2 = (mx + dy, my - dx)
                points = [(prevX, prevY), p1, (currX, currY), p2]
                pygame.draw.polygon(base_layer, current_color, points, THICKNESS)
            elif draw_mode == "eraser":
                pygame.draw.circle(base_layer, colorWHITE, (currX, currY), THICKNESS)
            elif draw_mode == "brush":
                pygame.draw.circle(base_layer, current_color, (currX, currY), THICKNESS // 2)

        # Key press events to change drawing parameters and modes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:  # Increase thickness
                THICKNESS += 1
            if event.key == pygame.K_MINUS and THICKNESS > 1:  # Decrease thickness (minimum 1)
                THICKNESS -= 1
            if event.key == pygame.K_r:  # 'R' for rectangle mode
                draw_mode = "rect"
            if event.key == pygame.K_c:  # 'C' for circle mode
                draw_mode = "circle"
            if event.key == pygame.K_e:  # 'E' for eraser mode
                draw_mode = "eraser"
            if event.key == pygame.K_b:  # 'B' for brush mode
                draw_mode = "brush"
            if event.key == pygame.K_s:  # 'S' for square mode
                draw_mode = "square"
            if event.key == pygame.K_t:  # 'T' for right triangle mode
                draw_mode = "right_triangle"
            if event.key == pygame.K_y:  # 'Y' for equilateral triangle mode
                draw_mode = "equilateral_triangle"
            if event.key == pygame.K_h:  # 'H' for rhombus mode
                draw_mode = "rhombus"
            if event.key == pygame.K_1:  # '1' to set color to red
                current_color = colorRED
            if event.key == pygame.K_2:  # '2' to set color to blue
                current_color = colorBLUE
            if event.key == pygame.K_3:  # '3' to set color to black
                current_color = colorBLACK
    
    pygame.display.flip()  # Update display
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
