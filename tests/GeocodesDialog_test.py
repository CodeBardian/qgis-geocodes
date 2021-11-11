import pytest
from qgis.utils import iface
from qgis.core import QgsPointXY
from qgis.gui import QgsVertexMarker

from GeocodeTools.GeocodesDialog import GeocodesDialog


@pytest.fixture()
def dialog():
    return GeocodesDialog(iface.mapCanvas(), iface.mainWindow())


class TestGeocodesDialog:

    def test_zoom_no_input(self, dialog):
        dialog.zoomTo()

        assert dialog.widget.textBox.styleSheet() == 'QLineEdit{background: yellow}'

    def test_zoom(self, dialog):
        dialog.widget.textBox.setText('9GC89PGC+M6')
        dialog.zoomTo()

        assert dialog.widget.textBox.styleSheet() == 'QLineEdit{background: white}'
        assert dialog.marker.center() == QgsPointXY(26.7205625, 58.3766875)

    def test_removeMarker(self, dialog):
        dialog.marker = QgsVertexMarker(iface.mapCanvas())

        dialog.removeMarker()

        assert dialog.marker is None
