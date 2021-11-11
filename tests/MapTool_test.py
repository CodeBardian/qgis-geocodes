import pytest
from qgis.utils import iface
from qgis.core import QgsPointXY

from GeocodeTools.CaptureGeocodeMapTool import CaptureGeocodeMapTool
from GeocodeTools.utils import GeocodeType


@pytest.fixture()
def capture_tool():
    return CaptureGeocodeMapTool(iface.mapCanvas())


class TestCaptureGeocodeMapTool:

    def test_transform(self, capture_tool):
        capture_tool.geocode_type = GeocodeType.OpenLocationCode
        point = QgsPointXY(26.7205625, 58.3766875)

        code = capture_tool.transformToGeocode(point)

        assert code == '9GC89PGC+M6'