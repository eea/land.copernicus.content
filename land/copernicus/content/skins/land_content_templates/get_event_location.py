##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=brain

if brain.Type == 'EEA Meeting':
    obj = brain.getObject()
    return obj.location
    return obj.absolute_url()

return brain.location
