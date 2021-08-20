# from discord import player
from discord import user
# from discord.ext.commands.core import check
# from . import Player
# from . import Display
import Display
from Player import Player
# from PIL import Image, ImageDraw
import numpy as np

"""
Rules:

Last Player standing wins.
Each day, players receive at least 1 Action Point.
Action points are lost upon use
Action points can be transferred to other players
Actions you can take:
Move one space
Shoot at a player within range
Increase range - up to 3
Transfer an Action Point to another Player
Each Player starts with 4 hearts, if you run out of hearts you die.
Defeated Players are added to the Angel Box and vote to give out bonus Action Points.
A player must receive 30% of the vote to receive the Action Point
"""

blank_grid = None
grid_size = [20, 10]
# number_of_players = 4
players_list = []
game_running = False
curr_grid = blank_grid


def distribute_action_points(target, amount):
    print(f"Distributing {amount} to {target.user_id}")

    target.action_points += amount

    return True


def update_grid():
    new_grid = blank_grid.copy()
    for x in players_list:
        new_grid = Display.place_tank(
            new_grid, x.health, x.coordinates, Display.colors[x.color])

    return new_grid


def generate_coordinates():
    x = np.random.randint(0, grid_size[0]-1)
    y = np.random.randint(0, grid_size[1]-1)
    return [x, y]


def check_valid_coords(coordinates):
    if len(players_list):
        for p in players_list:
            if coordinates == p.coordinates:
                return False
    return True


def get_valid_random_coordinates():
    while True:
        try:
            coords = generate_coordinates()
        except:
            continue

        if not check_valid_coords(coords):
            continue
        else:
            break
    return coords


def check_if_playing(player):
    for p in players_list:
        if player == p.user_id:
            return True
    return False


def add_user(player_name, debug=False):
    # if not game_running and len(players_list) < number_of_players and not check_if_playing(player_name):
    if not game_running and not check_if_playing(player_name):
        new_player = Player(user_id=player_name, color=list(Display.colors)[len(players_list)], coordinates=[0, 0])
        if debug:
            print(f"{new_player=}")
        players_list.append(new_player)
        return True
    else:
        return False


def move_player(user_id, dir: str):
    friend = get_index(user_id)
    return players_list[friend].move(dir, get_all_coords(), grid_size)


def admin_administer_points(amount: int):
    for p in players_list:
        distribute_action_points(p, amount)


def send_ac_point(source, target):
    friend, enemy = get_index(source, target)
    return players_list[friend].give_action(players_list[enemy]) and distribute_action_points(players_list[enemy], 1)


def get_ac_points(user_id):
    friend = get_index(user_id)
    return players_list[friend].action_points


def shoot_player(source, target):
    friend, enemy = get_index(source, target)
    if players_list[friend].shoot(players_list[enemy]):
        if players_list[enemy].take_damage():
            return True
        else:
            del players_list[enemy]
            return True
    return False


def increase_range(user_id):
    index = get_index(user_id)
    return players_list[index].increase_range()


def get_index(source, target=None):
    if target is not None:
        for index, p in enumerate(players_list):
            if p.user_id == source:
                friend = index
            if p.user_id == target:
                enemy = index
        return friend, enemy
    else:
        for index, p in enumerate(players_list):
            if p.user_id == source:
                friend = index
        return friend


def get_all_coords():
    coords_list = []
    for p in players_list:
        coords_list.append(list(p.coordinates))
    return coords_list


def start_game(grid_length, grid_height, debug=False):
    global game_running
    # global number_of_players
    global grid_size
    global blank_grid
    grid_size = [grid_length, grid_height]
    for index, p in enumerate(players_list):
        
        temp = get_valid_random_coordinates()
        p.coordinates = temp
        if debug:
            if index == 0:
                p.coordinates = [0, 0]
                p.action_points = 100
            if index == 1:
                p.coordinates = [4, 0]
            print(f"{p.user_id=}")
            print(f"{p.coordinates=}")
    game_running = True
    # number_of_players = num_players

    grid_pixel_length = 522*grid_length
    grid_pixel_height = 522*grid_height
    blank_grid = Display.draw_grid(grid_step=grid_length, grid_width=grid_pixel_length,
                                   grid_height=grid_pixel_height, pixel_thickness=10, debug=debug)

    return "\n".join(str(i) for i in players_list)


if __name__ == '__main__':
    global_debug = True
    print("Debugging Logic")
    add_user("alpha", debug=global_debug)
    add_user("beta", debug=global_debug)
    add_user("gamma", debug=global_debug)
    if True:
        add_user("delta")
        add_user("epsilon")
        add_user("zeta")
        add_user("eta")
        add_user("theta")
        add_user("iota")
        add_user("kappa")
    start_game(20, 20, debug=global_debug)
    print("Attempting to move alpha N: ",move_player(players_list[0].user_id, "N"))
    print("Attempting to move alpha W: ",move_player(players_list[0].user_id, "W"))
    print("Attempting to move alpha E: ",move_player(players_list[0].user_id, "E"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to give an action point: ", send_ac_point("alpha", "beta"))
    print("Attempting to increase range: ", increase_range("alpha"))
    print("Attempting to give an action point: ", send_ac_point("alpha", "beta"))
    print("Attempting to shoot beta: ", shoot_player("alpha", "beta"))
    print("Showing grid\n")
    update_grid().show()

