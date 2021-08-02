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

grid = Display.grid
number_of_players = 4
players_list = []


def distribute_action_points(target, amount):
    if target is list:
        for x in target:
            x.action_points += amount
    elif target is Player.Player:
        target.action_points += amount
    elif target == "All":
        for x in players_list:
            x.action_points += amount


def update_grid(old_grid):
    for x in players_list:
        old_grid = Display.place_tank(old_grid, Display.four_tank, player.coordinates, player.color)

    old_grid.show()
    return old_grid


if __name__ == '__main__':
    for player in range(number_of_players):
        players_list.append(Player.Player(user_id=player, color=Display.colors[player]))

    players_list[0].coordinates = [0, 0]
    players_list[1].coordinates = [19, 0]
    players_list[2].coordinates = [0, 9]
    players_list[3].coordinates = [19, 9]

    grid = update_grid()
    distribute_action_points("All")
