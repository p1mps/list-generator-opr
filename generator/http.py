import json
import requests

def get_army(name):
    armies_url = 'https://webapp.onepagerules.com/api/army-books'
    army_response = requests.get(armies_url, timeout=1000).json()

    armies_ids_names = [{'uid': army['uid'], 'name': army['name']}
                        for army in army_response]

    selected_army_id = list(filter(lambda a: a['name'] == name,
                                   armies_ids_names))[0]['uid']

    return requests.get(armies_url + '/' + selected_army_id,
                        timeout=1000).json()
