from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar
#Obtengo la clase de Tramos para convertir
from ClTramosEntity import ClTramosEntity
import operator



class ClDirectionEntity():
    
    def __init__(self):
        
        self.cl_direction = None

    def initialize(self, cl_direction):
        
        self.cl_direction = cl_direction

    def addDirection(self, tramo_select):
        
        #instancio la clase cltramosentity
        self.cltramosentity = ClTramosEntity()
        
        #Obtengo los puntos del tramo seleccionado
        array_point_tramo =  self.cltramosentity.getVertexTramoAsPoint(tramo_select)
        
        #obtengo el centroide el tramo utilizando el lentg / 2 porque sino se sale de la linea
        long = tramo_select.geometry().length() / 2
        
        #hago una interpolacion en la linea y obtengo el punto medio
        centroide = tramo_select.geometry().interpolate(long).asPoint()

        
        #arreglo que guardara los vertices que cumplen la condicion
        array_cond = []
        
        #obtengo el numero de vertices
        num_ver =  self.cltramosentity.getNumVertex(tramo_select)
        diccionario = {}
        
        if num_ver > 2:
            i = 0
            for point in array_point_tramo:
                
                diccionario[i] = centroide.distance(point)
                i = i + 1
                
       
        resultado = sorted(diccionario.items(), key=operator.itemgetter(1))
       
        mem_line_segment = self.SegmentLineToLine(tramo_select)
        
        linea_target = None
        
        for linea in mem_line_segment.getFeatures():
            buffer = QgsGeometry.fromPoint(centroide).buffer(0.2, 1)
            
            if linea.geometry().intersects(buffer):
                linea_target = linea
       
        
        #obtengo los vertices de la linea target como point
        linea_target_point = self.cltramosentity.getVertexTramoAsPoint(linea_target)
        
        point_select = linea_target_point[1]
        
        #calculo el angulo de orientacion del icono
        angulo = centroide.azimuth(point_select) + 2
               
        #inicio la edicion de cl_direction
        id_tramo = tramo_select['gid']
        
        self.cl_direction.startEditing()
        
          #obtengo los atributos
        attrs = [None] * len(self.cl_direction.fields())
        
        #obtengo el id de la clave foranea
        idx_tramo = self.cl_direction.fieldNameIndex("tramo_idtramo")
        idx_angulo = self.cl_direction.fieldNameIndex("angulo")
        
        #asigno el id a la clave foranea
        attrs[idx_tramo] = id_tramo
        attrs[idx_angulo] = angulo
        
        #creo un feature
        feature = QgsFeature()
        
        feature.setGeometry(QgsGeometry.fromPoint(centroide))
        feature.setAttributes(attrs)
        res = self.cl_direction.addFeature(feature)
        
        if res:
            
            if self.cl_direction.commitChanges():
                return True
            else:
                self.cl_direction.rollBack()
                return False
        else:
            return False

    
    def SegmentLineToLine(self, tramo_select):
        #Obtengo los puntos del tramo seleccionado
        array_point_tramo =  self.cltramosentity.getVertexTramoAsPoint(tramo_select)
        num_point_poly = len(array_point_tramo)
        
        mem_layer = self.createMemLayer(self.cl_direction, "segment_line")
        
        array_line = []
        for i in range(num_point_poly - 1):
            #accedo al primer punto
            segmento = []
            segmento.append(array_point_tramo[i])
            segmento.append(array_point_tramo[i + 1])
            array_line.append(segmento)
            
            
          #Guarda el vector de linea creado
     
        vector_line = self.createVectorLayer(array_line, mem_layer)
        #QgsMapLayerRegistry.instance().addMapLayer(vector_line)
       
        
        return vector_line
     
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
        n_seg = len(array_line)
        feature = QgsFeature()
        feature = []
        
        for i in range(n_seg):
            feat =QgsFeature()
            feature.append(feat)
            
        for i in range(n_seg):
            feature[i].setGeometry(QgsGeometry.fromPolyline(array_line[i]))
            feature[i].setAttributes([i])
        mem_layer.addFeatures(feature)
        mem_layer.commitChanges()
        return mem_layer
    
    def deleteDirectionByTramo(self, tramo_select):
        
        #obtengo el id del tramo
        id_tramo = tramo_select['gid']
        
        for feat in self.cl_direction.getFeatures():
            
            if feat['tramo_idtramo'] == id_tramo:
                self.cl_direction.startEditing()
                
                res = self.cl_direction.deleteFeature(feat.id())
                if res:
            
                    if self.cl_direction.commitChanges():
                        return True
                    else:
                        self.cl_direction.rollBack()
                        return False
    
        return False 

    def deleteDirection(self, dir_select):
        
        self.cl_direction.startEditing()
                
        res = self.cl_direction.deleteFeature(dir_select.id())
        if res:
            
            if self.cl_direction.commitChanges():
                return True
            else:
                self.cl_direction.rollBack()
                return False
    
        return False

    def changeDirection(self, dir_select):

        angulo = dir_select['angulo']

        if angulo > 180:
            angulo = angulo - 180
        else:
            angulo = angulo + 180

        #obtengo el id del punto_symbol


            #obtengo los indices de las columnas
        idx_angulo = self.cl_direction.fieldNameIndex("angulo")

        attrs = {idx_angulo: angulo}

        if self.cl_direction.dataProvider().changeAttributeValues({dir_select['gid']: attrs}):

            return True
        else:
            return False