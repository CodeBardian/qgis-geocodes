import os.path

from qgis import processing
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsProcessing, QgsPointXY, QgsGeometry, QgsFeature

from GeocodeTools.processing.provider import GeocodeProcessingProvider


class TestDecodeAlgorithm:
    provider = None

    @classmethod
    def setup_class(self):
        self.provider = GeocodeProcessingProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def test_processing_algorithm_registered(self):
        assert "qgisgeocodes:decodetopoints" in [alg.id() for alg in QgsApplication.processingRegistry().algorithms()]

    def test_algorithm(self):
        expected = (58.3766875, 26.7205625)

        uri = f'file:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/test.csv")}'
        layer_csv = QgsVectorLayer(uri, 'test_layer', 'delimitedtext')
        QgsProject.instance().addMapLayer(layer_csv)

        layer = processing.run("qgisgeocodes:decodetopoints", {
            'INPUT': layer_csv,
            'INPUT_CRS': 'EPSG:4326',
            'CODE_FIELD': 'OpenLocationCode',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        })['OUTPUT']

        for feature in layer.getFeatures():
            assert feature.geometry().asPoint() == QgsPointXY(expected[1], expected[0])


class TestEncodeAlgorithm:
    provider = None

    @classmethod
    def setup_class(self):
        self.provider = GeocodeProcessingProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def test_processing_algorithm_registered(self):
        assert "qgisgeocodes:encodetofield" in [alg.id() for alg in QgsApplication.processingRegistry().algorithms()]

    def test_algorithm(self):
        expected = 'ud7h05muk8rz'
        geom = QgsGeometry.fromPointXY(QgsPointXY(26.72685, 58.37796))

        layer = QgsVectorLayer(f"Point?crs=EPSG:4326", 'test', "memory")
        dp = layer.dataProvider()
        layer.startEditing()
        feat = QgsFeature()
        feat.setGeometry(geom)
        dp.addFeatures([feat])
        layer.commitChanges()

        QgsProject.instance().addMapLayer(layer)

        processing.run("qgisgeocodes:encodetofield", {
            'INPUT': layer,
            'CODE_TYPE': 2
        })

        for feature in layer.getFeatures():
            assert feature['geohash'] == expected
