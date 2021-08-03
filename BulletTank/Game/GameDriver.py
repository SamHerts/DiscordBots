import Player
import Display
from PIL import Image, ImageDraw

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
