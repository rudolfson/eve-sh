import esi
import collections
import roman


@esi.authenticated(scopes=['esi-planets.manage_planets.v1'])
def extract(period='1'):
    """Find extractors depleting in the given period

    :param period: period of time
    """
    character_info = esi.security.verify()
    character_id = character_info['CharacterID']
    planets = _planets(character_id)
    result = {}
    for planet in planets:
        planet_info = _planet(planet['planet_id'])
        colony = _colony(character_id, planet['planet_id'])
        result[planet_info['name']] = len(colony['pins'])

    result = collections.OrderedDict(sorted(result.items(), key=lambda item: roman.fromRoman(item[0].split()[1])))
    return result


def _planets(character_id):
    """Read all planets of a character

    :param character_id: the id of the character
    """
    op = esi.app.op['get_characters_character_id_planets'](character_id=character_id)
    response = esi.client.request(op)
    return response.data


def _planet(planet_id):
    """Read the public planet information

    :param planet_id: the if of the planet to get the info for"""
    op = esi.app.op['get_universe_planets_planet_id'](planet_id=planet_id)
    return esi.client.request(op).data


def _colony(character_id, planet_id):
    """Get information about a character's colony on a planet

    :param character_id: id of the character
    :param planet_id: id of the planet where the colony is located"""
    op = esi.app.op['get_characters_character_id_planets_planet_id'](character_id=character_id, planet_id=planet_id)
    return esi.client.request(op).data
