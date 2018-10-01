from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar


class ClTrdomEntity():
    
    def __init__(self, cl_trdom_layer):
        
        self.layer_cl_trdom = cl_trdom_layer
        
        
    def addSegment(self, feat_parcela, cl_tramo, linea, last_point):
        #Inicio la edicion de cl_trdom
        self.layer_cl_trdom.startEditing()
        gid_parcela = feat_parcela['gid']
        gid_cl_infotd_last = last_point['gid']
        gid_cl_tramo = cl_tramo['gid']
        
        #Obtengo los indice de cada uno de las gid foraneas
        idx_gid_parc =  self.layer_cl_trdom.fieldNameIndex("parcelas_idparcelas")
        idx_gid_cl_infotd =  self.layer_cl_trdom.fieldNameIndex("infotd_clinfotd")
        idx_gid_cl_tramo =  self.layer_cl_trdom.fieldNameIndex("tramos_cltramos")
        idx_length =  self.layer_cl_trdom.fieldNameIndex("longitud")
        
         #creo el arreglo vacion con la dimension de los atributos
        attrs = [None] * len( self.layer_cl_trdom.fields())
        
        #Asigno los valores al arreglo
        
        attrs[idx_gid_parc] = gid_parcela
        attrs[idx_gid_cl_infotd] = gid_cl_infotd_last
        attrs[idx_gid_cl_tramo] = gid_cl_tramo
        attrs[idx_length] = QgsGeometry.fromPolyline(linea).length()
        
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromPolyline(linea))
        feature.setAttributes(attrs)
        
        res = self.layer_cl_trdom.addFeature(feature)
        
        if self.layer_cl_trdom.commitChanges():
            return res
        else:
            self.layer_cl_trdom.rollBack()
            return False
        
    def getLastLineAdded(self):
        
        features = self.layer_cl_trdom.getFeatures()
        last = features.next()
        
        for feat in features:
            last = feat
            
        return last
        
        