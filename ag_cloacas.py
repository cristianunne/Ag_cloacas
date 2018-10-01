# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AGCloacas
                                 A QGIS plugin
 Módulo para manejar las cloacas
                              -------------------
        begin                : 2018-02-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by cristian
        email                : cristian297@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog

import os.path


#obtengo las herramientas
from modifiedattributetool import ModifiedAttributeTool
#from nodostool import NodosTool
from CloacasConexion import CloacasConexion
from TramosAction import TramosAction
from DeleteTramosProperties import DeleteTramosProperties
from DirectionAction import DirectionAction
from DirectionDeleteAction import DirectionDeleteAction
from DirectionChange import DirectionChange
from CuencaTool import CuencaTool




class AGCloacas:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'AGCloacas_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'AGCloacas')
        self.toolbar.setObjectName(u'AGCloacas')

    
    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        # Get the tools

        self.modified_attr_tool = ModifiedAttributeTool(self.iface, self.toolbar)
        self.toolbar.addSeparator()
        #self.nodos_tool = NodosTool(self.iface, self.toolbar)
        #self.toolbar.addSeparator()
        self.conexion_tool = CloacasConexion(self.iface, self.toolbar)
        self.toolbar.addSeparator()
        self.tramos_action = TramosAction(self.iface, self.toolbar)
        self.delete_tramos_properties = DeleteTramosProperties(self.iface, self.toolbar)
        self.toolbar.addSeparator()
        self.direction_action = DirectionAction(self.iface, self.toolbar)
        self.direction_delete_action = DirectionDeleteAction(self.iface, self.toolbar)
        self.direcion_change = DirectionChange(self.iface, self.toolbar)
        self.toolbar.addSeparator()
        #self.cuenca_tool = CuencaTool(self.iface, self.toolbar)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&AG Cloacas'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
