import argparse
import json
import os.path
from generator.parse import parse_army
from generator.http import get_army
from generator.print import print_unit

def save_army_json (army_name):
    army_file = './' + army_name + '.json'

    if os.path.isfile(army_file):
        with open(army_file, 'r', encoding='utf-8') as file:
            army = json.load(file)
    else:
        army = get_army(army_name)
        json_object = json.dumps(army, indent=4)
        with open(army_name + ".json", "w", encoding='utf-8') as file:
            file.write(json_object)
    return army


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='OPR list generator',
        description='Find best optimazed list for your army',
        epilog='')
    parser.add_argument('-a', '--army')
    args = parser.parse_args()
    army_json = save_army_json(args.army)
    all_units = parse_army(army_json)
    for unit in all_units:
        print_unit(unit)
