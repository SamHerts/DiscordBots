from PIL import Image, ImageDraw, ImageColor
import numpy as np
import os

colors = {
    'aqua':                 '#00FFFF',
    'blue':                 '#0000FF',
    'brown':                '#A52A2A',
    'chartreuse':           '#7FFF00',
    'coral':                '#FF7F50',
    'crimson':              '#DC143C',
    'darkgreen':            '#006400',
    'deeppink':             '#FF1493',
    'deepskyblue':          '#00BFFF',
    'goldenrod':            '#DAA520',
    'navajowhite':          '#FFDEAD',
    'fuchsia':              '#FF00FF',
    'black':                '#000000'
}

step = 20
# width = 10440
# height = 5220
thickness = 10
tank_resolution = 215

def get_tank(tank_health: int) -> Image.Image:
    curr_dir = os.getcwd()
    if not os.path.exists(curr_dir+'\Sprites\\1HTank.png'):
        curr_dir = curr_dir + "\BulletTank\Sprites"
    if tank_health == 1:
        tank_image = Image.open(curr_dir+'\\1HTank.png')
    elif tank_health == 2:
        tank_image = Image.open(curr_dir+'\\2HTank.png')
    elif tank_health == 3:
        tank_image = Image.open(curr_dir+'\\3HTank.png')
    elif tank_health == 4:
        tank_image = Image.open(curr_dir+'\\4HTank.png')
    return tank_image


def change_color(image: Image.Image, color: str) -> Image.Image:
    """
    Adjust the color of a sprite from black to given color
    """
    data = np.array(image.convert('RGBA'))
    color = ImageColor.getcolor(color, "RGB")
    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == 0) & (green == 0) & (blue == 0)
    data[:, :, :3][mask] = color

    return Image.fromarray(data)


def draw_grid(grid_step: int, grid_height: int, grid_width: int, debug=False) -> Image.Image:
    """
    Draws a game board grid with alpha values
    """

    image = Image.new(
        mode='RGBA',
        size=(grid_width*tank_resolution + thickness, grid_height*tank_resolution + thickness),
        color=(0, 0, 0, 130)
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
    if debug:
        print(
            f"Drawing a grid with parameters: {grid_step=}\n{grid_height=}\n{grid_width=}\n{thickness=}")
        image.show()
    del draw
    return image


def place_tank(board: Image.Image, health: int, coord: list, tank_color: str) -> Image.Image:
    """
    given coordinates relative to grid, place tank
    --need refactoring for different image sizes
    """

    #tank = tank_list.get(health)
    tank = get_tank(health)
    new_board = board.copy()
    board.close()
    x1, y1 = coord
    coord = x1 * tank_resolution + thickness + \
        1, y1 * tank_resolution + thickness + 66
    if tank_color is not None:
        tank = change_color(tank, tank_color)
    new_board.paste(tank, coord, tank.convert('RGBA'))
    tank.close()
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
