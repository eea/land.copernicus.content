##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=brain=None,event=None
##title=Retrieves the year from an brain representing an event

# retrieves the year from an brain representing an event

import DateTime

if brain is not None:
    start = brain.start
else:
    if event.portal_type in ['Event', 'Folderish Event']:
        start = event.start()

    elif event.portal_type == 'eea.meeting':
        start = DateTime.DateTime(event.start)

    else:
        return ''

if start:
    return start.year()

return ""
