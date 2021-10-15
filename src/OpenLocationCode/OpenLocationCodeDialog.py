import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QCursor

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.gui import QgsVertexMarker, QgsDockWidget

from .openlocationcode import decode


class OpenLocationCodeDialog(QgsDockWidget):
    def __init__(self, canvas, parent):
        super(OpenLocationCodeDialog, self).__init__(parent)

        self.canvas = canvas
        self.marker = None

        self.widget = uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui/dialog.ui'))
        self.setWidget(self.widget)

        self.widget.textBox.returnPressed.connect(self.zoomToOLC)

    def zoomToOLC(self):
        try:
            olc = str(self.widget.textBox.text()).replace(" ", "")
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            code_area = decode(olc)
            canvas_crs = self.canvas.mapSettings().destinationCrs()
            epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            transform4326 = QgsCoordinateTransform(epsg4326, canvas_crs, QgsProject.instance())
            center = transform4326.transform(code_area.longitudeCenter, code_area.latitudeCenter)
            self.canvas.zoomByFactor(1, center)
            self.canvas.refresh()
            if self.marker is None:
                self.marker = QgsVertexMarker(self.canvas)
            self.marker.setCenter(center)
            self.marker.setIconSize(8)
            self.marker.setPenWidth(4)
            self.widget.textBox.setStyleSheet("QLineEdit{background: white}")
        except Exception as e:
            self.widget.textBox.setStyleSheet("QLineEdit{background: yellow}")
        finally:
            QApplication.restoreOverrideCursor()

    def removeMarker(self):
        self.canvas.scene().removeItem(self.marker)
        self.marker = None

    def closeEvent(self, evt):
        if self.marker is not None:
            self.removeMarker()
