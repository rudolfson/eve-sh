import functools
import requests

URL = 'https://login.eveonline.com/oauth/'


def authenticated(scopes):
    def authenticated_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            browser_params = dict(response_type='code', redirect_url='http://localhost:7070/callback', client_id='asd',
                                  scope=' '.join(scopes), state='evesh')
            browser_url = requests.Request('GET', URL + 'authorize', params=browser_params).prepare().url
            print('TRACE opening ' + browser_url)

            result = func(*args, **kwargs)
            return result

        return wrapper

    return authenticated_decorator
