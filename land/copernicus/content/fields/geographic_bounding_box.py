from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.interfaces.field import IField
from Products.Archetypes.Field import decode
from Products.Archetypes.Field import encode
from land.copernicus.content.widgets.geographic_bounding_box import (
    GeographicBoundingBoxWidget
)
from Products.Archetypes import config
from Products.Archetypes.Field import ObjectField


class IGeographicBoundingBoxField(IField):
    """ Marker interface for GeographicBoundingBoxField
    """


class GeographicBoundingBoxField(atapi.LinesField):
    """ Based on LinesField, saves the values from all 4 text inputs
        West    = -81.2549
        East    = -81.2549
        North   = -81.2549
        South   = -81.2549
    """

    _properties = atapi.Field._properties.copy()
    _properties.update({
        'type': 'geographic_bounding_box',
        'default': (),
        'widget': GeographicBoundingBoxWidget,
    })

    implements(IGeographicBoundingBoxField)

    security = ClassSecurityInfo()

    @security.private
    def set(self, instance, value, **kwargs):
        __traceback_info__ = value, type(value)
        if isinstance(value, basestring):
            value = value.split('\n')
        value = [decode(v.strip(), instance, **kwargs)
                 for v in value if v and v.strip()]
        if config.ZOPE_LINES_IS_TUPLE_TYPE:
            value = tuple(value)
        ObjectField.set(self, instance, value, **kwargs)

    @security.private
    def get(self, instance, **kwargs):
        try:
            value = ObjectField.get(self, instance, **kwargs) or ()
            data = [encode(v, instance, **kwargs) for v in value]
        except Exception:
            value = ()
            data = [encode(v, instance, **kwargs) for v in value]
        if config.ZOPE_LINES_IS_TUPLE_TYPE:
            return tuple(data)
        else:
            return data

    @security.private
    def getRaw(self, instance, **kwargs):
        try:
            return self.get(instance, **kwargs)
        except Exception:
            return ()
