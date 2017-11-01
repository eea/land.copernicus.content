""" Content rules handler
"""
from plone.app.contentrules.handlers import execute


def execute_event(event):
    """ Execute custom rules
    """
    execute(event.object, event)
