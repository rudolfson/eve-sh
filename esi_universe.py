import esi


def names(ids):
    """Get the names of the given items"""
    op = esi.app.op['post_universe_names'](ids=ids)
    response = esi.client.request(op)
    return response.data
