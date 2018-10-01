# -*- coding: utf-8 -*-
"""
/***************************************************************************
 WhereAmIDialog
                                 A QGIS plugin
 Localiza las coordenadas de un punto
                             -------------------
        begin                : 2018-01-03
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Cristian
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtGui import QPixmap


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Symbol_inicio_tramos_dialog_base.ui'))


class Symbol_inicioTramosDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(Symbol_inicioTramosDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
   
        self.setupUi(self)
        self.initUI()
        
        
        
    def initUI(self):
        
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'PLD.png'))
        self.pld_inicio.setPixmap(pixmap)
        
        pixmapdes_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'DES.png'))
        self.des_inicio.setPixmap(pixmapdes_inicio)
        
        pixmapcal_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'CAL.png'))
        self.cal_inicio.setPixmap(pixmapcal_inicio)
        
        pixmapbrv_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'BRV.png'))
        self.brv_inicio.setPixmap(pixmapbrv_inicio)
        
        pixmapbrs_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'BRS.png'))
        self.brs_inicio.setPixmap(pixmapbrs_inicio)
        
        pixmapese_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'ESE.png'))
        self.ese_inicio.setPixmap(pixmapese_inicio)
        
        pixmapbrh_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'BRH.png'))
        self.brh_inicio.setPixmap(pixmapbrh_inicio)
        
        pixmaptil_inicio = QPixmap(os.path.join(os.path.dirname(__file__), 'TIL.png'))
        self.til_inicio.setPixmap(pixmaptil_inicio)
        
        
        
        
        
        
        
        
        
