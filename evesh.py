from email import header

import click
import esi
import evepraisal
import planets


@click.group()
def cli():
    """Command line tool for querying things from EVE Online. Use appropriate commands."""
    pass


@cli.command()
def status():
    """display current server status"""
    op = esi.app.op['get_status']()
    response = esi.client.request(op)
    if 'players' in response.data:
        click.secho('Server is {} with {} players'.format(click.style('running', fg='green'),
                                                          click.style(str(response.data['players']), fg='blue')))


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
@click.argument('days', default=1)
@click.argument('hours', default=0)
def extract(days, hours):
    """report extractors depleting in DAYS and HOURS from now"""
    result = planets.extract(days=days, hours=hours)
    click.secho(
        'Planets of {0}, expiry in {1} days {2} hours'.format(result['character_name'], days,
                                                              hours))
    for planet, extractors in result['planets'].items():
        extractor_display = list(map(_style_extractor_info, extractors))
        click.secho('{0:<20} {1}\n            {2}'.format(click.style(planet, fg='white'), extractor_display[0],
                                                          extractor_display[1]))


def _style_extractor_info(info):
    """use clicks styling to create a representation for the extractor info

    :param info: extractor info
    """
    if info['is_depleted']:
        return click.style('depleted', fg='white', bg='red')
    if info['will_deplete']:
        return click.style(info['expires_in'], fg='red')
    return click.style(info['expires_in'], fg='green')
