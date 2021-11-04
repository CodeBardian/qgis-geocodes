from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsField, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessing,
                       QgsProcessingParameterField, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject,
                       QgsProcessingParameterCrs, QgsGeometry, QgsProcessingParameterFeatureSink, QgsFields,
                       QgsWkbTypes, QgsFeatureSink, QgsProcessingException)

from GeocodeTools.utils import toPosition


class DecodeAlgorithm(QgsProcessingAlgorithm):
    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    INPUT = 'INPUT'
    INPUT_CRS = 'INPUT_CRS'
    CODE_FIELD = 'CODE_FIELD'
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(self.INPUT, self.tr('Input file'),
                                                            types=[QgsProcessing.TypeFile ]))

        self.addParameter(QgsProcessingParameterField(self.CODE_FIELD, 'Geocode Column',
                                                      parentLayerParameterName=self.INPUT,
                                                      type=QgsProcessingParameterField.String))

        self.addParameter(QgsProcessingParameterCrs(self.INPUT_CRS, 'Set Layer CRS', 'EPSG:4326', optional=True))
        self.addParameter(QgsProcessingParameterFeatureSink(self.OUTPUT, self.tr('Output layer')))

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        code_field = self.parameterAsString(parameters, self.CODE_FIELD, context).strip()
        input_crs = self.parameterAsCrs(parameters, self.INPUT_CRS, context)

        if input_layer is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context, QgsFields(input_layer.fields()),
                                               QgsWkbTypes.Point, input_crs)

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        feedback.pushInfo(f'Creating layer with CRS {input_crs.authid()}')

        total = 100.0 / input_layer.featureCount() if input_layer.featureCount() else 0
        field_index = input_layer.fields().indexFromName(code_field)
        for i, feature in enumerate(input_layer.getFeatures()):
            if feedback.isCanceled():
                break

            code = feature.attributes()[field_index]
            lat, lon = toPosition(code)

            transform = QgsCoordinateTransform(self.epsg4326, input_crs, QgsProject.instance())
            pt = transform.transform(lon, lat)

            g = QgsGeometry.fromPointXY(pt)
            feature.setGeometry(g)
            sink.addFeature(feature, QgsFeatureSink.FastInsert)

            feedback.setProgress(int(i * total))

        input_layer.commitChanges()

        return {"OUTPUT": dest_id}

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return DecodeAlgorithm()

    def name(self):
        return 'Convert Table to Point Layer'

    def displayName(self):
        return 'Convert Table to Point Layer'

    def shortHelpString(self):
        return 'Creates a map layer with point geometry from tables with a column of geocode values'