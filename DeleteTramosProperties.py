from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from ClTramosEntity import ClTramosEntity
from ClNodoTrSymbolEntity import ClNodoTrSymbolEntity
from ClVentilacionEntity import ClVentilacionEntity
from ClNodosEntity import ClNodosEntity
from ClCotasEntity import ClCotasEntity

from ClNodosTramos import ClNodosTramosEntity
from ClDirectionEntity import ClDirectionEntity



class DeleteTramosProperties():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        
         # Create actions 
        self.tramos_delete = QAction(QIcon(":/plugins/AGCloacas/polilinea_delete.png"),  QCoreApplication.translate("AG_Cloacas", "Eliminar Propieades del Tramo"),  self.iface.mainWindow())
            
        self.tramos_delete.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.tramos_delete.triggered.connect(self.action_delete_properties)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.tramos_delete)
        
        #Set Eavbled a los vbotomnes d los formnularios

    def deleteTramo(self, tramo_select, cl_tramos_entity):
        if cl_tramos_entity.deleteTramo(tramo_select):
            return True
        else:
            return False



    def action_delete_properties(self):
        #Accedo si el tool ha sido activado
        if self.tramos_delete.isChecked():
            
            res_dialog = self.showdialog()
            if(res_dialog == 1):
            
                try:
                    
                    layer_cl_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_tramos')[0]
                    cl_nodo_tr_symbol = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodo_tr_symbol')[0]
                    cl_ventilacion = QgsMapLayerRegistry.instance().mapLayersByName('cl_ventilacion')[0]
                    layer_cl_nodos = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos')[0]
                    layer_cl_cotas = QgsMapLayerRegistry.instance().mapLayersByName('cl_cotas')[0]
                    self.layer_cl_nodos_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos_tramos')[0]
                    layer_cl_direction = QgsMapLayerRegistry.instance().mapLayersByName('cl_direction')[0]

                    #Instancio las entidades y le paso las capas correspondietes
                    self.cl_tramos_entity = ClTramosEntity()
                    self.cl_tramos_entity.initialize(layer_cl_tramos)
                    
                    self.cl_nodo_symbol_entity = ClNodoTrSymbolEntity()
                    self.cl_nodo_symbol_entity.initialize(cl_nodo_tr_symbol)
                    
                    self.cl_ventilacion_entity = ClVentilacionEntity()
                    self.cl_ventilacion_entity.initialize(cl_ventilacion)

                    self.cl_nodos_entity = ClNodosEntity()
                    self.cl_nodos_entity.initialize(layer_cl_nodos)
                    
                    self.cl_cotas_entity = ClCotasEntity()
                    self.cl_cotas_entity.initialize(layer_cl_cotas)
                    
                    self.cl_nodos_tramos_entity = ClNodosTramosEntity()
                    self.cl_nodos_tramos_entity.initialize(self.layer_cl_nodos_tramos)

                    self.cl_direction_entity = ClDirectionEntity()
                    self.cl_direction_entity.initialize(layer_cl_direction)
                    
                    #verifico que haya al menos un elemento seleccionado
                    layer_select_tramo = layer_cl_tramos.selectedFeatures()
                    
                    if(len(layer_select_tramo) >= 1):
                        #guardo solo el elemento 1 de la seleccion
                        tramo_select = layer_select_tramo[0]
                        #borro los simbolos
                        if self.cl_nodo_symbol_entity.deleteNodoSymbol(tramo_select, True, layer_cl_tramos):
                            if self.cl_nodo_symbol_entity.deleteNodoSymbol(tramo_select, False, layer_cl_tramos):
                                
                                #Elimino la ventilacion
                                if self.cl_nodo_symbol_entity.getTypeSimbol(tramo_select) == "BRV":
                                    self.cl_ventilacion_entity.deleteVentilacion(tramo_select)
                                    self.cl_tramos_entity.deleteVertex(tramo_select)
                                    
                                #seteo a Null los datos del tramo
                                
                                if self.cl_tramos_entity.setNullData(tramo_select):
                                    #borro los nodos tengo que pasar la entidad
                                    
                                    if self.cl_nodos_entity.deleteNodos(tramo_select, self.cl_nodos_tramos_entity, self.layer_cl_nodos_tramos):
                                        #borro las cotas
                                        if self.cl_cotas_entity.deleteCotas(tramo_select):
                                            #borro la direccion
                                            if self.cl_direction_entity.deleteDirectionByTramo(tramo_select):

                                                #elimino la ventilacion
                                                if self.cl_ventilacion_entity.deleteVentilacion(tramo_select):
                                                    #llamo al metodo eliminar tramo
                                                    self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)
                                                    self.tramos_delete.setChecked(False)

                        self.cl_tramos_entity.deleteTramo(tramo_select)
                    
                    else:
                        self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", level=QgsMessageBar.WARNING)
                        self.tramos_delete.setChecked(False)
                    
                
                except (IndexError):
                    self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_tramos', 'cl_nodo_tr_symbol', 'cl_ventilacion', 'cl_cotas', 'cl_nodos'", level=QgsMessageBar.CRITICAL)
                    self.tramos_delete.setChecked(False)
                    
            self.tramos_delete.setChecked(False)
                
                
    def showdialog(self):
        
        retval = QMessageBox.question(self.iface.mainWindow(),
                "Question", "Borrar Propiedades del Tramo?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        val = None
        
        if retval == QMessageBox.Yes:
            
            val = 1
        else:
            val = 0
        
        
        return val