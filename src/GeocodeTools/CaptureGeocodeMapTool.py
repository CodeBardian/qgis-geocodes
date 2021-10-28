from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, Qgis
from qgis.utils import iface

from GeocodeTools.openlocationcode import encode
from GeocodeTools.osm_shortlink import short_osm
from GeocodeTools.utils import GeocodeType, toGeocode


class CaptureGeocodeMapTool(QgsMapToolEmitPoint):
    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    def __init__(self, canvas):
        QgsMapToolEmitPoint.__init__(self, canvas)

        self.canvas = canvas
        self.geocode_type = None
        self.cursor = Qt.CrossCursor

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def canvasReleaseEvent(self, event):
        pt = self.toMapCoordinates(event.pos())
        code = self.transformToGeocode(pt)

        iface.messageBar().pushMessage("Geocode Tools", f"The Geocode: {code} has been copied to the clipboard",
                                       level=Qgis.Info, duration=6)
        clipboard = QApplication.clipboard()
        clipboard.setText(code)

    def transformToGeocode(self, pt):
        canvas_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvas_crs, self.epsg4326, QgsProject.instance())
        pt4326 = transform.transform(pt.x(), pt.y())

        return toGeocode(pt4326, self.geocode_type)
