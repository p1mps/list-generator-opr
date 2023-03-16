import json

from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse


def replace_equipment(equipment, gains, select, replaceWhat):
    equipments = []

    for g in gains:
        while select > 0:
            equipment_copy = equipment.copy()
            for s in range(0, select):
                g.update({'upgrade': True, 'replaceWhat': replaceWhat})
                equipment_copy.append(g)
            select = select -1
            equipments.append(equipment_copy)

    return equipments

def combine_unit(unit):
    new_unit = unit
    new_unit['size'] = unit['size'] * 2
    new_unit['cost'] = unit['cost'] * 2
    return new_unit

def calculate_cost(unit):
    pass

def parse_equipment(unit, replacements):
    equipment = unit['equipment']
    new_equipments = []

    print("=========================")
    print(unit.get('name'))
    for e in equipment:
        for r in replacements:
            print(e.get('name'))
            for o in r.get('options'):
                print("------------------------------")
                for g in o.get('gains'):
                    print(g.get('name'))
                print("------------------------------")
                if isinstance(r, dict) and isinstance(e, dict) and e.get('name', 1) == r.get('replaceWhat', 2):
                    for o in r['options']:
                        new_equipments.append(replace_equipment(equipment, o['gains'],r.get('select', 1),r['replaceWhat']))
        if e.get('replaceWhat') == None:
            new_equipments.append([equipment])

    return new_equipments


def get_replacements(unit):
    upgrade_sections = [u['sections'] for u in unit['upgrades']]
    replacements = []

    for s in upgrade_sections:
        replace = list(filter (lambda s: s.get('type') == 'replace', s))
        if replace != []:
            replacements.append(replace[0])

    return replacements

def generate_all_units(unit):

    replacements = get_replacements(unit)
    new_equipments = parse_equipment(unit, replacements)

    for equipment in new_equipments:
        for weapons in equipment:
            upgrades = list(filter (lambda s: s.get('upgrade') == True, weapons))
            upgrade_names = [u['name'] for u in upgrades]
            for w in weapons:
                upgrades_count = len(list(filter (lambda s: s.get('replaceWhat') == w.get('name'), weapons)))
                size = unit['size'] - upgrades_count

                if w.get('upgrade') == True:
                    size = 1

                w['size'] = size

                #print(w['name'] + ' ' +  str(w['size']))
    new_unit = unit
    new_unit['equipment'] = new_equipments

    return new_unit



def find_upgrade(upgrades, upgrade_id):
    return next (filter (lambda a: a['uid'] == upgrade_id, upgrades))


import pprint


def parse_army(army):
    units = []
    upgrades = []
    for unit in army['units']:
        units.append(unit)

    for upgrade in army['upgradePackages']:
        upgrades.append(upgrade)

    for unit in units:
        print (unit ['name'])
        unit_upgrades = [find_upgrade(upgrades, u) for u in unit['upgrades']]

        upgrades = []
        for u in unit_upgrades:
            for s in u ['sections']:
                for o in s.get ('options'):
                    upgrades.apped ({'gains': o.get ('gains')})
            print (upgrades)
        for e in unit['equipment']:
            equipment_upgrade = list ((filter (lambda a: a.get ('replaceWhat') == e ['name'], unit_upgrades)))
            print(equipment_upgrade)
            print("-------")

    all_units = []

    # for unit in army['units']:
    #     all_units.append(generate_all_units(unit))

    return units




with open("Human Defense Force.json", 'r') as json_file:
    json_data = json.load(json_file)
    units = parse('units[*]').find(json_data)
    equipments = parse('units[*].equipment').find(json_data)

    data = dict ()
    for idx,unit in enumerate(units):
        unit_upgrades = unit.value['upgrades']

        gains = []
        print('Unit: ' + unit.value['name'])
        for u in unit_upgrades:
            upgrades = parse(f"upgradePackages[?(@.uid == '{u}')]").find(json_data)
            for s in upgrades [0].value ['sections']:
                for o in s ['options']:
                    for g in o ['gains']:
                        if g ['type'] == 'ArmyBookWeapon':
                            print (g ['name'] + ' ' + 'replace: ' + str (s.get ('replaceWhat')) + ' '+  g ['type'])
                            gains.append ({'replacement': s.get ('replaceWhat'), 'gain': g})
            data.update ({unit.value ['name']: {'gains':gains, 'equipment': unit.value ['equipment']}})


for unit in data.keys ():
    print (data [unit] ['equipment'])













