from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication

from qgis.gui import QgsMapToolEmitPoint
from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject, Qgis

from GeocodeTools.openlocationcode import encode
from GeocodeTools.osm_shortlink import short_osm


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
        code = self.toGeocode(pt)

        self.iface.messageBar().pushMessage("Geocode Tools", f"The Geocode: {code} has been copied to the clipboard",
                                            level=Qgis.Info, duration=6)
        clipboard = QApplication.clipboard()
        clipboard.setText(code)

    def toGeocode(self, pt):
        canvas_crs = self.canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvas_crs, self.epsg4326, QgsProject.instance())
        pt4326 = transform.transform(pt.x(), pt.y())

        if self.geocode_type == 'olc':
            code = encode(pt4326.x(), pt4326.y())
        elif self.geocode_type == 'osm':
            code = short_osm(pt4326.x(), pt4326.y())
        else:
            raise Exception('unknown geocode type')

        return code
