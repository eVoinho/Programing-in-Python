import random
from animal import Animal


class Sheep(Animal):
    def __init__(self, coord_x, coord_y, identity):
        super().__init__(coord_x, coord_y)
        self.ID = identity

    def move(self, move_dist):
        direction = ["north", "south", "west", "east"]
        choice = random.choice(direction)
        match choice:
            case "north":
                self.coordinates[1] += move_dist
            case "south":
                self.coordinates[1] -= move_dist
            case "west":
                self.coordinates[0] -= move_dist
            case "east":
                self.coordinates[0] += move_dist
