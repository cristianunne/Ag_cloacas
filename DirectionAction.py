from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from ClDirectionEntity import ClDirectionEntity



class DirectionAction():
    
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        
          # Create actions 
        self.direction = QAction(QIcon(":/plugins/AGCloacas/direction.png"),  QCoreApplication.translate("AG_Cloacas", "Agregar Direccion al Tramo"),  self.iface.mainWindow())
            
        self.direction.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.direction.triggered.connect(self.direction_action)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.direction)
        
        
        
    def direction_action(self):
        
        
        #primero utilizo el box para consultar si agregar
        #Accedo si el tool ha sido activado
        if self.direction.isChecked():
            
            res_dialog = self.showdialog()
            if(res_dialog == 1):
            
                try:
                    
                    layer_cl_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_tramos')[0]
                    layer_cl_direction = QgsMapLayerRegistry.instance().mapLayersByName('cl_direction')[0]
                    
                    #instanciio las clases e inicializo
                    cl_direction_entity = ClDirectionEntity()
                    cl_direction_entity.initialize(layer_cl_direction)
                    
                   
                    
                    try:
                        layer_select_tramo = layer_cl_tramos.selectedFeatures()
                        
                        if(len(layer_select_tramo) >= 1):
                            select_tramo = layer_cl_tramos.selectedFeatures()[0]
                            if cl_direction_entity.addDirection(select_tramo):
                                self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)
                                self.direction.setChecked(False)
                            
                    except(IndexError):
                        self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", level=QgsMessageBar.WARNING)
                    
                    
                    
                
                except (IndexError):
                    self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_tramos', 'cl_direction'", level=QgsMessageBar.CRITICAL)
                    self.direction.setChecked(False)
                    
            self.direction.setChecked(False)
        
        
        
        
    
    
    def showdialog(self):
        """msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        msg.setText("Insertar CL_NODO?")
        msg.setWindowTitle("Insertar CL_NODOS")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()"""
        
        retval = QMessageBox.question(self.iface.mainWindow(),
                "Question", "Agregar Direccion?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        val = None
        
        if retval == QMessageBox.Yes:
            
            val = 1
        else:
            val = 0
        
        
        return val        
        
    
    