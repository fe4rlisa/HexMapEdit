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

text_col = WHITE

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

show_start_message = True
message = False
message_time = 0
show_menu = False

input_active = {"radius": False, "grid_width": False, "grid_height": False}
input_text = {"radius": str(radius), "grid_width": str(grid_width), "grid_height": str(grid_height)}

menu_width = screen_width / 3
menu_height = screen_height
menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
menu_surface.fill((0,0,0,128))

#-- Adds xy cords and type of tile to grid[] (list) --#
def create_grid(grid_width, grid_height):
    grid.clear()
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

def draw_menu():
    screen.blit(menu_surface, (0,0))
    menu_surface.fill((0,0,0,128))

    settings = ["radius", "grid_width", "grid_height"]
    spacing = menu_height // (len(settings) + 1)
    y_position = spacing

    for setting in settings:
        label_surface = menu_font.render(f"{setting}: ", True, text_col)
        input_surface = menu_font.render(input_text[setting], True, text_col)

        label_rect = label_surface.get_rect(center=(menu_width / 4, y_position))
        input_rect = pygame.Rect(menu_width / 2, y_position - 15, 30, 30)

        pygame.draw.rect(menu_surface, GRAY if input_active[setting] else BLUE3, input_rect)
        menu_surface.blit(label_surface, label_rect)
        menu_surface.blit(input_surface, input_rect.topleft)
        y_position += spacing

def handle_menu_events(event):
    global radius, grid_width, grid_height

    if event.type == pygame.MOUSEBUTTONDOWN:
        y_position = menu_height / 4
        for setting in input_active:
            input_rect = pygame.Rect(menu_width / 2, y_position - 15, 100, 30)
            if input_rect.collidepoint(event.pos):
                for key in input_active:
                    input_active[key] = False
                input_active[setting] = True
            y_position += menu_height / 4

    elif event.type == pygame.KEYDOWN:
        for setting, active in input_active.items():
            if active:
                if event.key == pygame.K_RETURN:
                    if setting == "radius":
                        radius = int(input_text[setting])
                    elif setting == "grid_width":
                        grid_width = int(input_text[setting])
                    elif setting == "grid_height":
                        grid_height = int(input_text[setting])
                elif event.key == pygame.K_BACKSPACE:
                    input_text[setting] = input_text[setting][:-1]
                else:
                    input_text[setting] += event.unicode

def show_message():
    global message, message_time
    message = True
    message_time = time.time()

def show_start_message():
    global start_message, message_time
    start_message = True
    message_time = time.time()

def draw_message(text):
    text_surface = font.render(text, True, text_col)
    text_rect = text_surface.get_rect(center=(screen_width // 2, 28))
    screen.blit(text_surface, text_rect)

def grid_to_json(grid):
    json_data = {
        "settings":{
            "radius": radius,
            "grid_width": grid_width,
            "grid_height": grid_height,
        },
        "tiles": []
    }
    for hex_dict in grid:
        for (x,y), value in hex_dict.items():
            json_data["tiles"].append({
                "x": x,
                "y": y,
                "value": value,
            })
    return json_data

def save_to_file():
    file_path = easygui.filesavebox(default="map_data.json", filetypes=["JSON files (*.json)"])
    if file_path:
        try:
            with open(file_path, "w") as f:
                json.dump(grid_to_json(grid), f, indent=4)
            show_message()
        except Exception as e:
            print("Error saving file:", e)    

def import_file():
    file_path = easygui.fileopenbox()
    if file_path:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                settings = data.get("settings", {})
                global radius, grid_width, grid_height
                radius = settings.get("radius", radius)
                grid_width = settings.get("grid_width", grid_width)
                grid_height = settings.get("grid_height", grid_height)
                grid.clear()
                for tile in data["tiles"]:
                    x = tile["x"]
                    y = tile["y"]
                    value = tile["value"]
                    grid.append({(x,y): value})
                return data
        except Exception as e:
            print("Error loading file", e)
            return None


pygame.init()
screen = pygame.display.set_mode((BASE_SCREEN_WIDTH, BASE_SCREEN_HEIGHT))
pygame.display.set_caption("HexMapEdit")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
menu_font = pygame.font.SysFont(None, 30)
running = True



create_grid(grid_width, grid_height)
show_start_message()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif show_menu:
            handle_menu_events(event)

        elif event.type == pygame.KEYDOWN:

            #-- Key binds go here --#
            if event.key == pygame.K_ESCAPE:
                running = False
            #elif event.key == pygame.K_SPACE:
            #    show_menu = not show_menu
            elif event.key == pygame.K_s:
                save_to_file()
            elif event.key == pygame.K_f:
                print("importing file...")
                import_file()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            check_for_hex_fill(grid, mouse_pos)
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLUE1)
    # RENDER YOUR GAME HERE
    
    draw_grid(grid)

    if show_start_message:
        draw_message("S to save and F to load file")
        if time.time() - message_time > 4:
            show_start_message = False
    if message:
        draw_message("File Saved!")
        if time.time() - message_time > 2:
            message = False

    if show_menu:
        draw_menu()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)
pygame.quit()