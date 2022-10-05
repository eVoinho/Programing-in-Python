import random
import json
from wolf import Wolf
from sheep import Sheep


def create_sheep_flock(size, pos_limit):
    list_of_sheep = []
    for i in range(size):
        list_of_sheep.append(Sheep(random.uniform(-pos_limit, pos_limit),
                                   random.uniform(-pos_limit, pos_limit), i))
    return list_of_sheep


def create_dict_to_json_file(sheep_list, wolf, round_number):
    sheep_pos_list = []
    for sheep in sheep_list:
        sheep_pos_list.append([sheep.get_x(), sheep.get_y()])
    return {"round_no": round_number, "wolf_pos": [wolf.get_x(), wolf.get_y()], "sheep_pos": sheep_pos_list}




## TODO: Zapytać kiedy ma być zapisywana informacja do jsona i kiedy mają być wświtalanae napisy (po ruchu czy przed ruchem)
def run_simulation(sheep_move, wolf_move, max_round, sheep_list, wolf):
    list_of_dicts = []
    for i in range(max_round):
        count = 0
        for sheep in sheep_list:
            if sheep.coordinates[0] is not None:
                sheep.move(sheep_move)
                count += 1
        if count == 0:
            print("<<<===>>> Wolf has eaten all sheep <<<===>>>")
            break
        print(f"Current wolf position is: {round(wolf.get_x(), 3)} {round(wolf.get_y(), 3)}")
        print(f"Number of round: {i}")
        print(f"Before wolf's move, there was {count} sheep")
        list_of_dicts.append(create_dict_to_json_file(sheep_list, wolf, i))
        wolf.try_to_eat_sheep(sheep_list, wolf_move)
    with open("pos.json", "w") as log:
        json.dump(list_of_dicts, log, indent=4)


if __name__ == "__main__":
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    flock_of_sheep_size = 15
    max_rounds = 50

    sheep = create_sheep_flock(flock_of_sheep_size, init_pos_limit)

    wolf = Wolf(0, 0)

    run_simulation(sheep_move_dist, wolf_move_dist, max_rounds, sheep, wolf)



