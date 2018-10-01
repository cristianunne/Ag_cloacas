# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGCloacas
                                 A QGIS plugin
 Módulo para manejar las cloacas
                             -------------------
        begin                : 2018-02-13
        copyright            : (C) 2018 by cristian
        email                : cristian297@hotmail.com
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
    """Load AGCloacas class from file AGCloacas.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ag_cloacas import AGCloacas
    return AGCloacas(iface)
