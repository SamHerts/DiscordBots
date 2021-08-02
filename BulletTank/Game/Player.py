from math import dist


class Player:
    user_id = 0
    health = 4
    color = (0, 0, 0)
    action_points = 0
    range = 1
    coordinates = [0, 0]
    x_start = 0
    y_start = 0
    x_end = 19
    y_end = 19

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
        choices = {'N': (-1, 0),
                   'S': (1, 0),
                   'E': (0, 1),
                   'W': (0, -1),
                   'NW': (-1, -1),
                   'NE': (-1, 1),
                   'SW': (1, -1),
                   'SE': (1, 1)}
        action_taken = False
        if self.has_action():
            result = choices.get(direction, 'default')
            if self.coordinates[0] == self.x_start and (direction == 'N' or direction == 'NW' or direction == 'NE'):
                pass
            elif self.coordinates[0] == self.x_end and (direction == 'S' or direction == 'SW' or direction == 'SE'):
                pass
            elif self.coordinates[1] == self.y_start and (direction == 'W' or direction == 'SW' or direction == 'NW'):
                pass
            elif self.coordinates[1] == self.y_end and (direction == 'E' or direction == 'SE' or direction == 'NE'):
                pass
            else:
                self.coordinates = [self.coordinates[0] + result[0], self.coordinates[1] + result[1]]
                self.use_action()
                action_taken = True
        return action_taken

    def shoot(self, target):
        """
        Validate Action Points, and Target.
        """
        if self.has_action() and check_range(self.coordinates, target, self.range):
            self.use_action()
            return True
        else:
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

    def take_damage(self, amount):
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
    return dist(first_coordinates, second_coordinates) < max_range


if __name__ == '__main__':
    print("This is a Player class, no need to run this as main.")