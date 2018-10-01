
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import QgsMessageBar, QgsRubberBand
import os.path, sys
from symbol import except_clause

sys.setrecursionlimit(10000)



class CuencaTool():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        self.result = False
        #Clase que maneja el trdom
        self.cl_trdom = None
        self.info_td = None
        
        
        # Create actions 
        self.cuenca = QAction(QIcon(":/plugins/AGCloacas/icon.png"),  QCoreApplication.translate("AG_Cloacas", "Crear Cuenca"),  self.iface.mainWindow())
            
        self.cuenca.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.cuenca.triggered.connect(self.CuencaAction)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.cuenca)
        
        
    def CuencaAction(self):
          
        if self.cuenca.isChecked():
             #Verifico que las tablas esten cargadas
            
            
            try:
                #Verifico que las tablas esten cargadas

                layer_cl_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_tramos')[0]
                layer_cl_cotas = QgsMapLayerRegistry.instance().mapLayersByName('cl_cotas')[0]
                layer_cl_ventilacion = QgsMapLayerRegistry.instance().mapLayersByName('cl_ventilacion')[0]
            
                
                res_dialog = self.showdialog()
                if(res_dialog == 1):
                    self.processCuenca(layer_cl_tramos, layer_cl_cotas, layer_cl_ventilacion)
                
                self.cuenca.setChecked(False)
                
                
            except (IndexError):
                self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_tramos'", level=QgsMessageBar.CRITICAL)
                self.cuenca.setChecked(False)
    
    
    def processCuenca(self, layer_cl_tramos, layer_cl_cotas, layer_cl_ventilacion):
        
        #Almacena los tramos que pertenecen a la cuenca
        lista_tramos_cuenca = []
        
        feat_cltramos = None
        try:
            feat_cltramos = layer_cl_tramos.selectedFeatures()
            
            if(len(feat_cltramos) >= 1):
                feat_cltramos = layer_cl_tramos.selectedFeatures()[0]
                
                
                lista_ = [feat_cltramos]
                lista_tramos_cuenca.append(feat_cltramos)
                
                self.runArbolCuenca(lista_, layer_cl_tramos, lista_tramos_cuenca, layer_cl_ventilacion)
                
                print("Cantidad Final de Tramos: " + str(len(lista_tramos_cuenca)))
                
                #creo el mem_layer
                mem_layer = self.createMemLayer(layer_cl_tramos, "cuenca")
                
                vector_ = self.createVectorLayer(lista_tramos_cuenca, mem_layer)
                
                
                
                
                renderer =  vector_.rendererV2()
              
                symbol = renderer.symbol()
                symbol.setColor(QColor('green'))
                symbol.setWidth(2)
               
                
                
                QgsMapLayerRegistry.instance().addMapLayer(vector_)
                
                
               
            
            else:
                self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", level=QgsMessageBar.WARNING)
            
            
            
        except (IndexError):
           
            self.iface.messageBar().pushMessage("Error", "Debe seleccionar 1 tramo", level=QgsMessageBar.CRITICAL) 
    
    
    
    
    def getCotaFinal(self, layer_cl_cotas, tramo):
        
        for cotas in layer_cl_cotas.getFeatures():
            
            if cotas['tramo_idtramo'] == tramo['gid'] and cotas['tipo'] == 'Fin':
                
                return cotas
        
        return None
    
    
    
    def getObjectByPosition(self, tramo_select, layer_cl_tramos, lista_tramos_cuenca, layer_cl_ventilacion):
        
        lista_objects = []
        
        #obtengo el ultimo vertice del tramo seleccionado
        vertices = tramo_select.geometry().asMultiPolyline()
        vertc_poly = vertices[0]
        cantiad_vert = len(vertc_poly)
        last_vert = vertc_poly[cantiad_vert - 1]
        point_ = QgsGeometry.fromPoint(last_vert)
        id_tramo = tramo_select['gid']
        
        
        #Necesito consultar que el punto que toque del tramo sea el final
        
        for tramos in layer_cl_tramos.getFeatures():
            
            
            #Convierto el tramo a vertices para saber si es el punto final el que toca
            
            if point_.touches(tramos.geometry()) and tramos['gid'] != id_tramo:
                
                #Consulto si toca el tramo Inicial
                vert_2 = tramos.geometry().asMultiPolyline()
                vert_poly_2 = vert_2[0]
                inicial_vert = vert_poly_2[0]
                
                
                if last_vert == inicial_vert:
            
                    if tramos['tipo'] != None:
                        
                        if self.existVentilacion(tramos['gid'], layer_cl_ventilacion) == False:
                            lista_objects.append(tramos)
                            lista_tramos_cuenca.append(tramos)
                    
                    
                
        
        
        return lista_objects
    
    
    def existVentilacion(self, id_tramo, layer_cl_ventilacion):
        
        for vent in layer_cl_ventilacion.getFeatures():
            if id_tramo == vent['tramo_idtramo']:
                 return True
             
        return False     
             
    
    
    def runArbolCuenca(self, lista_objects, layer_cl_tramos, lista_tramos_cuenca, layer_cl_ventilacion):
        
        lis = []
        
        print("cantidad tramos pasados: " + str(len(lista_objects)))
        if len(lista_objects) > 0:
            for i in range(len(lista_objects)):
                layer_cl_tramos.select(lista_objects[i].id())
                print(lista_objects[i]['gid'])
                
                #funcion recursiva
                lista_ = self.getObjectByPosition(lista_objects[i], layer_cl_tramos, lista_tramos_cuenca, layer_cl_ventilacion)
                
                print("cantidad tramos touch: " + str(len(lista_)))
                
                if len(lista_) > 0:
                    
                    self.runArbolCuenca(lista_, layer_cl_tramos, lista_tramos_cuenca, layer_cl_ventilacion)
                
              
        return
    
    
    
    def createMemLayer(self, layer, name):

        CRS = layer.crs().postgisSrid()
 
        URI = "MultiLineString?crs=epsg:"+str(CRS)+"&field=id:integer""&index=yes"
        #create memory layer
        mem_layer = QgsVectorLayer(URI,
                            name,
                            "memory")
        return mem_layer
    
    
    
    def createVectorLayer(self, array_line, mem_layer):
        #Arrayline contiene los puntos de las lineas
        #Prepare mem_layer for editing
        mem_layer.startEditing()
        
            
        for i in range(len(array_line)):
            feature = QgsFeature()
            feature.setGeometry(array_line[i].geometry())
            feature.setAttributes([i])
            mem_layer.addFeature(feature)
        mem_layer.commitChanges()
        return mem_layer
    
    
    
    def showdialog(self):

        
        retval = QMessageBox.question(self.iface.mainWindow(),
                "Question", "Crear Cuenca para el tramo seleccionado?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        val = None
        
        if retval == QMessageBox.Yes:
            
            val = 1
        else:
            val = 0
        
        
        return val        
    
    