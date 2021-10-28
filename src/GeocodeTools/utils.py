from enum import Enum

from GeocodeTools.openlocationcode import encode
from GeocodeTools.osm_shortlink import short_osm


class GeocodeType(Enum):
    OpenLocationCode = 'pluscode'
    OSMShortLink = 'shortlink'


def toGeocode(pt, code_type):
    if code_type == GeocodeType.OpenLocationCode:
        code = encode(pt.y(), pt.x())
    elif code_type == GeocodeType.OSMShortLink:
        code = short_osm(pt.y(), pt.x())
    else:
        raise Exception('unknown geocode type')

    return code
