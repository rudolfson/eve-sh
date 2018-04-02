import functools
import requests
import cherrypy
import datetime
import click
import string
import random
import threading

URL = 'https://login.eveonline.com/oauth/'

cherrypy.config.update({'server.socket_port': 7070})
cherrypy.config.update({'server.shutdown_timeout': 1})
cherrypy.config.update({'engine.autoreload.on': False})


class Authenticator(object):
    def __init__(self):
        self.code = None
        self.state = None

    @cherrypy.expose
    def callback(self, state='unknown', code='unknown'):
        self.code = code
        self.state = state
        return f'Ok - received code {self.code} for state {self.state} at {datetime.datetime.now()}'


def authenticated(scopes):
    def authenticated_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # prepare authentication url to open in browser
            state = ''.join(random.sample(string.ascii_letters + string.digits, 40))
            browser_params = dict(response_type='code', redirect_uri='http://localhost:7070/callback',
                                  client_id='ca73ab1ab8a949518d8e9d35ea46d2d2',
                                  scope=' '.join(scopes), state=state)
            browser_url = requests.Request('GET', URL + 'authorize', params=browser_params).prepare().url
            # prepare embedded http server for callback
            authenticator = Authenticator()
            print(f'TRACE active threads = {threading.active_count()}')
            cherrypy.tree.mount(authenticator, '')
            cherrypy.engine.subscribe('after_request', lambda: cherrypy.engine.exit())
            cherrypy.engine.start()
            # open the browser url
            click.launch(browser_url)
            # wait until a request has been handled - currently this only handles one request and exits
            cherrypy.engine.wait(cherrypy.engine.states.EXITING)
            cherrypy.server.stop()

            result = func(*args, **kwargs)

            print(f'TRACE active threads = {threading.active_count()}')
            for t in threading.enumerate():
                print(f'TRACE thread {t}')
                if t is not threading.current_thread():
                    print(f'{t} is not the current one')

            return result

        return wrapper

    return authenticated_decorator
