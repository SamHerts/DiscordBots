from math import dist, floor


class Player:

    def __init__(self, user_id="default user", color='black', coordinates: list = None):
        if coordinates is None:
            coordinates = [0, 0]
        self.user_id = user_id
        self.color = color
        self.coordinates = coordinates
        self.health = 4
        self.action_points = 3
        self.range = 1

    def __str__(self) -> str:
        return "{0}, your coordinates are {1}, and your color is {2}".format(self.user_id, self.coordinates, self.color)

    def move(self, direction, other_coords, max_size: list) -> bool:
        """
        Validate Direction, Action Points, and occupied, then move that direction.
        Directions are Cardinal - N,S,E,W and the four diagonals -NW, NE, SW, SE
        """
        # TODO: add debug
        # print(f"{self.coordinates=}, {direction=}, {other_coords=}")
        choices = {'W': (-1, 0),
                   'E': (1, 0),
                   'S': (0, 1),
                   'N': (0, -1),
                   'NW': (-1, -1),
                   'NE': (1, -1),
                   'SW': (-1, 1),
                   'SE': (1, 1)}
        action_taken = False
        if self.has_action():
            result = choices.get(direction, 'default')
            tmp_coordinates = [int(self.coordinates[0]) +
                               int(result[0]), int(self.coordinates[1]) + int(result[1])]
            if not (0 <= tmp_coordinates[0] < max_size[0]) or not (0 <= tmp_coordinates[1] < max_size[1]):
                # debug:print(f"outside of map: {tmp_coordinates=}")
                pass
            elif tmp_coordinates in other_coords:
                # debug:print(f"on top of someone: {tmp_coordinates=}")
                pass
            else:
                #debug: print(f"Able to move: {tmp_coordinates=}")
                self.coordinates = tmp_coordinates
                self.use_action()
                action_taken = True
        return action_taken

    def shoot(self, target):
        """
        Validate Action Points, and Target.
        """
        # debug:print(f"Shooting! With a range of {self.range}")
        if self.has_action() and check_range(self.coordinates, target.coordinates, self.range):
            # debug:print(f"{self.user_id} at location {self.coordinates} shot {target.user_id} at location {target.coordinates}!")
            self.use_action()
            self.range = 1
            return True
        else:
            # debug: print(f"{self.user_id} at location {self.coordinates} missed {target.user_id} at location {target.coordinates}!")
            return False

    def give_action(self, target):
        """
        Validate Distance??, and Number of Actions points > 2, then give to target.
        """
        if self.has_action():
            self.use_action()
            return True
        else:
            return False

    def increase_range(self):
        """
        Validate Action points and increase range
        """
        if self.has_action() and self.range < 3:
            self.use_action()
            self.range += 1
            return True
        else:
            return False

    def take_damage(self, amount=1):
        if self.health > 1:
            self.health = self.health - amount
            return True
        else:
            return False

    def has_action(self):
        return self.action_points

    def use_action(self):
        if self.has_action():
            self.action_points -= 1


def check_range(first_coordinates, second_coordinates, max_range):
    """
    Check if the first coordinates are within the distance of the second coordinates
    """
    # debug: print(f"First Coords: {first_coordinates}\nSecond Coords: {second_coordinates}\nDistance: {dist(first_coordinates, second_coordinates)}")
    return floor(dist(first_coordinates, second_coordinates)) <= max_range
