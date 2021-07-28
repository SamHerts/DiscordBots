from PIL import Image, ImageDraw
import numpy as np

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
Colors = [RED, GREEN, BLUE, None]
step = 20
width = 10440
height = 5220
thickness = 10


# noinspection PyTypeChecker
def change_color(image: Image.Image, color: list) -> Image.Image:
    data = np.array(image.convert('RGBA'))

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == 0) & (green == 0) & (blue == 0)
    data[:, :, :3][mask] = color

    return Image.fromarray(data)


def draw_grid(grid_step, grid_height, grid_width, pixel_thickness):
    image = Image.new(
        mode='RGBA',
        size=(grid_width + pixel_thickness, grid_height + pixel_thickness),
        color=(255, 255, 255, 0)
    )
    draw = ImageDraw.Draw(image)

    y_start = 0
    y_end = image.height
    step_size = int(image.width / step)

    for x in range(0, image.width, step_size):
        line = ((x + int(thickness / 2) - 1, y_start), (x + (thickness / 2) - 1, y_end))
        draw.line(line, fill=(0, 0, 0, 255), width=thickness)

    x_start = 0
    x_end = image.width

    for y in range(0, image.height, step_size):
        line = ((x_start, y + int(thickness / 2) - 1), (x_end, y + int(thickness / 2) - 1))
        draw.line(line, fill=(0, 0, 0, 255), width=thickness)

    del draw
    return image


def place_tank(board, tank, coord, tank_color):
    x1, y1 = coord
    coord = x1 * 522 + thickness, y1 * 522 + thickness
    if tank_color is not None:
        tank = change_color(tank, tank_color)
    board.paste(tank, coord, tank)
    return board


def rainbow_tank(image):
    for x in range(0, 20):
        for y in range(0, 10):
            color = Colors[(x + y) % 4]
            image = place_tank(image, fullTank_img, (x, y), color)
    return image


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fullTank_img = Image.open(r'.\4HTank.png')
    Board = draw_grid(step, height, width, thickness)
    Board.save(r'.\Board.png')
    rainbow_board = rainbow_tank(Board)
    rainbow_board.show()
