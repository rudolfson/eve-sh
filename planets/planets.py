import requests
from auth import esi_auth

URL = 'https://esi.tech.ccp.is/latest/'


@esi_auth.authenticated(scopes=['esi-planets.manage_planets.v1'])
def extract(character_id, period="1"):
    """Find extractors depleting in the given period

    :param character_id: the id of the character
    :param period: period of time"""
    return __planets(character_id)


def __planets(character_id):
    """Read all planets of a character

    :param character_id: the id of the character
    """
    return 'yeehah! planets!'
