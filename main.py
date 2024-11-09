import matplotlib.pyplot as plt 
import matplotlib.patches as patches
import numpy as np

w, h = 500,500

pixels_x = .9 * w
pixels_y = .9 * h

radius = 10

sep_x = 3 * radius
sep_y = (np.sqrt(3) / 2) * radius


grid_x = int(pixels_x / sep_x) + 1
grid_y = int(pixels_y / sep_y) + 1


def draw_hexagon(ax, x, y, radius):
    angles = np.linspace(0, 2 * np.pi, 7)
    hexagon_vertices = [(x + radius * np.cos(angle), y + radius * np.sin(angle)) for angle in angles]


    hexagon = patches.Polygon(hexagon_vertices, 
    edgecolor="black", facecolor="none", linewidth=2)

    #circle = patches.Circle((x,y), radius,
    #edgecolor='black', facecolor='none', linewidth=2)
    #ax.add_patch(circle)   //hexagon logic based off of this

    ax.add_patch(hexagon)

def setup():
    fig, ax = plt.subplots(figsize=(10,8))
    ax.set_aspect('equal')
    plt.xlim(0, w)
    plt.ylim(0, h)
    return fig, ax



def draw_grid(ax):
    current_x = w / 2 - pixels_x / 2
    current_y = h / 2 - pixels_y / 2
    for i in range(grid_y):
        if (i%2 == 0):
            current_x += 1.5 * radius
        for j in range(grid_x):
            draw_hexagon(ax, current_x, current_y, radius)

            current_x += sep_x
        current_x = w / 2 - pixels_x / 2
        current_y += sep_y

    plt.show()

def main():
    fig, ax = setup()
    draw_grid(ax)

if __name__ == '__main__':
    main()