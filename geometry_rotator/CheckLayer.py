# -*- coding: utf-8 -*-
from qgis.core import (
  QgsApplication,
  QgsDataSourceUri,
  QgsCategorizedSymbolRenderer,
  QgsClassificationRange,
  QgsPointXY,
  QgsProject,
  QgsExpression,
  QgsField,
  QgsFields,
  QgsFeature,
  QgsFeatureRequest,
  QgsFeatureRenderer,
  QgsGeometry,
  QgsGraduatedSymbolRenderer,
  QgsMarkerSymbol,
  QgsMessageLog,
  QgsRectangle,
  QgsRendererCategory,
  QgsRendererRange,
  QgsSymbol,
  QgsVectorDataProvider,
  QgsVectorLayer,
  QgsVectorFileWriter,
  QgsWkbTypes,
  QgsSpatialIndex,
  QgsVectorLayerUtils,
  QgsPoint,
)

from qgis.core.additions.edit import edit

from qgis.PyQt.QtGui import (
    QColor,
)
from qgis.PyQt.QtWidgets import QAction,QMessageBox

# Проверка слоя и угла поворота на соответствие условиям работы плагина
class CheckLayer:
    def isOK(iface, angle_text):
        try:
            angle = float(str(angle_text))
        except ValueError:
            QMessageBox.warning(None, u"Ошибка", u'Входная строка имела некорректный формат')
            return False

        layer = iface.activeLayer()
    
        if layer == None:
            QMessageBox.warning(None, u"Ошибка", u'Нет выделено ни одного слоя')
            return False
    
        features = layer.selectedFeatures()

        if len(features) == 0:
            QMessageBox.warning(None, u"Ошибка", u'В активном слое нет ни одного выделенного объекта')
            return False
    
        return True

