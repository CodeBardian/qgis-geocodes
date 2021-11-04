from enum import Enum

from GeocodeTools.openlocationcode import encode, decode
from GeocodeTools.osm_shortlink import short_osm, _decode


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


def toPosition(code):
    try:
        code_area = decode(code)
        return code_area.latitudeCenter, code_area.longitudeCenter
    except:
        pass

    try:
        lat, lon, zoom = _decode(code)
        return lon, lat
    except:
        pass

    raise Exception('invalid geocode')
