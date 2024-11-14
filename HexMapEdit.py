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


radius = 36
hex_width = np.sqrt(3) * radius
hex_height = 3 / 2 * radius
grid_width = 8
grid_height = 8
grid = {}

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
            grid[(x,y)] = {"type": 0}
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
            grid_index = (x, y)

            if grid_index not in grid:
                continue

            hex_dict = grid[grid_index]
            color = color_mapping[hex_dict["type"]]
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
                grid_index = (x, y)
                hex_dict = grid[grid_index]
                for key in hex_dict:
                    hex_dict[key] = (hex_dict[key] + 1) %len(color_mapping)
                break



def draw_menu():
    screen.blit(menu_surface, (0,0))
    menu_surface.fill((0,0,0,128))

    settings = {"radius": "Radius",
     "grid_width": "Grid Width",
     "grid_height": "Grid Height",
    }
    spacing = menu_height // (len(settings) + 1)
    y_position = spacing

    for var_name, display in settings.items():
        current_value = globals()[var_name]
        label_surface = menu_font.render(f"{display}: {current_value}", True, text_col)
        label_rect = label_surface.get_rect(center=( menu_width * 2 / 4, y_position))
        menu_surface.blit(label_surface, label_rect)

        minus_rect = pygame.Rect(label_rect.left - 50, y_position - 10, 20, 20)
        pygame.draw.rect(menu_surface, GRAY, minus_rect)
        minus_text = menu_font.render(" -",True, BLACK)
        menu_surface.blit(minus_text, minus_rect.topleft)

        plus_rect = pygame.Rect(label_rect.right + 30, y_position - 10, 20, 20)
        pygame.draw.rect(menu_surface, GRAY, plus_rect)
        plus_text = menu_font.render(" +", True, BLACK)
        menu_surface.blit(plus_text, plus_rect.topleft)

        input_active[var_name + "_minus"] = minus_rect
        input_active[var_name + "_plus"] = plus_rect

        y_position += spacing

def handle_menu_events(event):
    global radius, grid_width, grid_height, hex_width, hex_height, grid

    temp_grid = {k: v for k, v in grid.items()}

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        for setting in ["radius", "grid_width", "grid_height"]:
            if input_active[setting + "_minus"].collidepoint(mouse_pos):
                if setting == "radius":
                    radius -= 2
                    input_text[setting] = str(radius)
                elif setting == "grid_width":
                    grid_width -= 1
                    input_text[setting] = str(grid_width)
                elif setting == "grid_height":
                    grid_height -= 1
                    input_text[setting] = str(grid_width)
                create_grid(grid_width, grid_height)

            elif input_active[setting + "_plus"].collidepoint(mouse_pos):
                if setting == "radius":
                    radius += 2
                    input_text[setting] = str(radius)
                elif setting == "grid_width":
                    grid_width += 1
                    input_text[setting] = str(grid_width)
                elif setting == "grid_height":
                    grid_height += 1
                    input_text[setting] = str(grid_width)

        hex_width = np.sqrt(3) * radius
        hex_height = 3 / 2 * radius

        new_grid = create_grid(grid_width, grid_height)
        for (x,y), value in temp_grid.items():
            if x < grid_width and y < grid_height:
                new_grid[(x,y)] = value

        grid = new_grid
        

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
    for (x, y), hex_dict in grid.items():
        json_data["tiles"].append({
            "x": x,
            "y": y,
            "value": hex_dict["type"],
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
                    grid[(x,y)] = {"type": value}
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
        

        elif event.type == pygame.KEYDOWN:

            #-- Key binds go here --#
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                show_menu = not show_menu
            elif event.key == pygame.K_s:
                save_to_file()
            elif event.key == pygame.K_f:
                print("importing file...")
                import_file()        

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not show_menu:
                check_for_hex_fill(grid, mouse_pos)
            else:
                handle_menu_events(event)
        
        
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