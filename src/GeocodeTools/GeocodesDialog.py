import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QApplication, QLineEdit
from qgis.PyQt.QtGui import QCursor, QIcon

from qgis.core import QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject
from qgis.gui import QgsVertexMarker, QgsDockWidget

from .utils import toPosition


class GeocodesDialog(QgsDockWidget):
    def __init__(self, canvas, parent):
        super(GeocodesDialog, self).__init__(parent)

        self.canvas = canvas
        self.marker = None
        self.setWindowTitle('Geocode Tools')

        self.widget = uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui/dialog.ui'))
        self.setWidget(self.widget)
        self.widget.bZoom.setIcon(QIcon(':/images/themes/default/mActionZoomIn.svg'))
        self.widget.bZoom.clicked.connect(self.zoomTo)
        self.widget.bClearMarker.setIcon(QIcon(':/images/themes/default/mActionRemove.svg'))
        self.widget.bClearMarker.clicked.connect(self.removeMarker)

        self.widget.textBox.setClearButtonEnabled(True)
        self.widget.textBox.addAction(QIcon(":/images/themes/default/search.svg"), QLineEdit.LeadingPosition)
        self.widget.textBox.returnPressed.connect(self.zoomTo)

    def zoomTo(self):
        try:
            code = str(self.widget.textBox.text()).replace(" ", "")
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            lat, lon = toPosition(code)

            canvas_crs = self.canvas.mapSettings().destinationCrs()
            epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")
            transform4326 = QgsCoordinateTransform(epsg4326, canvas_crs, QgsProject.instance())
            center = transform4326.transform(lon, lat)
            self.canvas.zoomByFactor(1, center)
            self.canvas.refresh()
            if self.marker is None:
                self.marker = QgsVertexMarker(self.canvas)
            self.marker.setCenter(center)
            self.marker.setIconSize(8)
            self.marker.setPenWidth(4)
            self.widget.textBox.setStyleSheet("QLineEdit{background: white}")

        except:
            self.widget.textBox.setStyleSheet("QLineEdit{background: yellow}")
        finally:
            QApplication.restoreOverrideCursor()


    def removeMarker(self):
        if self.marker is not None:
            self.canvas.scene().removeItem(self.marker)
            self.marker = None

    def closeEvent(self, evt):
        self.removeMarker()
