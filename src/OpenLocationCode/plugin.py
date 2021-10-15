
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from OpenLocationCode.OpenLocationCodeDialog import OpenLocationCodeDialog


class OpenLocationCodePlugin:

    def __init__(self, iface):
        self.iface = iface

        self.menu = 'OpenLocationCode Tools'
        self.dockWidget = OpenLocationCodeDialog(self.iface.mapCanvas(), self.iface.mainWindow())

        self.first_start = None
        self.actions = []

    def initGui(self):
        zoomToIcon = QIcon(':/images/themes/default/mActionZoomIn.svg')
        zoomToAction = QAction(zoomToIcon, "Zoom to OpenLocationCode address", self.iface.mainWindow())
        zoomToAction.triggered.connect(self.showDialog)
        self.iface.addPluginToMenu(self.menu, zoomToAction)
        self.actions.append(zoomToAction)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.hide()

    def showDialog(self):
        self.dockWidget.show()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)

        self.iface.removeDockWidget(self.dockWidget)
