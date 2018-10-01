from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.core import QgsFeature, QgsGeometry, QgsPoint
from PyQt4.QtGui import QColor, QMessageBox
from qgis.gui import QgsAttributeDialog, QgsAttributeForm, QgsRubberBand, QgsVertexMarker
from ag_cloacas_dialog import AGCloacasDialog


class AddNodoTool(QgsMapTool):
    
    select_ = pyqtSignal(object)
    
    def __init__(self, iface):
        QgsMapTool.__init__(self, iface.mapCanvas())
        
        self.iface = iface
        self.qpoint = None
        
        self.geom_Sel = None
        
        self.dlg = AGCloacasDialog()
        
        self.canvas = iface.mapCanvas()
        
        self.r_polyline = None
        self.m = []
        
         #our own fancy cursor
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                  "      c None",
                                  ".     c #0000ff",
                                  "+     c #FFFFFF",
                                  "                ",
                                  "       +.+      ",
                                  "      ++.++     ",
                                  "     +.....+    ",
                                  "    +.     .+   ",
                                  "   +.   .   .+  ",
                                  "  +.    .    .+ ",
                                  " ++.    .    .++",
                                  " ... ...+... ...",
                                  " ++.    .    .++",
                                  "  +.    .    .+ ",
                                  "   +.   .   .+  ",
                                  "   ++.     .+   ",
                                  "    ++.....+    ",
                                  "      ++.++     ",
                                  "       +.+      "]))
        
        
    def activate(self):
        self.canvas.setCursor(self.cursor)
        
    def canvasPressEvent(self, e):
       
       self.qpoint = self.toMapCoordinates(e.pos())
       """if e.button() == Qt.LeftButton:
           self.qpoint = self.toMapCoordinates(e.pos())
           print("Boton Izquierdo")
       else:
           print("Boton Derecho")"""
      
            
    def canvasMoveEvent(self,event):
         pass
  
    def canvasReleaseEvent(self,e):
                 
        res = self.selecciona(self.qpoint)
        
        if res == True:
            
            res_dialog = self.showdialog()
            if(res_dialog == 1):
           
                layer = self.canvas.currentLayer()
            
                v_geom = self.geom_Sel.geometry()
                num_v = 0
                ver = v_geom.vertexAt(0)
                points=[]
 
                #count vertex and extract nodes
                while(ver != QgsPoint(0,0)):
              
                    num_v +=1
                    points.append(ver)
                    ver = v_geom.vertexAt(num_v)
            
                #CREAR UN ARCHIVO DE LINEA Y PASARLE A LA SELECCION
            
                mem_layer = self.memLayerFromSelect(layer, v_geom, num_v, points)
            
           
            
                self.canvas.refresh()
            
                #obtengo la parte seleccionada segun los vertices
                part = self.seleciona_part(self.qpoint, mem_layer)
                
                #obtengo los vertices para crear la nueva capa
                ver_1 = part.attributes()[1]
                ver_2 = part.attributes()[2]
                
                
                #obtengo las partes usando como indice los vertices y el punto seleccionado, para ellos creo dos listas
                list_part_1 = []
                list_part_2 = []
                
                long_linea_1 = 0
                long_linea_2 = 0
                
                #voy desde el primer vertice hasta el el antes del punto clickeado
                for i in range(num_v):
                    if i < ver_2:
                        list_part_1.append(v_geom.vertexAt(i))
                        
                list_part_1.append(self.qpoint)
                
                #la segunda parte empieza con el punto seleccionado y se agrega despues
                
                list_part_2.append(self.qpoint)
                
                for i in range(num_v):
                    if i > ver_1:
                        list_part_2.append(v_geom.vertexAt(i))
                        
                
                
                #calculo las distancia de los vertices
                long_linea_1 = self.distance_segmentos(list_part_1)
                long_linea_2 = self.distance_segmentos(list_part_2)

                
                if long_linea_1 >= long_linea_2:
                    self.changePart(list_part_1, layer, self.geom_Sel)
                    self.addPart(list_part_2, layer)
                    
                else:
                    self.changePart(list_part_2, layer, self.geom_Sel)
                    self.addPart(list_part_1, layer)
                layer.removeSelection()
        
        
        self.deactivate()
             
           

    def selecciona(self, point):
        
        #Borro la seleccion actual
        mc = self.iface.mapCanvas()
         #remuevo el rubber band
        
        
       
        
        for layer in mc.layers():
            if layer.type() == layer.VectorLayer:
                layer.removeSelection()
            mc.refresh()
        
        pntGeom = QgsGeometry.fromPoint(self.qpoint)
        pntBuffer = pntGeom.buffer((mc.mapUnitsPerPixel()*0.3), 0)
        rectan = pntBuffer.boundingBox()
        cLayer = mc.currentLayer()
        cLayer.select(rectan,False)
        
        feats = cLayer.selectedFeatures()
        n = len(feats)
        
        #si n es mayor a 1 deselecciono todo los demas a expecion del primer elemento
        if n >= 1:
            if n > 1:
                i = 1
                
                while (i < n):
                    cLayer.deselect(feats[i].id())
                    i = i + 1

                #obtengo el feature seleecionado y asigno
                self.geom_Sel = cLayer.selectedFeatures()[0]
                
            
            else:
                self.geom_Sel = cLayer.selectedFeatures()[0]
            
            mc.refresh()
            return True
        else:
            return False
        
    
    def seleciona_part(self, point, layer_mem):
        
        #point representa las coordenadas del click
        #layer_mem representa la nueva capa creada con los vertices
        mc = self.iface.mapCanvas()
        
        pntGeom = QgsGeometry.fromPoint(point)
        pntBuffer = pntGeom.buffer((mc.mapUnitsPerPixel()*0.3), 0)
        rectan = pntBuffer.boundingBox()
        cLayer = layer_mem
        cLayer.select(rectan,False)
        part = cLayer.selectedFeatures()[0]
        
        #llamo al metodo que crea el rubberband
        
        #self.addRubberBandPart(part)
        #self.addVertexMarker(part)
        
        mc.refresh()
        
        return part
        
    def addRubberBandPart(self, geom_):
        
        
        #get geometry
        self.canvas.scene().removeItem(self.r_polyline)
        self.canvas.refresh()
        
        
        self.r_polyline = QgsRubberBand(self.canvas, False)  # False = not a polygon
        geom_1 = geom_.geometry().asPolyline()
        
        color = QColor(0, 167, 0) 
        self.r_polyline.setToGeometry(QgsGeometry.fromPolyline(geom_1), None)
        self.r_polyline.setWidth(7)
        self.r_polyline.setColor(color)
        self.r_polyline.show()
        
    
    def addVertexMarker(self, part):
        
        #convierto a geometria la parte seleccionada
        v_geom = part.geometry()
        num_v = 0
        ver = v_geom.vertexAt(0)
        points=[]
 
        #count vertex and extract nodes
        while(ver != QgsPoint(0,0)):
              
            num_v +=1
            points.append(ver)
            ver = v_geom.vertexAt(num_v)
        
        
        for i in range(num_v):
            kk = QgsVertexMarker(self.canvas)
            self.m.append(kk)
        
        for i in range(num_v):
            self.m[i].setCenter(points[i])
            self.m[i].setColor(QColor(0, 0, 255))
            self.m[i].setIconSize(7)
            self.m[i].setIconType(QgsVertexMarker.ICON_BOX)  # See the enum IconType from http://www.qgis.org/api/classQgsVertexMarker.html
            self.m[i].setPenWidth(3)

            #self.m[i].hide()
            self.m[i].show()
            
    def memLayerFromSelect(self, layer, geom_sel, num_v, points):
        
        #creo la nueva geometria con las coordenadas de los vertices
        #Extract CRS from route
        CRS = layer.crs().postgisSrid()
        #print("CRS: " + str(CRS))
        #Creo la capa en el URI
        URI = "LineString?crs=epsg:"+str(CRS)+"&field=id:integer""&field=p1:integer""&field=p2:integer""&index=yes"
            
        #create memory layer
        mem_layer = QgsVectorLayer(URI,"Linea","memory")
        
        #add Map Layer to Registry
        #QgsMapLayerRegistry.instance().addMapLayer(mem_layer)

        #Prepare mem_layer for editing
        mem_layer.startEditing()
            
        #Set feature
        feature = []
            
        num_v = num_v - 1
            
        for j in range(num_v):
            fe = QgsFeature()
            feature.append(fe)
                
        for j in range(num_v):
            feature[j].setGeometry(QgsGeometry.fromPolyline([points[j], points[j + 1]]))
            feature[j].setAttributes([j, j, j + 1])
            mem_layer.addFeature(feature[j], True)
            
            
        i = 0
        for g in points:
                
            #print("Point " + str(i) + ": " + str(g.x()) + ", " + str(g.y()))
            i = i + 1
        
        #stop editing and save changes
        mem_layer.commitChanges()
        
        #metodo para remover un layer
        #QgsMapLayerRegistry.instance().removeMapLayer(mem_layer)
        return mem_layer
        
    
    def distance_segmentos(self, points_):
        
        #numero de puntos en la lista
        num_point = len(points_)
        
        final = num_point - 1
        
        long_linea = 0
        
        for i in range(num_point):
            if i < final:
                #ontengo el punto
                pun = points_[i]
                pun_2 = points_[i + 1]
                
                long_linea = long_linea + pun.distance(pun_2)
                
        return long_linea       
    
    def addPart(self, list_part, layer):
        
        list_1 = []
        list_1.append(list_part)
        
        geom_part_1 = QgsGeometry.fromMultiPolyline(list_1)
         
        num_attr = len(layer.attributeList())
                
        layer.startEditing()
         
        newgeom = QgsFeature()
        newgeom.setGeometry(QgsGeometry.fromMultiPolyline(list_1))
        
        #Cargo todos los atributos vacios
        attr_vacio = []
        attr_vacio.append("nextval('cloacas.cl_tramos_gid_seq'::regclass)")
        #recorro un for para setear los atributos
        for i in range(num_attr - 1):
            attr_vacio.append("")
         
        
        #agrego la parte al layer
        newgeom.setAttributes(attr_vacio)
        layer.addFeature(newgeom, True)
        layer.commitChanges()
        
      
    
    def changePart(self, list_part, layer, layer_sel):
        
        list_1 = []
        list_1.append(list_part)
        
        geom_part_1 = QgsGeometry.fromMultiPolyline(list_1)
         
        layer.startEditing()
         
        newgeom = QgsGeometry.fromMultiPolyline(list_1)
        
        layer.changeGeometry(layer_sel.id(), newgeom)
        layer.commitChanges()
    
    
    def deactivate(self):

        self.canvas.scene().removeItem(self.r_polyline)
        
        n = len(self.m)
        
        for i in range(n):
            self.canvas.scene().removeItem(self.m[i])
            
        del self.m[:]
        self.canvas.refresh()      
    
    def showdialog(self):
        """msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        msg.setText("Insertar CL_NODO?")
        msg.setWindowTitle("Insertar CL_NODOS")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()"""
        
        retval = QMessageBox.question(self.iface.mainWindow(),
                "Question", "Insertar CL_NODOS?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        val = None
        
        if retval == QMessageBox.Yes:
            
            val = 1
        else:
            val = 0
        
        
        return val
    
    
    
    
    
    
    
    
    
    
    
    