def autofillFullname(context):
    """ Because we splitted user fullname in first_name and last_name on
        register, fullname was omited from schema. But we autofill this
        on register event.
    """
    plone_user = context.principal
    properties = plone_user._propertysheets.get('mutable_properties')
    first_name = properties.getProperty('first_name')
    last_name = properties.getProperty('last_name')
    auto_fullname = first_name + " " + last_name
    properties.setProperty(plone_user, 'fullname', auto_fullname)
    # [TODO] Fix first_name and last_name to have the real data in fields.
