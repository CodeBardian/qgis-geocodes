from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsField, QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer, QgsProcessing,
                       QgsProcessingParameterEnum, QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsProject)

from GeocodeTools.utils import GeocodeType, toGeocode


class EncodeAlgorithm(QgsProcessingAlgorithm):
    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    INPUT = 'INPUT'
    CODE_TYPE = 'CODE_TYPE'

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorLayer(self.INPUT, self.tr('Input layer'),
                                                            types=[QgsProcessing.TypeVectorPoint]))

        self.addParameter(QgsProcessingParameterEnum(self.CODE_TYPE, 'Geocode Type',
                                                     options=[e.name for e in GeocodeType], defaultValue=0,
                                                     optional=False))

    def processAlgorithm(self, parameters, context, feedback):
        input_layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        code_type_index = self.parameterAsEnum(parameters, self.CODE_TYPE, context)
        code_type = list(GeocodeType)[code_type_index]

        feedback.pushInfo(f'{code_type.value}')

        input_layer.startEditing()
        if code_type.value not in input_layer.fields().names():

            input_layer.addAttribute(QgsField(code_type.value, QVariant.String))
            input_layer.updateFields()

        total = 100.0 / input_layer.featureCount() if input_layer.featureCount() else 0
        field_index = input_layer.fields().indexFromName(code_type.value)
        for i, feature in enumerate(input_layer.getFeatures()):
            if feedback.isCanceled():
                break

            transform = QgsCoordinateTransform(input_layer.crs(), self.epsg4326, QgsProject.instance())
            pt = feature.geometry().asPoint()
            pt4326 = transform.transform(pt.x(), pt.y())

            code = toGeocode(pt4326, code_type)
            input_layer.changeAttributeValue(feature.id(), field_index, code)

            feedback.setProgress(int(i * total))

        input_layer.commitChanges()

        return {"OUTPUT": input_layer.id()}

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return EncodeAlgorithm()

    def name(self):
        return 'encodetofield'

    def displayName(self):
        return 'Append Geocode Field to Point Layer'

    def shortHelpString(self):
        return 'Encode location of each feature in a point layer and append result as attribute'