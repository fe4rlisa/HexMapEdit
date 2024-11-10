import sys
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600

SCREEN_WIDTH, SCREEN_HEIGHT = 800,600#screen.get_size()
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


radius = 34
hex_width = np.sqrt(3) * radius
hex_height = 3 / 2 * radius
grid_width = 10
grid_height = 10
grid = []


def create_grid(grid_width, grid_height):
    for y in range(grid_height):
        for x in range(grid_width):
            grid.append({(x,y): 1})
    print(grid)
    return grid

def draw_grid(grid):
    grid_pixel_width = (grid_width) *  (hex_width) - (hex_width / 2)
    grid_pixel_height = (grid_height) * (hex_height) - (hex_width)

    start_x = SCREEN_CENTER[0] - grid_pixel_width / 2
    start_y = SCREEN_CENTER[1] - grid_pixel_height / 2

    for y in range(grid_height):
        for x in range(grid_width):
            grid_x_location = start_x + (hex_width) * x
            grid_y_location = start_y + (hex_height) * y
            if (y%2 == 0):
                grid_x_location += hex_width / 2

            angles = np.linspace(np.pi / 6, 11 * np.pi / 6, 6)
            hexagon_vertices = [(grid_x_location + radius * np.cos(angle), grid_y_location + radius * np.sin(angle)) for angle in angles]
            
            # <For debug> changes color of odd x heagons to red
            if (x%2 == 0):
                pygame.draw.polygon(screen, BLACK, hexagon_vertices, width=4)
            else:
                hexagon_inner = pygame.draw.polygon(screen, (200,200,200), hexagon_vertices)
                hexagon_outer = pygame.draw.polygon(screen, BLACK, hexagon_vertices, width=4)

# Need to translate center cords to real cords???
def cord_to_real(grid):
    start_x = SCREEN_CENTER[0] - grid_pixel_width / 2
    start_y = SCREEN_CENTER[1] - grid_pixel_height / 2
    grid_x_location = start_x + (hex_width) * x
    grid_y_location = start_y + (hex_height) * y
    

pygame.init()
screen = pygame.display.set_mode((BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT))
pygame.display.set_caption("HexMapEdit")
clock = pygame.time.Clock()
running = True



create_grid(grid_width, grid_height)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE

    draw_grid(grid)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  
pygame.quit()