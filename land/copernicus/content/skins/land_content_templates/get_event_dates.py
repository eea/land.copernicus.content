##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=brain=None, event=None
##title=format dates for an event

# extract dates from a brain representing an event
# return output: 28–29 October

import DateTime

if brain is not None:
    start = brain.start
    end = brain.end
else:
    if event.portal_type in ['Event', 'Folderish Event']:
        start = event.start()
        end = event.end()

    elif event.portal_type == 'eea.meeting':
        return event.human_readable_date

if not (start and end):
    return ""

start_day, start_month = start.day(), start.Month()
end_day, end_month = end.day(), end.Month()

if start_month == end_month:
    if start_day == end_day:
        return "%s %s" % (start_day, start_month)
    return "%s-%s %s" % (start_day, end_day, start_month)

return "%s %s - %s %s" % (start_day, start_month, end_day, end_month)
