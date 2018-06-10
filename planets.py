import esi
import collections
import roman
import datetime


@esi.authenticated(scopes=['esi-planets.manage_planets.v1'])
def extract(days=1, hours=0):
    """Find extractors depleting in the given days and hours

    :param days: days in which extractors deplete
    :param hours: hours in which extractors deplete
    """
    character_info = esi.security.verify()
    character_id = character_info['CharacterID']
    planets = _planets(character_id)
    now = datetime.datetime.now(datetime.timezone.utc)
    deplete_in = datetime.timedelta(days=days, seconds=hours * 3600)
    result = {}
    for planet in planets:
        planet_info = _planet(planet['planet_id'])
        colony = _colony(character_id, planet['planet_id'])
        extractors = map(_create_expiry_info(now, deplete_in), filter(lambda pin: 'expiry_time' in pin, colony['pins']))
        result[planet_info['name']] = list(extractors)

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


def _create_expiry_info(now, deplete_in):
    def expiry_info(pin):
        expiry_time = pin['expiry_time'].v - now
        depleted = expiry_time.total_seconds() < 0
        info = {'is_depleted': depleted, 'will_deplete': (expiry_time < deplete_in)}
        if not depleted:
            info['expires_in'] = f'{expiry_time.days:2} days {expiry_time.seconds // 3600:2} hours'
        return info

    return expiry_info
