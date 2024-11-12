import sys
import json
import time
import pygame
import easygui
import numpy as np


BLACK = (23, 14, 25)
BLUE1 = (47, 33, 59)
BLUE2 = (67, 58, 96)
BLUE3 = (101, 115, 140)
BROWN = (96, 59, 58)
GREEN1 = (58, 96, 74)
GREEN2 = (33, 59, 37)
VIOLET = (110, 81, 129)
WHITE = (255, 255, 255) 
GRAY = (200,200,200)

BASE_SCREEN_WIDTH = 800
BASE_SCREEN_HEIGHT = 600

screen_width, screen_height = 800,600
screen_center = (screen_width/2, screen_height/2)


radius = 34
hex_width = np.sqrt(3) * radius
hex_height = 3 / 2 * radius
grid_width = 10
grid_height = 10
grid = []

color_mapping= {
    0: BLUE2,
    1: BLUE3,
    2: BROWN,
    3: GREEN1,
    4: GREEN2,
}

show_message = False
message_time = 0

#-- Adds xy cords and type of tile to grid[] (list) --#
def create_grid(grid_width, grid_height):
    for y in range(grid_height):
        for x in range(grid_width):
            grid.append({(x,y): 0})
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
                color = color_mapping[hex_dict[key]]
                pygame.draw.polygon(screen, color, hexagon_vertices)
               
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
                    hex_dict[key] = (hex_dict[key] + 1) %len(color_mapping)
                break

def show_save_message():
    global show_message, message_time
    show_message = True
    message_time = time.time()

def draw_message(text):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(screen_width // 2, 28))
    screen.blit(text_surface, text_rect)

def grid_to_json(grid):
    json_grid = []
    for hex_dict in grid:
        for (x,y), value in hex_dict.items():
            json_grid.append({
                "x": x,
                "y": y,
                "value": value,
            })
    return json_grid

def save_to_file():
    file_path = easygui.filesavebox(default="map_data.json", filetypes=["JSON files (*.json)"])
    if file_path:
        try:
            with open(file_path, "w") as f:
                json.dump(grid_to_json(grid), f, indent=4)
            show_save_message()
        except Exception as e:
            print("Error saving file:", e)    


pygame.init()
screen = pygame.display.set_mode((BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT))
pygame.display.set_caption("HexMapEdit")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
running = True



create_grid(grid_width, grid_height)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            #-- Key binds go here --#
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s:
                save_to_file()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_for_hex_fill(grid, mouse_pos)
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLUE1)
    # RENDER YOUR GAME HERE
    
    draw_grid(grid)

    if show_message:
        draw_message("File Saved!")
        if time.time() - message_time > 2:
            show_message = False

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)
pygame.quit()