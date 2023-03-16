def print_unit(unit):
    print(unit['name'] + ' defense: ' + str(unit['defense']) + ' quality: '+ str(unit['quality']))
    weapons_all = [[]]
    for equipment in unit['equipment']:
        print(equipment)
        print(unit['upgrades'])

    #unit_string = print_upgrades(unit)

