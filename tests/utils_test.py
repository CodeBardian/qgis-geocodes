import pytest

from qgis.core import QgsPointXY
from GeocodeTools.utils import toGeocode, GeocodeType, toPosition


class TestUtils:

    @pytest.mark.parametrize('coords, code_type, expected',
                             [((58.3766875, 26.7205625), GeocodeType.OpenLocationCode, '9GC89PGC+M6'),
                              ((58.37796, 26.72685), GeocodeType.OSMShortLink, 'https://osm.org/go/0w8AFnqSL'),
                              ((58.37796, 26.72685), GeocodeType.Geohash, 'ud7h05muk8rz')])
    def test_toGeocode(self, coords, code_type, expected):
        point = QgsPointXY(coords[1], coords[0])
        code = toGeocode(point, code_type)

        assert code == expected

    @pytest.mark.parametrize('expected, code',
                             [((58.3766875, 26.7205625), '9GC89PGC+M6'),
                              ((58.37796, 26.72685), 'https://osm.org/go/0w8AFnqSL'),
                              ((58.37796, 26.72685), 'ud7h05muk8rz')])
    def test_toPosition(self, code, expected):
        position = toPosition(code)

        assert position[0] == pytest.approx(expected[0])
        assert position[1] == pytest.approx(expected[1])

    def test_toPosition_failing(self):
        with pytest.raises(Exception, match='invalid geocode'):
            position = toPosition('9PF8+CF')