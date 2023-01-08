import logging
import random
from chase.animal import Animal


class Sheep(Animal):
    def __init__(self, coord_x, coord_y, identity):
        super().__init__(coord_x, coord_y)
        self.ID = identity

    def move(self, move_dist):
        logging.debug(f"move method is called for sheep with id = {self.ID}")
        direction = ["north", "south", "west", "east"]
        choice = random.choice(direction)
        logging.info(f"Sheep with ID = {self.ID} moves in the direction of {choice}")
        match choice:
            case "north":
                self.coordinates[1] += move_dist
            case "south":
                self.coordinates[1] -= move_dist
            case "west":
                self.coordinates[0] -= move_dist
            case "east":
                self.coordinates[0] += move_dist
        logging.debug(f"Sheep new coordinates are ({self.coordinates[0]};{self.coordinates[1]})")
