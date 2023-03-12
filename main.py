import requests
import pprint
import json

armies_url = 'https://webapp.onepagerules.com/api/army-books'

def get_army(name):
    armies_response = requests.get(armies_url).json()
    armies_ids_names = [dict(uid = army['uid'], name = army['name']) for army in armies_response]
    selected_army_id = (list (filter (lambda a: a['name'] == name, armies_ids_names)))[0]['uid']
    json_object = json.dumps(army_response, indent=4)

    with open(name + ".json", "w") as outfile:
        outfile.write(json_object)

    return requests.get(armies_url + '/' + selected_army_id).json()

# def string_attribute(data, attribute):
#     str(data + ': ' + unit[attribute])

def print_equipment(unit):
    equipment_string = ''
    for e in unit['equipment']:
        equipment_string = equipment_string + e['name'] + ' attacks ' + str(e['attacks']) + ' '
    return equipment_string

def print_upgrades(unit):
    upgrade_string = ''
    for u in unit['upgrades']:
        for s in u['sections']:
            if s.get('type') == 'replace':
                for o in s['options']:
                    print(s.get('replaceWhat'))
                    pprint.pprint(o['gains'])

    return upgrade_string

def replace_equipment(equipment, replacement):
    pass


def generate_all_units(unit):
    upgrade_sections = [u['sections'] for u in unit['upgrades']]
    replacements = []
    for s in upgrade_sections:
        replace = list(filter (lambda s: s.get('type') == 'replace', s))
        if replace != []:
            replacements.append(replace[0])
        #replacements = list(filter (lambda s: s.get('type') == 'replace', upgrade_sections))
    new_equipment = []

    return replacements


def print_unit(unit):
    unit_string = 'name: '+ unit['name'] + ' defense: ' + str(unit['defense']) + ' quality: '+ str(unit['quality']) + ' equipment: '+ print_equipment(unit) + ' upgrades: '+ print_upgrades(unit)
    #unit_string = print_upgrades(unit)
    print(unit_string)


def find_upgrade(upgrades, upgrade_id):
    return next (filter (lambda a: a['uid'] == upgrade_id, upgrades))

#get_army('Human Defense Force')

with open('Human Defense Force.json', 'r') as openfile:
    army = json.load(openfile)

units = []
upgrades = []

for root in army:
    print(root)

for unit in army['units']:
    units.append(unit)

#print(units[0])

for upgrade in army['upgradePackages']:
    upgrades.append(upgrade)

#print(upgrades[0])

for unit in units:
    unit.update({'upgrades': [find_upgrade(upgrades, u) for u in unit['upgrades']]})

# pprint.pprint(units[0])
print_unit(units[0])


# units
generate_all_units(units[0])
