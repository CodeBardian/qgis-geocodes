
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from GeocodeTools.CaptureGeocodeMapTool import CaptureGeocodeMapTool
from GeocodeTools.GeocodesDialog import GeocodesDialog

CODE_TYPES = {
    'olc': 'OpenLocationCode',
    'osm': 'OSM Short Link'
}


class GeocodeToolsPlugin:

    def __init__(self, iface):
        self.iface = iface

        self.menu = 'Geocode Tools'
        self.dockWidget = GeocodesDialog(self.iface.mapCanvas(), self.iface.mainWindow())

        self.first_start = None
        self.actions = []

        self.tool = CaptureGeocodeMapTool(self.iface.mapCanvas())

    def initGui(self):
        zoom_icon = QIcon(':/images/themes/default/mActionZoomIn.svg')
        zoom_action = QAction(zoom_icon, "Zoom to Geocode address", self.iface.mainWindow())
        zoom_action.triggered.connect(self.showDialog)
        self.iface.addPluginToMenu(self.menu, zoom_action)
        self.actions.append(zoom_action)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.hide()

        tool_icon = QIcon(':/images/themes/default/mActionIdentify.svg')
        for code_type in CODE_TYPES.keys():
            tool_action = QAction(tool_icon, f"Capture {CODE_TYPES[code_type]}", self.iface.mainWindow())
            tool_action.triggered.connect(lambda checked, c=code_type: self.setTool(c))
            self.iface.addPluginToMenu(self.menu, tool_action)
            self.actions.append(tool_action)

    def setTool(self, code_type):
        self.tool.geocode_type = code_type
        self.iface.mapCanvas().setMapTool(self.tool)

    def showDialog(self):
        self.dockWidget.show()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)

        self.iface.removeDockWidget(self.dockWidget)
