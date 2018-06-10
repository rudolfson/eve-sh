import datetime
import functools
import os
import pickle
import random
import string

import cherrypy
import click
import esipy

# On loading the module initialize the ESI Swagger App, Client and Security
if os.path.isfile('app.pickle'):
    with open('app.pickle', 'rb') as f:
        app = pickle.load(f)
else:
    app = esipy.App.create(url='https://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility')
    with open('app.pickle', 'wb') as f:
        pickle.dump(app, f)
security = esipy.EsiSecurity(app=app, redirect_uri='http://localhost:7070/callback',
                             client_id='ca73ab1ab8a949518d8e9d35ea46d2d2',
                             secret_key='crLG9e6cQ7rYlDxgVZKEfH0yw2x3VFkUBPdy2MYb',
                             headers={'User-Agent': 'EVE CLI by Leonty Alkaev'})
client = esipy.EsiClient(security=security, headers={'User-Agent': 'EVE CLI by Leonty Alkaev'})

# Configure the callback server
# TODO switch to flask again and use the shutdown function, see http://flask.pocoo.org/snippets/67/
cherrypy.log.screen = None
cherrypy.log.logger_root = None
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
            browser_url = security.get_auth_uri(scopes, state=state)
            # prepare embedded http server for callback
            authenticator = Authenticator()
            cherrypy.tree.mount(authenticator, '/', config={'/': {}})
            cherrypy.engine.subscribe('after_request', lambda: cherrypy.engine.exit())
            cherrypy.engine.start()
            # open the browser url
            click.launch(browser_url)
            # wait until a request has been handled - currently this only handles one request and exits
            cherrypy.engine.wait(cherrypy.engine.states.EXITING)
            cherrypy.server.stop()

            security.auth(authenticator.code)

            # do the actual call
            result = func(*args, **kwargs)

            return result

        return wrapper

    return authenticated_decorator
