from qgis.core import QgsProcessingProvider

from GeocodeTools.processing.EncodeAlgorithm import EncodeAlgorithm


class GeocodeProcessingProvider(QgsProcessingProvider):

    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(EncodeAlgorithm())

    def id(self, *args, **kwargs):
        return 'qgisgeocodes'

    def name(self, *args, **kwargs):
        return self.tr('Geocode Tools')

    def icon(self):
        return QgsProcessingProvider.icon(self)