from PIL import Image, ImageDraw
import numpy as np
import os


colors = {'WHITE': [255, 255, 255],
          'RED': [255, 0, 0],
          'PURPLE': [255, 0, 255],
          'GREEN': [0, 128, 0],
          'OLIVE': [128, 128, 0],
          'YELLOW': [250, 250, 0],
          'BLUE': [0, 0, 255],
          'AQUA': [0, 255, 255]}
step = 20
width = 10440
height = 5220
thickness = 10

four_tank = Image.open(os.getcwd()+'\Sprites\\4HTank.png')
three_tank = Image.open(os.getcwd()+'\Sprites\\3HTank.png')
two_tank = Image.open(os.getcwd()+'\Sprites\\2HTank.png')
one_tank = Image.open(os.getcwd()+'\Sprites\\1HTank.png')
grid = Image.open(os.getcwd()+'\Sprites\Board.png')

tank_list = {1: one_tank, 2: two_tank, 3: three_tank, 4: four_tank}


def change_color(image: Image.Image, color: list) -> Image.Image:
    """
    Adjust the color of a sprite from black to given color
    """
    data = np.array(image.convert('RGBA'))

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == 0) & (green == 0) & (blue == 0)
    data[:, :, :3][mask] = color

    return Image.fromarray(data)


def draw_grid(grid_step, grid_height, grid_width, pixel_thickness):
    """
    Draws a game board grid with alpha values - needs refactoring for different sizes and shapes
    """

    image = Image.new(
        mode='RGBA',
        size=(grid_width + pixel_thickness, grid_height + pixel_thickness),
        color=(255, 255, 255, 15)
    )
    draw = ImageDraw.Draw(image)

    x_start = y_start = 0
    y_end = image.height
    x_end = image.width
    step_size = int(image.width / grid_step)

    for x in range(0, image.width, step_size):
        line = ((x + int(thickness / 2) - 1, y_start),
                (x + (thickness / 2) - 1, y_end))
        draw.line(line, fill=(0, 0, 0, 255), width=thickness)

    for y in range(0, image.height, step_size):
        line = ((x_start, y + int(thickness / 2) - 1),
                (x_end, y + int(thickness / 2) - 1))
        draw.line(line, fill=(0, 0, 0, 255), width=thickness)

    del draw
    return image


def place_tank(board, health, coord, tank_color):
    """
    given coordinates relative to grid, place tank
    --need refactoring for different image sizes
    """
    tank = tank_list.get(health)
    new_board = board.copy()
    x1, y1 = coord
    coord = x1 * 522 + thickness, y1 * 522 + thickness
    if tank_color is not None:
        tank = change_color(tank, tank_color)
    new_board.paste(tank, coord, tank.convert('RGBA'))
    return new_board


def rainbow_tank(board: Image.Image) -> Image.Image:
    """
    Fun function to create a rainbow patterned board
    """
    for x in range(0, 20):
        for y in range(0, 10):
            color = colors[(x + y) % 4]
            board = place_tank(board, 4, (x, y), color)
    return board
