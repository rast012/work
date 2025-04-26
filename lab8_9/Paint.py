import pygame 
import math    # for triangle and many other things

pygame.init()  # start pygame
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # make screen
Background = (255, 255, 255)  # white bg
# layer for drawing, stays persistent
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill(Background)  # make it white
# Colors
colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)   
colorBLACK = (0, 0, 0)    
colorWHITE = Background   # eraser color
# Defaults
current_color = colorRED 
THICKNESS = 5          # line/border size
draw_mode = "brush"     # start with brush
clock = pygame.time.Clock() # for FPS
LMBpressed = False  # check if left mouse button is clicked or nah
# Mouse coords
prevX = prevY = currX = currY = 0

def calculate_rect(x1, y1, x2, y2):
    # makes a rect from two points
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True  # loop control
while running:
    # redraw base layer each frame
    screen.blit(base_layer, (0, 0))
    
    for event in pygame.event.get(): # handle events
        if event.type == pygame.QUIT:  # X button
            running = False
        
        # Mouse click down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 is left button
            LMBpressed = True
            prevX, prevY = event.pos  # store start pos
            
        # Mouse drag
        if event.type == pygame.MOUSEMOTION and LMBpressed:
            currX, currY = event.pos  # update current pos
            # redraw screen with base to clear old preview
            screen.blit(base_layer, (0, 0))
            
            # Show shape preview while dragging
            if draw_mode == "rect":
                pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif draw_mode == "circle":
                radius = max(abs(currX - prevX), abs(currY - prevY)) // 2
                pygame.draw.circle(screen, current_color, ((prevX + currX) // 2, (prevY + currY) // 2), radius, THICKNESS)
            elif draw_mode == "eraser": # eraser just draws white on base layer
                pygame.draw.circle(base_layer, colorWHITE, (currX, currY), THICKNESS)
                screen.blit(base_layer, (0, 0)) # show erased part immediately
            elif draw_mode == "brush": # brush draws small circles on base layer
                pygame.draw.circle(base_layer, current_color, (currX, currY), THICKNESS // 2)
                screen.blit(base_layer, (0, 0)) # show drawn part immediately
            elif draw_mode == "square": # square preview
                side = max(abs(currX - prevX), abs(currY - prevY))
                sign_x = 1 if currX - prevX >= 0 else -1
                sign_y = 1 if currY - prevY >= 0 else -1
                end_x = prevX + sign_x * side
                end_y = prevY + sign_y * side
                square_rect = pygame.Rect(min(prevX, end_x), min(prevY, end_y), side, side)
                pygame.draw.rect(screen, current_color, square_rect, THICKNESS)
            elif draw_mode == "right_triangle": # right triangle preview
                points = [(prevX, prevY), (currX, prevY), (prevX, currY)]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)
            elif draw_mode == "equilateral_triangle": # equilateral triangle preview
                # fancy math for 3rd point
                vx = (prevX + currX) / 2 - (math.sqrt(3) / 2) * (prevY - currY)
                vy = (prevY + currY) / 2 - (math.sqrt(3) / 2) * (currX - prevX)
                points = [(prevX, prevY), (currX, currY), (vx, vy)]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)
            elif draw_mode == "rhombus": # rhombus preview
                # math for other 2 points
                mx = (prevX + currX) / 2
                my = (prevY + currY) / 2
                dx = (currX - prevX) / 2
                dy = (currY - prevY) / 2
                p1 = (mx - dy, my + dx)
                p2 = (mx + dy, my - dx)
                points = [(prevX, prevY), p1, (currX, currY), p2]
                pygame.draw.polygon(screen, current_color, points, THICKNESS)

        # Mouse click up
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # 1 is left button
            LMBpressed = False
            currX, currY = event.pos  # store end pos
            
            # Draw final shape on base_layer (except brush/eraser which drew already)
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
            # No need for brush/eraser here, they draw continuously

        # Keyboard stuff
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:  # + thickness
                THICKNESS += 1
            if event.key == pygame.K_MINUS and THICKNESS > 1:  # - thickness (min value is 1)
                THICKNESS -= 1
            # Switch modes
            if event.key == pygame.K_r: draw_mode = "rect"
            if event.key == pygame.K_c: draw_mode = "circle"
            if event.key == pygame.K_e: draw_mode = "eraser"
            if event.key == pygame.K_b: draw_mode = "brush"
            if event.key == pygame.K_s: draw_mode = "square"
            if event.key == pygame.K_t: draw_mode = "right_triangle"
            if event.key == pygame.K_y: draw_mode = "equilateral_triangle"
            if event.key == pygame.K_h: draw_mode = "rhombus"
            # Switch colors
            if event.key == pygame.K_1: current_color = colorRED
            if event.key == pygame.K_2: current_color = colorBLUE
            if event.key == pygame.K_3: current_color = colorBLACK
    pygame.display.flip()  # show everything on screen
    clock.tick(60)  # limit to 60 FPS
pygame.quit() # close pygame