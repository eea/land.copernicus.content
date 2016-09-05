from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Widget import StringWidget

from AccessControl import ClassSecurityInfo


class GeographicBoundingBoxWidget(StringWidget):
    """ Based on StringWidget, saves the values from all 4 text inputs
        West    = -81.2549
        East    = -81.2549
        North   = -81.2549
        South   = -81.2549
    """
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'geographic_bounding_box_widget',
    })

    security = ClassSecurityInfo()

    security.declarePublic('render_own_label')

    def render_own_label(self):
        return True


registerWidget(
    GeographicBoundingBoxWidget,
    title='Geographic Bounding Box Widget',
    description='GeographicBoundingBoxWidget uses 4 inputs '
                '(West, East, North, South)',
    used_for=('land.copernicus.content.fields.'
              'geographic_bounding_box.GeographicBoundingBoxWidget',)
)
