import logging
from chase.animal import Animal
import math


class Wolf(Animal):
    def __init__(self, coord_x, coord_y):
        super().__init__(coord_x, coord_y)

    def find_closest_sheep(self, sheep_list):
        logging.debug("find_closest_sheep called")
        distance = -1
        index = 0
        for new_index, sheep in enumerate(sheep_list):
            if sheep.coordinates[0] is not None:
                new_distance = math.dist(self.coordinates, sheep.coordinates)
                if distance == -1 or distance > new_distance:
                    distance = new_distance
                    index = new_index
        logging.debug(f"find_closest_sheep returned sheep index = {index} and distance = {distance}")
        return distance, index

    def try_to_eat_sheep(self, sheep_list, move_dist):
        logging.info("Wolf checks if eating sheep is possible. If not then chase nearest one")
        logging.debug("try_to_eat_sheep function called")
        distance, index = self.find_closest_sheep(sheep_list)
        nearest_sheep = sheep_list[index]
        if distance > move_dist:
            logging.debug(f"Wolf is chasing sheep")
            print(f"Wolf is chasing sheep with ID = {nearest_sheep.ID}")
            vector = (nearest_sheep.get_x() - self.get_x(),
                      nearest_sheep.get_y() - self.get_y())
            unitVector = (vector[0] / distance, vector[1] / distance)
            self.coordinates[0] += (unitVector[0] * distance)
            self.coordinates[1] += (unitVector[1] * distance)
            logging.info(f"""Wolf is chasing sheep with id = {nearest_sheep.ID} 
                            His current coordinates are ({self.coordinates[0]};{self.coordinates[1]})""")

        else:
            logging.debug(f"Wolf has eaten sheep")
            print(f"Wolf has eaten sheep with ID = {nearest_sheep.ID}")
            self.coordinates[0] += (nearest_sheep.get_x())
            self.coordinates[1] += (nearest_sheep.get_x())
            sheep_list[index].coordinates[0] = None
            sheep_list[index].coordinates[1] = None
            logging.info(f"""Wolf has eaten sheep with id = {nearest_sheep.ID} 
                            His current coordinates are ({self.coordinates[0]};{self.coordinates[1]})""")
