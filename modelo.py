from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

#obtengo la herramienta que agrega el nodo
from addnodotool import AddNodoTool

class NodosTool():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        self.result = False
        
        # Create actions 
        self.nodos = QAction(QIcon(":/plugins/AGCloacas/cl_tramos.png"),  QCoreApplication.translate("AG_Cloacas", "Agregar Nodos Cloacas"),  self.iface.mainWindow())
            
        self.nodos.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.nodos.triggered.connect(self.act_add_nodos)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.nodos)
        # Get the tool
        self.tool = AddNodoTool(self.iface)
        
       
        
    def act_add_nodos(self):
        
        #evaluo que el currentlayer sea cl_tramos 
        
        layer = self.canvas.currentLayer()
        
        if self.nodos.isChecked():
             #evaluo que el currentlayer sea cl_tramos     
            if layer.name() == "cl_tramos":
                print("El current es cl_tramos")
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage("Error", "Debe seleccionar la capa 'cl_tramos'", level=QgsMessageBar.CRITICAL)
                self.nodos.setChecked(False)
                print(layer.name())
            
        else:
            self.deactivate()
            self.unsetTool()
        
    def activate(self):
        
        pass
    
    
    def deactivate(self):
        
        pass
        
       
    def unsetTool(self):
        pass