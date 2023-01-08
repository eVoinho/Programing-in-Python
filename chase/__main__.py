import logging
import os
import random
import json
import csv
import argparse
from configparser import ConfigParser
from chase.wolf import Wolf
from chase.sheep import Sheep


def create_sheep_flock(size, pos_limit):
    list_of_sheep = []
    for i in range(size):
        list_of_sheep.append(Sheep(random.uniform(-pos_limit, pos_limit),
                                   random.uniform(-pos_limit, pos_limit), i))
    logging.info("There is ", size, " sheep in the flock.")
    logging.debug("Function create_sheep_flock called and performed"
                  "Flock size: " + str(size) + " Initial position limit: " + str(pos_limit))
    return list_of_sheep


def create_dict_to_json_file(sheep_list, wolf, round_number):
    sheep_pos_list = []
    for sheep in sheep_list:
        if sheep.get_x() is not None:
            sheep_pos_list.append([sheep.get_x(), sheep.get_y()])
        else:
            sheep_pos_list.append(None)
    logging.debug("Function create_dict_to_json_file called and performed")
    return {"round_no": round_number, "wolf_pos": [wolf.get_x(), wolf.get_y()], "sheep_pos": sheep_pos_list}


def count_alive_sheep(sheep_list):
    num_of_alive = 0
    for sheep in sheep_list:
        if sheep.get_x() is not None:
            num_of_alive += 1
    logging.debug(f"Function count_alive_sheep called and performed. Number of alive sheep {num_of_alive}")
    return num_of_alive


def run_simulation(sheep_move, wolf_move, max_round, sheep_list, wolf, wait, dir):
    logging.debug("Simulation started")
    list_of_dicts = []
    list_for_alive_csv = []
    for i in range(max_round):
        logging.info("Round nr: " + str(i))
        count = 0
        for sheep in sheep_list:
            if sheep.coordinates[0] is not None:
                sheep.move(sheep_move)
                count += 1

        logging.info(f"There is {count} sheep left")

        if count == 0:
            print(f"Number of round: {i}")
            print(f"Current wolf position is: {round(wolf.get_x(), 3)} {round(wolf.get_y(), 3)}")
            print(f"There is {count} sheep left")
            list_of_dicts.append(create_dict_to_json_file(sheep_list, wolf, i))
            print("<<<===>>> Wolf has eaten all sheep <<<===>>>")
            break
        wolf.try_to_eat_sheep(sheep_list, wolf_move)
        print(f"Number of round: {i}")
        print(f"Current wolf position is: {round(wolf.get_x(), 3)} {round(wolf.get_y(), 3)}")
        print(f"There is {count} sheep left")

        list_of_dicts.append(create_dict_to_json_file(sheep_list, wolf, i))
        list_for_alive_csv.append([i, count_alive_sheep(sheep_list)])
        if wait:
            input("Press any key to continue...")
        print("")

    if dir:
        higher_dirs = os.getcwd()
        path = higher_dirs + '\\' + dir
        if not os.path.exists(path):
            print("Creating output directory")
            os.mkdir(dir)
        os.chdir(dir)
        with open("pos.json", "w") as f:
            json.dump(list_of_dicts, f, indent=4)
        logging.info("Creating json file")
        with open("alive.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(list_for_alive_csv)
        logging.info("Creating csv file")
    else:
        with open("pos.json", "w") as f:
            json.dump(list_of_dicts, f, indent=4)
        logging.info("Creating json file")
        with open("alive.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(list_for_alive_csv)
        logging.info("Creating csv file")


def positive_check(value):
    intvalue = int(value)
    if intvalue <= 0:
        raise argparse.ArgumentTypeError("%svalue must be positive" % value)
    logging.debug("check_positive(", value, ") called, got ", intvalue)


def config_parser(file):
    config = ConfigParser()
    config.read(file)
    init_config = config.get('Terrain', 'InitPosLimit')
    sheep_config = config.get('Movement', 'SheepMoveDist')
    wolf_config = config.get('Movement', 'WolfMoveDist')
    if float(init_config) < 0 or float(sheep_config) < 0 or float(wolf_config) < 0:
        logging.error("At least one of passed arguments is an negative number")
        raise ValueError("Negative number")
    logging.debug(f"""Function config_parser called and performed. Config is applied
                    init_pos_limit = {float(init_config)}
                    sheep_move_dist = {float(sheep_config)}
                    wolf_move_dist = {float(wolf_config)} """)
    return float(init_config), float(sheep_config), float(wolf_config)


if __name__ == "__main__":
    init_pos_limit = 10.0
    sheep_move_dist = 0.5
    wolf_move_dist = 1.0
    flock_of_sheep_size = 15
    max_rounds = 50
    directory = None
    wait = False

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help="Set path to config file", action='store',
                        dest='conf_file', metavar='FILE')
    parser.add_argument('-d', '--dir', help="Set directory for output files", action='store',
                        dest='directory', metavar='DIR')
    parser.add_argument('-l', '--log', help="Create log file with set log LEVEL", action='store',
                        dest='log_lvl', metavar='LEVEL')
    parser.add_argument('-r', '--rounds', help="State how many rounds should be played", action='store',
                        dest='round_no', type=positive_check, metavar='NUM')
    parser.add_argument('-s', '--sheep', help="State how many sheeps should be spawned", action='store',
                        dest='sheep_no', type=positive_check, metavar='NUM')
    parser.add_argument('-w', '--wait', help="Wait for input after each round", action='store_true')

    args = parser.parse_args()
    if args.conf_file:
        init_pos_limit, sheep_move_dist, wolf_move_dist = config_parser(args.conf_file)
    if args.directory:
        directory = args.directory
    if args.log_lvl:
        if args.log_lvl == "DEBUG":
            lvl = logging.DEBUG
        elif args.log_lvl == "INFO":
            lvl = logging.INFO
        elif args.log_lvl == "WARNING":
            lvl = logging.WARNING
        elif args.log_lvl == "ERROR":
            lvl = logging.ERROR
        elif args.log_lvl == "CRITICAL":
            lvl = logging.CRITICAL
        else:
            raise ValueError("Invalid log level provided")

        if directory:
            higher_dirs = os.getcwd()
            path = higher_dirs + '\\' + directory
            if not os.path.exists(path):
                print("Creating output directory")
                os.mkdir(directory)
            os.chdir(directory)
            logging.basicConfig(level=lvl, filename="chase.log", force=True)
            os.chdir("..")
        logging.debug("debug")
    if args.round_no:
        round_no = args.round_no
    if args.sheep_no:
        sheep_no = args.sheep_no
    if args.wait:
        wait = args.wait

    sheep = create_sheep_flock(flock_of_sheep_size, init_pos_limit)

    wolf = Wolf(0, 0)

    run_simulation(sheep_move_dist, wolf_move_dist, max_rounds, sheep, wolf, wait, directory)
