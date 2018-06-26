import esi
import esi_universe


@esi.authenticated(scopes=['esi-location.read_location.v1', 'esi-location.read_ship_type.v1'])
def location():
    """Get a character's location"""
    character_info = esi.security.verify()
    character_id = character_info['CharacterID']
    loc = _location(character_id)
    ship = _ship(character_id)
    names = esi_universe.names([loc['solar_system_id'], ship['ship_type_id']])

    return {
        'character_name': character_info['CharacterName'],
        'solar_system': next(name for name in names if name['id'] == loc['solar_system_id'])['name'],
        'ship': next(name for name in names if name['id'] == ship['ship_type_id'])['name'],
    }


def _location(character_id):
    """Read the character location

    :param character_id: the id of the character
    """
    op = esi.app.op['get_characters_character_id_location'](character_id=character_id)
    response = esi.client.request(op)
    return response.data


def _ship(character_id):
    """Read the character's current ship

    :param character_id: the id of the character
    """
    op = esi.app.op['get_characters_character_id_ship'](character_id=character_id)
    response = esi.client.request(op)
    return response.data
