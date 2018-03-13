import requests
import re

URL_TEMPLATE = 'https://evepraisal.com/appraisal.json'


def value(items_str: str, market='jita', persist=False):
    """Estimate the value of the given list of items using evepraisal.com

    :param items_str: comma separated list of item names
    :param market: specify the market to use
    :param persist: persist this praisal for later referral
    """
    items_data = re.sub('\s*[,;|/]\s*', '\n', items_str)
    params = {'market': market, 'raw_textarea': items_data}
    if not persist:
        params['persist'] = 'no'
    response = requests.post(URL_TEMPLATE, params=params)
    response.raise_for_status()
    appraisal = response.json()['appraisal']
    return {'market': appraisal['market_name'].capitalize(), **appraisal['totals']}
