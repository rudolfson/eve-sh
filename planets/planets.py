import requests
from auth import esi_auth

URL = 'https://esi.tech.ccp.is/latest'


@esi_auth.authenticated(scopes=['esi-planets.manage_planets.v1'])
def extract(character_id, period="1", request_headers=None):
    """Find extractors depleting in the given period

    :param character_id: the id of the character
    :param period: period of time
    :param request_headers: additional request headers to use
    """
    planets = _planets(character_id, request_headers=request_headers)
    for planet in planets:
        planet_info = _planet(planet['planet_id'])
        colony = _colony(character_id, planet['planet_id'], request_headers)
        print(f'TRACE {planet_info}')
        print(f'TRACE {colony}')

    return planets


def _planets(character_id, request_headers=None):
    """Read all planets of a character

    :param character_id: the id of the character
    :param request_headers: additional request headers to use
    """
    response = requests.get(f'{URL}/characters/{character_id}/planets/', headers=request_headers)
    response.raise_for_status()
    return response.json()


def _planet(planet_id):
    """Read the public planet information

    :param planet_id: the if of the planet to get the info for"""
    response = requests.get(f'{URL}/universe/planets/{planet_id}/')
    response.raise_for_status()
    return response.json()


def _colony(character_id, planet_id, request_headers):
    """Get information about a character's colony on a planet

    :param character_id: id of the character
    :param planet_id: id of the planet where the colony is located"""
    response = requests.get(f'{URL}/characters/{character_id}/planets/{planet_id}/', headers=request_headers)
    response.raise_for_status()
    return response.json()
