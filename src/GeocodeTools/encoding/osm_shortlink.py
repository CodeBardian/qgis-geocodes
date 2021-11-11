# adapted from osm_shortlink.py - MAximillian Dornseif 2013 - Public Domain
# https://gist.github.com/mdornseif/5652824
# and short_link.rb https://github.com/openstreetmap/openstreetmap-website/blob/master/lib/short_link.rb

import math

ARRAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_~'


def short_osm(lat, lon, zoom=19):
    """Return a short link representing a location in OpenStreetmap.

    Provide coordinates and optional zoom level. e.g.:

    >>> short_osm(50.671530961990356, 6.09715461730957, 16)
    'https://osm.org/go/0GAjIv8h'
    >>> short_osm(0, 0, 3)
    'https://osm.org/go/wAAA--'
    >>> short_osm(0, 0, 4)
    'https://osm.org/go/wAAA'
    """
    return 'https://osm.org/go/' + _encode(lat, lon, zoom)


def _decode(short_link):
    """Returns latitude longitude and zoom level of given osm short link
    >>> _decode('https://osm.org/go/wAAA--')
    (0.0, 0.0, 3)
    >>> _decode('https://osm.org/go/wAAA')
    (0.0, 0.0, 4)
    >>> _decode('https://osm.org/go/0MZL7BaZ')
    ()
    """
    code = short_link.split('https://osm.org/go/')[1]
    x, y, z, z_offset = 0, 0, 0, 0

    for char in code:
        digit = ARRAY.find(char)
        if digit == -1:
            z_offset -= 1
            continue

        for i in range(3):
            x <<= 1
            if digit & 32 != 0:
                x |= 1
            digit <<= 1

            y <<= 1
            if digit & 32 != 0:
                y |= 1
            digit <<= 1
        z += 3

    x <<= (32 - z)
    y <<= (32 - z)

    x = (x * 360.0 / 2**32) - 180.0
    y = (y * 180.0 / 2**32) - 90.0
    z = z - 8 - (z_offset % 3)

    return x, y, z


def _encode(lat, lon, z):
    """given a location and zoom, return a short string representing it."""
    x = int((lon + 180.0) * 2**32 / 360.0)
    y = int((lat + 90.0) * 2**32 / 180.0)
    code = _interleave(x, y)
    s = ''
    # add eight to the zoom level, which approximates an accuracy of
    # one pixel in a tile.
    for i in range(int(math.ceil((z + 8) / 3.0))):
        digit = (code >> (58 - 6 * i)) & 0x3f
        s += ARRAY[digit]
    # append characters onto the end of the string to represent
    # partial zoom levels (characters themselves have a granularity
    # of 3 zoom levels).
    for i in range((z + 8) % 3):
        s += "-"
    return s


def _interleave(x, y):
    """combine 2 32 bit integers to a 64 bit integer"""
    c = 0
    for i in range(31, -1, -1):
        c = (c << 1) | ((x >> i) & 1)
        c = (c << 1) | ((y >> i) & 1)
    return c
