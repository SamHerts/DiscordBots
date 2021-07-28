class Player:
    user_id = None
    health = 4
    color = None
    action_points = 0
    range = 1

    def move(self, direction):
        """
        Validate Direction, Action Points, and occupied, then move that direction.
        """
        pass

    def shoot(self, target):
        """
        Validate Action Points, and Target, then give damage to target.
        """
        pass

    def give_action(self, target):
        """
        Validate Distance??, and Number of Actions points > 2, then give to target.
        """
        pass

    def take_damage(self, amount):
        pass
