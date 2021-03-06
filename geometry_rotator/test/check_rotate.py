import unittest
import sys
sys.path.append('../')

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

import rotation

class TestFunction(unittest.TestCase):
    def test_centroid(self):
        self.assertAlmostEqual(rotation.Centroid.getCentroid(1, 1, 3, 3).asWkt(), 'POINT(2 2)')
if __name__ == '__main__':
    unittest.main()