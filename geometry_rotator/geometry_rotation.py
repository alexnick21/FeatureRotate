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
  QgsMultiLineString
)

from qgis.core.additions.edit import edit

from qgis.PyQt.QtGui import (
    QColor,
)
from qgis.PyQt.QtWidgets import QAction,QMessageBox

# Класс разворота точек
class PointRotation:
    # Поворот точки
    # geom - геометрия,
    # cp-центральная точка,
    # angle - угол
    def rotatePoint(geom, cp, angle):
        # Строим полилинию от центра до нашей точки
        # и вертим ее вокруг центра
        poline = QgsGeometry.fromPolylineXY([cp, geom]);
        poline.rotate(angle, cp)
        g = poline.asPolyline()
        start_point = QgsPoint(g[0])
        end_point = QgsPoint(g[-1])
        # Выбираем точку конца радиуса разворота
        result_point = QgsGeometry().fromWkt(end_point.asWkt())
        return result_point

#Класс разворота мультиточек
class MultiPointRotation:
    # По точечке по точечке и объект повернут
    def rotateMultiPoint(geom, cp, angle):        
        for i in range(geom.partCount()):
            new_part = PointRotation.rotatePoint(geom.parts[i].asPoint(), cp, angle)
            geom.parts[i] = new_part

# Класс разворота линий
class LineRotation:
    def rotateLine(geom, cp, angle):
        for i in range(len(geom)):
            new_part = PointRotation.rotatePoint(geom[i], cp, angle)
            p = new_part.asPoint()
            res_pnt = QgsPoint()
            res_pnt.fromWkt(p.asWkt())
            geom[i] = res_pnt
        return geom

# Класс разворота мультилиний    
class MultiLineRotation:
    def rotateMultiLine(geom, cp, angle):
        gparts = []
        for i in range(len(geom)):
            new_part = LineRotation.rotateLine(geom[i], cp, angle)
            geom[i] = new_part
            gparts.append(new_part)            
            
        # Сборка объекта    
        result_geom = QgsGeometry.fromPolyline(gparts[0])
        if len(gparts) > 1:
            for i in range(1,len(gparts)):
                result_geom.addPartGeometry(QgsGeometry.fromPolyline(gparts[i]))
                
        return result_geom
