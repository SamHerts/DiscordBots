from discord.ext.commands.core import check
from utils import CustomExceptions as ce
from numpy.random.mtrand import randint

try:
    from . import Display
    from . import Player
except ImportError:
    try:
        import Display
        import Player
    except ImportError:
        raise


blank_grid = None
grid_size = [20, 10]
number_of_players = 12
players_list = []
game_running = False
curr_grid = blank_grid


def get_index(source, target=None):
    """
    Attempts to find the given user_id's, otherwise returns None
    """
    friend = enemy = None
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


def distribute_action_points(target: Player, amount: int):
    """
    Increase the amount of action points a player has
    """
    print(f"Distributing {amount} to {target.user_id}")

    target.action_points += amount

    return True


def update_grid():
    """
    Takes all active players and returns a populated grid
    """
    new_grid = blank_grid.copy()
    for x in players_list:
        new_grid = Display.place_tank(
            new_grid, x.health, x.coordinates, Display.colors[x.color])

    return new_grid


def generate_coordinates(boundary):
    """
    Returns a pair of randomized coordinates
    """
    x = randint(0, boundary[0]-1)
    y = randint(0, boundary[1]-1)
    return [x, y]


def check_valid_coords(coordinates: list):
    """
    Ensures coordinates are not already taken
    """
    if len(players_list):
        for p in players_list:
            if coordinates == p.coordinates:
                return False
    return True


def get_valid_random_coordinates(grid_size):
    """
    Continues to generate rando coordinates until successful
    """
    while True:
        try:
            coords = generate_coordinates(grid_size)
        except:
            continue

        if not check_valid_coords(coords):
            continue
        else:
            break
    return coords


def check_if_playing(player: str):
    if get_index(player) is None:
        raise ce.not_playing



def get_alive():
    """
    Returns the total count of active players
    """
    return len(players_list)


def add_user(player_name: str, debug=False, color=None, coords=None, health=None, actions=None):
    """
    Creates a Player object and appends it to the active player list
    """
    try:
        check_if_playing(player_name)
    except ce.not_playing:
        if debug:
            new_player = Player.Player(
            user_id=player_name, color=color, coordinates=coords)
            print(f"{new_player=}")
            new_player.health = health
            new_player.action_points = actions
            players_list.append(new_player)
        elif not len(players_list) < number_of_players:
            raise ce.too_many_players
        else:
            new_player = Player.Player(user_id=player_name, color=list(
            Display.colors)[len(players_list)], coordinates=[0, 0])
            players_list.append(new_player)


def move_player(user_id, dir: str):
    friend = get_index(user_id)
    try:
        players_list[friend].move(dir, get_all_coords(), grid_size)
    except ce.out_of_bounds:
        print("Got out of bounds exception")
        raise
    except ce.occupied_space:
        print("Got occupied space exception")
        raise
    except ce.out_of_actions:
        print("Got out of actions exception")
        raise


def admin_administer_points(amount: int):
    for p in players_list:
        distribute_action_points(p, amount)


def send_ac_point(source, target):
    friend, enemy = get_index(source, target)
    try:
        players_list[friend].give_action(players_list[enemy]) 
        distribute_action_points(players_list[enemy], 1)
    except ce.out_of_actions:
        print("Cannot give an action, because you don't have any!")
        raise


def get_ac_points(user_id):
    friend = get_index(user_id)
    return players_list[friend].action_points


def shoot_player(source, target):
    friend, enemy = get_index(source, target)
    try:
        players_list[friend].shoot(players_list[enemy])
        players_list[enemy].take_damage()
            # del players_list[enemy]
            #return True
    except ce.out_of_actions:
        print("You can't shoot them, you don't have any actions!")
        raise
    except ce.out_of_range:
        print("You're not close enough to shoot them!")
        raise
    except ce.health_is_zero:
        print("You've killed them!!")


def increase_range(user_id):
    index = get_index(user_id)
    try:
        players_list[index].increase_range()
    except:
        raise


def get_all_coords():
    coords_list = []
    for p in players_list:
        coords_list.append(list(p.coordinates))
    return coords_list


def where_the_fuck_am_i(author):
    index = get_index(author)
    return str(players_list[index].coordinates)


def get_user_color(author):
    index = get_index(author)
    return str(players_list[index].color)


def start_game(grid_length, grid_height, debug=False):
    """
    Initializes game board and places players within boundaries
    """
    global game_running
    # global number_of_players
    global grid_size
    global blank_grid
    grid_size = [grid_length, grid_height]
    for index, p in enumerate(players_list):
        p.coordinates = get_valid_random_coordinates(grid_size)
        if debug:
            if index == 0:
                p.coordinates = [0, 0]
                p.action_points = 100
            if index == 1:
                p.coordinates = [4, 0]
            print(f"{p.user_id=}")
            print(f"{p.coordinates=}")
    game_running = True

    blank_grid = Display.draw_grid(grid_step=grid_length, grid_width=grid_length,
                                   grid_height=grid_height, debug=debug)

    return "\n".join(str(i) for i in players_list)
