from math import dist, floor


class Player:
    user_id = 0
    health = 4
    color = (0, 0, 0)
    action_points = 3
    range = 1
    coordinates = [0, 0]
    x_start = 0
    y_start = 0
    x_end = 19
    y_end = 9

    def __init__(self, user_id, color, coordinates=None):
        if coordinates is None:
            coordinates = [0, 0]
        self.user_id = user_id
        self.color = color
        self.coordinates = coordinates

    def move(self, direction) -> bool:
        """
        Validate Direction, Action Points, and occupied, then move that direction.
        Directions are Cardinal - N,S,E,W and the four diagonals -NW, NE, SW, SE
        """
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
            tmp_coordinates = [self.coordinates[0] +
                               result[0], self.coordinates[1] + result[1]]
            if (self.x_start < tmp_coordinates[0] < self.x_end) or (self.y_start < tmp_coordinates[1] < self.y_end):
                pass
            else:
                self.coordinates = tmp_coordinates
                self.use_action()
                action_taken = True
        return action_taken

    def shoot(self, target):
        """
        Validate Action Points, and Target.
        """
        print(f"Shooting! With a range of {self.range}")
        if self.has_action() and check_range(self.coordinates, target.coordinates, self.range):
            print(
                f"{self.user_id} at location {self.coordinates} shot {target.user_id} at location {target.coordinates}!")
            self.use_action()
            return True
        else:
            print(
                f"{self.user_id} at location {self.coordinates} missed {target.user_id} at location {target.coordinates}!")
            return False

    def give_action(self, target):
        """
        Validate Distance??, and Number of Actions points > 2, then give to target.
        """
        if self.has_action() and check_range(self.coordinates, target, self.range):
            self.use_action()
            return True
        else:
            return False

    def increase_range(self):
        """
        Validate Action points and increase range
        """
        if self.has_action():
            self.use_action()
            self.range += 1
            return True
        else:
            return False

    def take_damage(self, amount=1):
        if self.health > 0:
            self.health = self.health - amount

    def has_action(self):
        return self.action_points

    def use_action(self):
        if self.has_action():
            self.action_points -= 1


def check_range(first_coordinates, second_coordinates, max_range):
    """
    Check if the first coordinates are within the distance of the second coordinates
    """
    print(
        f"First Coords: {first_coordinates}\nSecond Coords: {second_coordinates}\nDistance: {dist(first_coordinates, second_coordinates)}")
    return floor(dist(first_coordinates, second_coordinates)) <= max_range


if __name__ == '__main__':
    print("This is a Player class, no need to run this as main.")
