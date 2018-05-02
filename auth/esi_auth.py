"""Implementation of EVE SSO authentication.

To make use of authentication you need to decorate the according method with

    @authenticated(scope)

See https://eveonline-third-party-documentation.readthedocs.io/en/latest/sso/intro.html
for details upon EVE's authentication.
"""
import functools
import requests
import cherrypy
import datetime
import click
import string
import random

AUTH_URL = 'https://login.eveonline.com/oauth/'

cherrypy.config.update({'server.socket_port': 7070})
cherrypy.config.update({'server.shutdown_timeout': 1})
cherrypy.config.update({'engine.autoreload.on': False})


class Authenticator(object):
    """Provide a callback to the authentication request and store the provided authentication data.

    """

    def __init__(self):
        self.code = None
        self.state = None

    @cherrypy.expose
    def callback(self, state='unknown', code='unknown'):
        self.code = code
        self.state = state
        return f'Ok - received code {self.code} for state {self.state} at {datetime.datetime.now()}'


def authenticated(scopes):
    """Decorate a call to the ESI API to handle authentication

    The character's id after login will be available as a keyword argument "character_id".
    """

    def authenticated_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # prepare authentication url to open in browser
            state = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            browser_params = dict(response_type='code', redirect_uri='http://localhost:7070/callback',
                                  client_id='ca73ab1ab8a949518d8e9d35ea46d2d2',
                                  scope=' '.join(scopes), state=state)
            browser_url = requests.Request('GET', AUTH_URL + 'authorize', params=browser_params).prepare().url
            # prepare embedded http server for callback
            authenticator = Authenticator()
            cherrypy.tree.mount(authenticator, '')
            cherrypy.engine.subscribe('after_request', lambda: cherrypy.engine.exit())
            cherrypy.engine.start()
            # open the browser url
            click.launch(browser_url)
            # wait until a request has been handled - currently this only handles one request and exits
            cherrypy.engine.wait(cherrypy.engine.states.EXITING)
            cherrypy.server.stop()

            # now get the access token
            access_token = _get_access_token(authenticator.code)
            verification = _verify(access_token)
            kwargs['character_id'] = verification['CharacterID']
            authorization_header = _create_authorization_header(access_token)
            if 'request_headers' not in kwargs:
                kwargs['request_headers'] = {}
            kwargs['request_headers'] = {**kwargs['request_headers'], **authorization_header}

            # do the actual call
            result = func(*args, **kwargs)

            return result

        return wrapper

    return authenticated_decorator


def _get_access_token(authorization_code):
    """After authentication fetch an access token to do the actual API call"""

    data = {'grant_type': 'authorization_code', 'code': authorization_code}
    authentication = ('ca73ab1ab8a949518d8e9d35ea46d2d2', 'crLG9e6cQ7rYlDxgVZKEfH0yw2x3VFkUBPdy2MYb')
    response = requests.post(AUTH_URL + 'token', json=data, auth=authentication)
    response.raise_for_status()
    return response.json()


def _verify(access_token):
    """Verify the fetched access_token"""

    headers = _create_authorization_header(access_token)
    response = requests.get(AUTH_URL + 'verify', headers=headers)
    response.raise_for_status()
    return response.json()


def _create_authorization_header(access_token):
    """Create a dictionary containing the Authorization header"""
    return {'Authorization': f"{access_token['token_type']} {access_token['access_token']}"}
