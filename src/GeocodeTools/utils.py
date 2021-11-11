from enum import Enum

from GeocodeTools.encoding.openlocationcode import encode, decode
from GeocodeTools.encoding.osm_shortlink import short_osm, _decode
from GeocodeTools.encoding import geohash


class GeocodeType(Enum):
    OpenLocationCode = 'pluscode'
    OSMShortLink = 'shortlink'
    Geohash = 'geohash'


def toGeocode(pt, code_type):
    if code_type == GeocodeType.OpenLocationCode:
        code = encode(pt.y(), pt.x())
    elif code_type == GeocodeType.OSMShortLink:
        code = short_osm(pt.y(), pt.x())
    elif code_type == GeocodeType.Geohash:
        code = geohash.encode(pt.y(), pt.x())
    else:
        raise Exception('unknown geocode type')

    return code


def toPosition(code):
    if not code:
        raise Exception('invalid geocode')
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

    try:
        lat, lon = geohash.decode(code)
        return lat, lon
    except:
        pass

    raise Exception('invalid geocode')
