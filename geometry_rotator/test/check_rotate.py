import unittest
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
from ..rotation import Centroid

class TestFunction(unittest.TestCase):
    def test_true(self):
        self.assertEqual(1+1, 2)
    def test_centroid(self):
        self.assertAlmostEqual(Centroid.getCentroid(1, 1, 3, 3), None)
if __name__ == '__main__':
    unittest.main()