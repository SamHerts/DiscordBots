from discord.ext.commands.core import check
from . import Player
from . import Display
from PIL import Image, ImageDraw
import numpy as np

"""
Driver needs to take input and follow logic rules

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

blank_grid = Display.grid
number_of_players = 4
players_list = []
game_running = False
curr_grid = blank_grid


def distribute_action_points(target, amount):
    print(f"Distributing {amount} to {target.user_id}")

    target.action_points += amount

    return target


def update_grid():
    new_grid = blank_grid.copy()
    for x in players_list:
        new_grid = Display.place_tank(
            new_grid, x.health, x.coordinates, x.color)

    return new_grid


def generate_coordinates():
    x = np.random.randint(0, 19)
    y = np.random.randint(0, 9)
    return x, y


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


def add_user(player_name):
    if not game_running and len(players_list) < number_of_players and not check_if_playing(player_name):

        players_list.append(Player.Player(
            user_id=player_name, color=Display.colors[len(players_list)], coordinates=get_valid_random_coordinates()))
        return True
    else:
        return False


def move_player(user_id, dir):
    for p in players_list:
        if p.user_id == user_id:
            return p.move(dir)


def admin_administer_points():
    for p in players_list:
        distribute_action_points(p, 1)


def get_ac_points(user_id):
    for p in players_list:
        if user_id == p.user_id:
            return p.action_points


def shoot_player(shooter, shootee):
    pass


if __name__ == '__main__':
    for player in range(number_of_players):
        players_list.append(Player.Player(
            user_id=player, color=Display.colors[player]))

    players_list[0].coordinates = [0, 0]
    players_list[1].coordinates = [19, 0]
    players_list[2].coordinates = [0, 9]
    players_list[3].coordinates = [19, 9]

    curr_grid = update_grid()
    curr_grid.show()

    players_list[0] = distribute_action_points(players_list[0], 10)
    print(players_list[0].action_points)
    for x in range(6):
        if players_list[0].move("S"):
            print("Move Successful")
        else:
            print("Could not move")
    curr_grid = update_grid()
    curr_grid.show()
    if players_list[0].shoot(players_list[2]):
        print("Shots fired! And a hit!!!")
    else:
        print("Shots fired! And a miss! Oh no!")

    curr_grid = update_grid()
    curr_grid.show()

    print(
        f"{players_list[0].user_id} has {players_list[0].action_points} left")

    if players_list[0].increase_range():
        print("Range Increased!")
    else:
        print("not enough action points!")

    if players_list[0].increase_range():
        print("Range Increased!")
    else:
        print("not enough action points!")

    if players_list[0].shoot(players_list[2]):
        print("Shots fired! And a hit!!!")
        players_list[2].take_damage(1)
    else:
        print("Shots fired! And a miss! Oh no!")

    curr_grid = update_grid()
    curr_grid.show()
