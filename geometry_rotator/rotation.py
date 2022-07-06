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
from .geometry_rotation import (
    PointRotation,
    MultiPointRotation,
    LineRotation,
    MultiLineRotation,
    PolygonRotation,
    MultiPolygonRotation,
)

# Разворот объектов активного слоя
class RotateSelectedLayer:
    def rotateLayer(iface, angle_text):
        Xmin = []
        Xmax = []
        Ymin = []
        Ymax = []
    
        angle = float(str(angle_text))
        layer = iface.activeLayer()
        features = layer.selectedFeatures()        

        # Присматриваемся к слою
        # Выясняем параметры этого Мирка
        for feature in features:
            geom = feature.geometry()

            # Копим координаты конвертов
            # по конвертам выясним большой конверт
            # а его центроид будем считать геометрическим центром всего стада объектов
            # грубо, но просто...
            ext = geom.boundingBox()
            Xmin.append(ext.xMinimum())
            Xmax.append(ext.xMaximum())
            Ymin.append(ext.yMinimum())
            Ymax.append(ext.yMaximum())
        
        # Выясняем где центр Мирка избранных объектов
        # Приготовим конверт
        gPolygon = QgsGeometry.fromPolygonXY([[QgsPointXY(min(Xmin), min(Ymin)),
                                               QgsPointXY(min(Xmin), max(Ymax)),
                                               QgsPointXY(max(Xmax), max(Ymax)),
                                               QgsPointXY(max(Xmin), min(Ymin)),
                                               QgsPointXY(min(Xmin), min(Ymin))]])
        # Вожделенный центр
        cp = gPolygon.centroid().asPoint()

        # Теперь начинаем все это дербанить по-взрослому
        # К геометрии подход индивидуальный в зависимости от типа
        # Геометрические оси симетрии? Чавойта? Не слышали о таком!
        for feature in features:
            # Исторгнем мусорное сообщение
            QgsMessageLog.logMessage(u"Объект ID: " + str(feature.id()),"geometry_rotator")
            
            geom = feature.geometry()
            
            # Выясняем Партийность геометрии
            geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
            if geom.type() == QgsWkbTypes.PointGeometry:
                if geomSingleType:
                    obj = geom.asPoint()
                    QgsMessageLog.logMessage("Point: "+ str(obj.asWkt()),"geometry_rotator")
                    try:
                        result_geom = PointRotation.rotatePoint(obj, cp, angle)
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue
                    
                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
                else:
                    obj = geom.asMultiPoint()
                    QgsMessageLog.logMessage("MultiPoint: "+ str(geom.asWkt()),"geometry_rotator")                    
                    try:
                        result_geom = MultiPointRotation.rotateMultiPoint(obj, cp, angle)
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue
                    
                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
            elif geom.type() == QgsWkbTypes.LineGeometry:
                if geomSingleType:
                    obj = geom.asPolyline()
                    QgsMessageLog.logMessage("Line: "+str(geom.asWkt()) + u" длина: " +str( geom.length()),"geometry_rotator")
                    try:
                        result_geom = QgsGeometry.FromPolylineXY(LineRotation.rotateMultiPoint(obj, cp, angle))
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue
                    
                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
                else:
                    obj = geom.asMultiPolyline()
                    QgsMessageLog.logMessage("MultiLine: " + str(geom.asWkt()) + u" длина: " + str(geom.length()),"geometry_rotator")
                    try:
                        result_geom = MultiLineRotation.rotateMultiLine(obj, cp, angle)
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()                    
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue

                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
            elif geom.type() == QgsWkbTypes.PolygonGeometry:
                if geomSingleType:
                    obj = geom.asPolygon()
                    QgsMessageLog.logMessage("Polygon: " + str(geom.asWkt()) + " площадь: " +  str(geom.area()),"geometry_rotator")
                    try:
                        result_geom = QgsGeometry.FromPolygonXY(PolygonRotation.rotatePolygon(obj, cp, angle))
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()                    
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue

                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
                else:
                    obj = geom.asMultiPolygon()
                    QgsMessageLog.logMessage("MultiPolygon: " + str(geom.asWkt()) + " площадь: " + str(geom.area()),"geometry_rotator")
                    try:
                        result_geom = MultiPolygonRotation.rotateMultiPolygon(obj, cp, angle)
                        layer.startEditing()
                        layer.changeGeometry(feature.id(), result_geom )
                        layer.commitChanges()                    
                    except Exception as e:
                        QgsMessageLog.logMessage(u"Ошибка разворота объекта: " + str(e),"geometry_rotator")
                        continue

                    QgsMessageLog.logMessage(u"Поворот завершен успешно.","geometry_rotator")
            else:
                QgsMessageLog.logMessage(u"Нечто непонятное! Его не лечим!","geometry_rotator")
                continue
            
            

    
