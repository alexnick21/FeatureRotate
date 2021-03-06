# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeometryRotator
                                 A QGIS plugin
 Поворот геометрии выделенных объектов
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-07-05
        copyright            : (C) 2022 by alexnick21
        email                : alexnick_ank@mail.ru
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load GeometryRotator class from file GeometryRotator.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .geometry_rotator import GeometryRotator
    return GeometryRotator(iface)
