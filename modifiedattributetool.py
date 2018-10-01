# -*- coding: latin1 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsAttributeDialog


#Traigo la herramienta de seleccion
from modifiedattrtool import ModifiedAttrTool


class ModifiedAttributeTool():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        self.result = False
        
        # Create actions 
        self.md_attr= QAction(QIcon(":/plugins/AGCloacas/editar_attr.png"),  QCoreApplication.translate("AG_Cloacas", "Modificar Atributos"),  self.iface.mainWindow())
            
        self.md_attr.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.md_attr.triggered.connect(self.act_modified_attr)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.md_attr)
        # Get the tool
        self.tool = ModifiedAttrTool(self.iface)
        
        
    def act_modified_attr(self):
        
        if self.md_attr.isChecked():
            self.canvas.setMapTool(self.tool)
            self.tool.select_.connect(self.alm_res)
            self.activate()
            
            if self.result != False:
                print(self.result)
                
            else:
                pass
          
            
        else:
            self.deactivate()
            self.unsetTool()
    
    
    def alm_res(self, result):
        
        self.result = result
        
    def unsetTool(self):
        mc = self.canvas
        mc.unsetMapTool(self.tool)
            
    
    def activate(self):
        
        print("Activo la herramienta Modificar Atributos")
    
    
    def deactivate(self):
        
        mc = self.canvas
        
        layer = self.canvas.currentLayer()
        
        for la in mc.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
            mc.refresh()
        print("Desactivo la Herramienta de Modificar Atributos")