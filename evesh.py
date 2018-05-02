import click
import requests
from market import evepraisal
from planets import planets

URL = 'https://esi.tech.ccp.is/latest/{0}?datasource=tranquility'


@click.group()
def cli():
    """Command line tool for querying things from EVE Online. Use appropriate commands."""
    pass


@cli.command()
def status():
    """display current server status"""
    response = requests.get(URL.format('status/'))
    data = response.json()
    if 'players' in data:
        click.secho('Server is {} with {} players'.format(click.style('running', fg='green'),
                                                          click.style(str(data['players']), fg='blue')))


@cli.group()
def market():
    """market related commands"""
    pass


@market.command()
@click.option('--persist', is_flag=True, help='create a persistent praisal for later referral')
@click.argument('items')
def value(persist, items):
    """estimate the value of ITEMS (comma separated list of full item names)"""
    values = evepraisal.value(items, persist=persist)
    click.secho('{0} buy: {1:>28}\n{0} sell: {2:>27}'.format(click.style(values['market'], fg='white'),
                                                             click.style('{:,.2f}'.format(values['buy']), fg='yellow'),
                                                             click.style('{:,.2f}'.format(values['sell']), fg='blue')))


@cli.group()
def pi():
    """planetary interaction related commands"""
    pass


@pi.command()
@click.argument('period', default='1')
def extract(period):
    """report extractors depleting in PERIOD from now"""
    click.echo(planets.extract(period=period))

