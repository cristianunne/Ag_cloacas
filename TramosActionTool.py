from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar


class TramosActionTool():
    
    def __init__(self, iface, toolbar):
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        
        
    def addVertexToLine(self, layer_line, feat_line):
        #distancia ocupada para interpolar el punto
        distance = 10
        
        geom_line = feat_line.geometry()
        
        #inicio la edicion del layer
        layer_line.startEditing()
        
        #Obtengo el punto de la interpolacion
        point = geom_line.interpolate(distance)
        
        #inseto el vertice
        res = geom_line.insertVertex(point.asPoint().x(), point.asPoint().y(), 1)
        
        if res:
            
            layer_line.changeGeometry(feat_line.id(), geom_line)
            layer_line.commitChanges()
            return True
        
        layer_line.rollBack()
        return False
    
    def insertSymbolToInicio(self, layer_point_inicio, feat_line, n_nod, ty_sim, z_tn, ty_z):
        
        vertices = feat_line.geometry().asMultiPolyline()[0]
        n_rel = n_nod
        tramo_idtramo = feat_line['gid']
        
        #Si es BRV CALCULO EL ANGULO SINO NO
        if ty_sim == "BRV":
            angulo = self.getAngleVertex1_2(vertices)
        else:
            angulo = 0
        
        #Ya tengo todos los datos
        layer_point_inicio.startEditing()
        
        #creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(layer_point_inicio.fields())
        
        #obtengo los indices de las variables
        idx_n_nodo = layer_point_inicio.fieldNameIndex("n_nod")
        idx_n_rel = layer_point_inicio.fieldNameIndex("n_rel")
        idx_ty_sim = layer_point_inicio.fieldNameIndex("ty_sym")
        idx_z_tn = layer_point_inicio.fieldNameIndex("z_tn")
        idx_ty_z = layer_point_inicio.fieldNameIndex("ty_z")
        idx_tramo_idtramo = layer_point_inicio.fieldNameIndex("tramo_idtramo")
        idx_angulo = layer_point_inicio.fieldNameIndex("angulo")
        
        #Agrego los atributos con su indices
        attrs[idx_n_nodo] = int(n_nod)
        attrs[idx_n_rel] = int(n_rel)
        attrs[idx_ty_sim] = ty_sim
        attrs[idx_z_tn] = float(z_tn)
        attrs[idx_ty_z] = ty_z
        attrs[idx_tramo_idtramo] = tramo_idtramo
        attrs[idx_angulo] = angulo
        
        #creoe l feature para agregar
        feature = QgsFeature()
        
        #elijo el 1er vertice como point
        point = vertices[0]
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes(attrs)
        res = layer_point_inicio.addFeature(feature)
        
        if res:
            
            if layer_point_inicio.commitChanges():
                return True
            else:
                layer_point_inicio.rollBack()
                return False
        else:
            return False
        
    def insertSymbolToFinal(self, layer_point_final, feat_line, n_nod, ty_sim, z_tn, ty_z):
        vertices = feat_line.geometry().asMultiPolyline()[0]
        nodo_final = len(vertices) - 1
        n_rel = n_nod
        tramo_idtramo = feat_line['gid']
        angulo = 0
        
        #Ya tengo todos los datos
        layer_point_final.startEditing()
        
        #creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len(layer_point_final.fields())
        
        #obtengo los indices de las variables
        idx_n_nodo = layer_point_final.fieldNameIndex("n_nod")
        idx_n_rel = layer_point_final.fieldNameIndex("n_rel")
        idx_ty_sim = layer_point_final.fieldNameIndex("ty_sym")
        idx_z_tn = layer_point_final.fieldNameIndex("z_tn")
        idx_ty_z = layer_point_final.fieldNameIndex("ty_z")
        idx_tramo_idtramo = layer_point_final.fieldNameIndex("tramo_idtramo")
        idx_angulo = layer_point_final.fieldNameIndex("angulo")
        
        #Agrego los atributos con su indices
        attrs[idx_n_nodo] = int(n_nod)
        attrs[idx_n_rel] = int(n_rel)
        attrs[idx_ty_sim] = ty_sim
        attrs[idx_z_tn] = float(z_tn)
        attrs[idx_ty_z] = ty_z
        attrs[idx_tramo_idtramo] = tramo_idtramo
        attrs[idx_angulo] = angulo
        
        #creoe l feature para agregar
        feature = QgsFeature()
        
        #elijo el 1er vertice como point
        point = vertices[nodo_final]
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttributes(attrs)
        res = layer_point_final.addFeature(feature)
        
        if res:
            
            if layer_point_final.commitChanges():
                return True
            else:
                layer_point_final.rollBack()
                return False
        else:
            return False
            
    def addAttributesToTramo(self, layer_tramo, feat_linea, tipo, longitud, diametro, material, conforme):
        
        #obtengo el id del tramo
        id_tramo = feat_linea["gid"]
        
        #obtengo los indices de los atributos
        idx_tipo = layer_tramo.fieldNameIndex("tipo")
        idx_longitud = layer_tramo.fieldNameIndex("longitud")
        idx_diametro = layer_tramo.fieldNameIndex("diametro")
        idx_material= layer_tramo.fieldNameIndex("material")
        idx_conforme = layer_tramo.fieldNameIndex("conforme")
        
        attrs = {idx_tipo :  tipo, idx_longitud : longitud, idx_diametro : diametro, idx_material : material, idx_conforme : conforme}
        
        if layer_tramo.dataProvider().changeAttributeValues({ id_tramo : attrs }):
            return True
        else:
            return False
    
    
        
    def getAngleVertex1_2(self, array_vertex):
        
        #Obtengo los dos vertices iniciales
        point1 = array_vertex[0]
        point2 = array_vertex[1]
        
        res = point1.azimuth(point2)
        
        return res
            