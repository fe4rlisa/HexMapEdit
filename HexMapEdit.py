import sys
import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
GRAY = (200,200,200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600

screen_width, screen_height = 800,600
screen_center = (screen_width/2, screen_height/2)


radius = 34
hex_width = np.sqrt(3) * radius
hex_height = 3 / 2 * radius
grid_width = 4
grid_height = 4
grid = []


#-- color_mapping --#
#    0: WHITE       #
#    1: GRAY        #
#    2: RED         #
#    3: GREEN       #
#-------------------#

#-- Adds xy cords and type of tile to grid[] (list) --#
def create_grid(grid_width, grid_height):
    for y in range(grid_height):
        for x in range(grid_width):
            grid.append({(x,y): 0})
    print(grid)
    return grid
#-----------------------------------------------------#



def draw_grid(grid):
    grid_pixel_width = (grid_width) *  (hex_width) - (hex_width / 2)        #/ Calculates the size of \#
    grid_pixel_height = (grid_height) * (hex_height) - (hex_width)          #\      the hex grid      /#


    start_x = screen_center[0] - grid_pixel_width / 2                       #/ Centers the hex grid \#
    start_y = screen_center[1] - grid_pixel_height / 2                      #\     to the center    /#

    for y in range(grid_height):
        for x in range(grid_width):
            grid_x_location = start_x + (hex_width) * x
            grid_y_location = start_y + (hex_height) * y
            if (y%2 == 0):
                grid_x_location += hex_width / 2


            #-- Get points for hexagons --#
            angles = np.linspace(np.pi / 6, 11 * np.pi / 6, 6)
            hexagon_vertices = [(grid_x_location + radius * np.cos(angle), grid_y_location + radius * np.sin(angle)) for angle in angles]
            #-----------------------------#


            #-- Draw hexagons and then hexagon outlines --#
            grid_index = y * grid_width + x
            hex_dict = grid[grid_index]
            for key in hex_dict:
                if hex_dict[key] == 0:
                    hexagon = pygame.draw.polygon(screen, WHITE, hexagon_vertices)
                elif hex_dict[key] == 1:
                    hexagon = pygame.draw.polygon(screen, GRAY, hexagon_vertices)
                elif hex_dict[key] == 2:
                    hexagon = pygame.draw.polygon(screen, RED, hexagon_vertices)
                elif hex_dict[key] == 3:
                    hexagon = pygame.draw.polygon(screen, GREEN, hexagon_vertices)
        
            hexagon_outline = pygame.draw.polygon(screen, BLACK, hexagon_vertices, width=4)
            #---------------------------------------------#


# Get real cords to check if user has clicked on a hexagon
def check_for_hex_fill(grid, mouse_pos):
    grid_pixel_width = grid_width * hex_width - (hex_width / 2)
    grid_pixel_height = grid_height * hex_height - hex_height
    start_x = screen_center[0] - grid_pixel_width / 2
    start_y = screen_center[1] - grid_pixel_height / 2
    

    for y in range(grid_height):
        for x in range(grid_width):
            grid_x_location = start_x + (hex_width) * x
            grid_y_location = start_y + (hex_height) * y
            if y % 2 == 0:
                grid_x_location += hex_width / 2
            
            distance_x = mouse_pos[0] - grid_x_location
            distance_y = mouse_pos[1] - grid_y_location
            distance = np.sqrt(distance_x ** 2 + distance_y ** 2)

            if distance <= radius:
                grid_index = y * grid_width + x
                hex_dict = grid[grid_index]
                for key in hex_dict:
                    hex_dict[key] = (hex_dict[key] + 1) if hex_dict[key] < 3 else 0
                break


pygame.init()
screen = pygame.display.set_mode((BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT))
pygame.display.set_caption("HexMapEdit")
clock = pygame.time.Clock()
running = True



create_grid(grid_width, grid_height)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_for_hex_fill(grid, mouse_pos)
            print(grid)
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    
    draw_grid(grid)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  
pygame.quit()