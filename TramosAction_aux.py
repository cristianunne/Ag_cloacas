from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from TramosAction_dialog import TramosActionDialog
from Symbol_inicio_tramos_dialog import Symbol_inicioTramosDialog
from Nodo_Final_Tramo import NodoFinalTramosDialog
from Symbol_final_tramos_dialog import Symbol_finalTramosDialog
from Resumen_Final_Tramo_Dialog import ResumenFinalTramosDialog
from TramosActionTool import TramosActionTool
from CotasTool import CotasTool
from NodosTool import NodosTool

from _ast import Pass


class TramosAction():
    
    def __init__(self, iface, toolbar):
        
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()
        
        self.tramosactiontool = TramosActionTool(iface, toolbar)
        
        #Llamo a las clases de los Formularios
        self.dlg_tramos = TramosActionDialog()
        self.dlg_symbol_inicio = Symbol_inicioTramosDialog()
        self.dlg_nodo_final = NodoFinalTramosDialog()
        self.dlg_symbol_final = Symbol_finalTramosDialog()
        self.dlg_resumen_final = ResumenFinalTramosDialog()
        self.cotas_tool = CotasTool(iface, toolbar)
        self.nodos_tool = NodosTool(iface, toolbar)
        
        self.result = False
        
        # Create actions 
        self.tramos = QAction(QIcon(":/plugins/AGCloacas/polilinea.png"),  QCoreApplication.translate("AG_Cloacas", "Agregar Propieades al Tramo"),  self.iface.mainWindow())
            
        self.tramos.setCheckable(True)
        
         # Connect to signals for button behaviour
        self.tramos.triggered.connect(self.action_tramos)
        
        # Add actions to the toolbar
        self.toolbar.addAction(self.tramos)
        
        
        self.dlg_symbol_inicio.rb_inicio_pld.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_des.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_cal.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_brv.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_brs.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_ese.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_brh.clicked.connect(self.setEnabled)
        self.dlg_symbol_inicio.rb_inicio_til.clicked.connect(self.setEnabled)
        
        self.dlg_symbol_final.rb_final_pld.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_des.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_cal.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_brv.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_brs.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_ese.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_brh.clicked.connect(self.setEnabledFinal)
        self.dlg_symbol_final.rb_final_til.clicked.connect(self.setEnabledFinal)

        
       
        
    def action_tramos(self):
        
        #CERO LAS VARIABLES QUE GUARDAN LOS DATOS
        n_nodo_inicial = None
        tipo_z_inicial = None
        ztn_inicial = None
        tipo_simbol_inicio = None
        
        n_nodo_final = None
        tipo_z_final = None
        ztn_final = None
        tipo_simbol_final = None
        longitud_linea = None
        
        nro_conforme = None
        cota_cano_inicio = None
        cota_cano_final = None
        diametro = None
        cb_tipo_tramo = None
        #evaluo que el currentlayer sea cl_tramos 
        
        self.deactivate()
        self.restoreEnabled()
        self.resetAll()
        
        #layer = self.canvas.currentLayer()
        #self.dlg_tramos.ok.setEnabled(False)
        #Verifico que la capa Tramos este cargada
        
        if self.tramos.isChecked():
            
            try:
    
                layer_cl_tramos = QgsMapLayerRegistry.instance().mapLayersByName('cl_tramos')[0]
                layer_cl_nodo_tr_inicial = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodo_tr_inicial')[0]
                layer_cl_nodo_tr_final = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodo_tr_final')[0]
                layer_cl_cotas = QgsMapLayerRegistry.instance().mapLayersByName('cl_cotas')[0]
                layer_cl_nodos = QgsMapLayerRegistry.instance().mapLayersByName('cl_nodos')[0]
                
                #verifico que haya al menos un elemento seleccionado
                layer_select_tramo = layer_cl_tramos.selectedFeatures()
                
                if(len(layer_select_tramo) >= 1):
                    #guardo solo el elemento 1 de la seleccion
                    tramo_select = layer_select_tramo[0]
                    
                    #PRIMERO VERIFICO QUE NO HAYA NINGUN TIPO DE DATOS CARGADOS EN EL TRAMO
                    if self.verifiedTramo(layer_cl_nodo_tr_inicial, layer_cl_nodo_tr_final, tramo_select) == False:
                
                        res = self.dlg_tramos.exec_()
                        if res == 1:
                            #Guardo las Variables
                            n_nodo_inicial = self.dlg_tramos.n_nodo_inicial.text()
                            tipo_z_inicial = self.dlg_tramos.tipo_z_inicial.currentText()
                            ztn_inicial = self.dlg_tramos.ztn_inicial.text()
                            
                            res_2 = self.dlg_symbol_inicio.exec_()
                            
                            if res_2 == 1:
                                
                                tipo_simbol_inicio = self.optioninicioChecked()
                                
                                res_3 = self.dlg_nodo_final.exec_()
                                
                                if res_3 == 1:
                                    n_nodo_final = self.dlg_nodo_final.n_nodo_final.text()
                                    tipo_z_final = self.dlg_nodo_final.tipo_z_final.currentText()
                                    ztn_final = self.dlg_nodo_final.ztn_final.text()
                        
                                    res4 = self.dlg_symbol_final.exec_()
                                    if res4 == 1:
                                        tipo_simbol_final = self.optionCheckedFinal()
                                        
                                        #seteo los textos que ya tengo en el dlg.resumen
                                        id_tr = str(tramo_select['gid'])
                                        
                                        longitud_linea = tramo_select.geometry().length()
                                        
                                        self.setInfoResumenFinal(id_tr, n_nodo_inicial, n_nodo_final, tipo_simbol_inicio, tipo_simbol_final, longitud_linea)
                                        
                                        res5 = self.dlg_resumen_final.exec_()
                                        
                                        if (res5 == 1):
                                            
                                            #obtengo el material
                                            tipo_material = self.optionResumenChecked()
                                            nro_conforme =  self.dlg_resumen_final.nro_conforme.text()
                                            cota_cano_inicio = self.dlg_resumen_final.cota_cano_inicio.text()
                                            cota_cano_final = self.dlg_resumen_final.cota_cano_final.text()
                                            diametro = self.dlg_resumen_final.diametro.text()
                                            cb_tipo_tramo = self.dlg_resumen_final.cb_tipo_tramo.currentText()
                                            
                                            if self.dlg_symbol_inicio.rb_inicio_brv.isChecked():
                                                #agrego el vertice
                                                if self.tramosactiontool.addVertexToLine(layer_cl_tramos, tramo_select):
                                                    #inserto el vertice avanzp
                                                    if self.tramosactiontool.insertSymbolToInicio(layer_cl_nodo_tr_inicial, tramo_select, n_nodo_inicial, tipo_simbol_inicio, ztn_inicial, tipo_z_inicial):
                                                        res_ = self.tramosactiontool.insertSymbolToFinal(layer_cl_nodo_tr_final, tramo_select, n_nodo_final, tipo_simbol_final, ztn_final, tipo_z_final)
                                                        
                                                        if res_:
                                                            #inserto los atributos del tramo
                                                            res_attr = self.tramosactiontool.addAttributesToTramo(layer_cl_tramos, tramo_select, cb_tipo_tramo, longitud_linea, diametro, tipo_material, nro_conforme)
                                                            
                                                            if res_attr:
                                                                if self.cotas_tool.insertCota(layer_cl_cotas, tramo_select, cota_cano_inicio, cota_cano_final):
                                                                    if self.nodos_tool.createNodos(layer_cl_nodos, tramo_select):
                                                                        self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)
                                                
                                            elif self.dlg_symbol_inicio.rb_inicio_brs.isChecked():
                                                    #inserto el vertice avanzp
                                                    if self.tramosactiontool.insertSymbolToInicio(layer_cl_nodo_tr_inicial, tramo_select, n_nodo_inicial, tipo_simbol_inicio, ztn_inicial, tipo_z_inicial):
                                                        res_ = self.tramosactiontool.insertSymbolToFinal(layer_cl_nodo_tr_final, tramo_select, n_nodo_final, tipo_simbol_final, ztn_final, tipo_z_final)
                                                        if res_:
                                                            #inserto los atributos del tramo
                                                            res_attr = self.tramosactiontool.addAttributesToTramo(layer_cl_tramos, tramo_select, cb_tipo_tramo, longitud_linea, diametro, tipo_material, nro_conforme)
                                                            if res_attr:
                                                                if self.cotas_tool.insertCota(layer_cl_cotas, tramo_select, cota_cano_inicio, cota_cano_final):
                                                                    if self.nodos_tool.createNodos(layer_cl_nodos, tramo_select):
                                                                        self.iface.messageBar().pushMessage("Resultado: ", "Proceso Exitoso!", level=QgsMessageBar.INFO)
                                                
                                            
                                            #print(tipo_material + "\n" + nro_conforme + "\n" + cota_cano_inicio + "\n" + diametro + "\n" + cb_tipo_tramo)
                                            
                                            
                                        
                                        #YA TENGO GUARDADA TODAS LAS VARIABLES
                                    
                    
                  
                    else:
                        self.iface.messageBar().pushMessage("Error", "Ya existen Propiedades Agregadas. Borrelos e intente nuevamente!", level=QgsMessageBar.CRITICAL)
                else:
                     self.iface.messageBar().pushMessage("Error", "Seleccione un Tramo", level=QgsMessageBar.WARNING)
                
                self.tramos.setChecked(False)
                
            except (IndexError):
                self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_tramos', 'cl_nodo_tr_inicial', 'cl_nodo_tr_final'", level=QgsMessageBar.CRITICAL)
                self.tramos.setChecked(False)
            
            
            
                    
            
        else:
            self.deactivate()
            self.unsetTool()
        
    
    def setEnabled(self):
        self.dlg_symbol_inicio.ok.setEnabled(True)
    
    def setEnabledFinal(self):
        self.dlg_symbol_final.ok.setEnabled(True)
        
    def activate(self):
        pass
        

    def verifiedTramo(self, layer_cl_nodo_tr_inicial, layer_cl_nodo_tr_final, tramo_select):
        
        id_tramo = tramo_select["gid"]
        
        res = False
        #obtengo el iterador de nodo_inicial
        cl_nodo_ini_iter = layer_cl_nodo_tr_inicial.getFeatures()
        
        for feat in cl_nodo_ini_iter:
            if feat["tramo_idtramo"] == id_tramo:
                res = True
        
        
        cl_nodo_fin_iter = layer_cl_nodo_tr_final.getFeatures()
        
        for feat in cl_nodo_fin_iter:
            if feat["tramo_idtramo"] == id_tramo:
                res = True
        
        
        return res
        
    def deactivate(self):
        
        self.dlg_symbol_inicio.rb_inicio_pld.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_pld.repaint()
        self.dlg_symbol_inicio.rb_inicio_des.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_cal.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brv.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brs.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_ese.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_brh.setChecked(False)
        self.dlg_symbol_inicio.rb_inicio_til.setChecked(False)
        self.dlg_symbol_inicio.ok.setEnabled(False)
        self.dlg_symbol_final.ok.setEnabled(False)
        
    def optioninicioChecked(self):
        
        if self.dlg_symbol_inicio.rb_inicio_brv.isChecked():
            
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(False)
            
            return self.dlg_symbol_inicio.rb_inicio_brv.text()
        
        elif self.dlg_symbol_inicio.rb_inicio_brs.isChecked():
            self.dlg_symbol_final.rb_final_pld.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_cal.setEnabled(False)
            self.dlg_symbol_final.rb_final_des.setEnabled(False)
            self.dlg_symbol_final.rb_final_brv.setEnabled(False)
            self.dlg_symbol_final.rb_final_ese.setEnabled(False)
            self.dlg_symbol_final.rb_final_brh.setEnabled(False)
            return self.dlg_symbol_inicio.rb_inicio_brs.text()
    
    def optionCheckedFinal(self):
        if self.dlg_symbol_final.rb_final_brs.isChecked():
            return self.dlg_symbol_final.rb_final_brs.text()
          

    def optionResumenChecked(self):
        if self.dlg_resumen_final.br_sd.isChecked():
            return self.dlg_resumen_final.br_sd.text()
        elif self.dlg_resumen_final.br_pvc.isChecked():
            return self.dlg_resumen_final.br_pvc.text()
        elif self.dlg_resumen_final.br_ff.isChecked():
            return self.dlg_resumen_final.br_ff.text()
        elif self.dlg_resumen_final.br_fg.isChecked():
            return self.dlg_resumen_final.br_fg.text()
        elif self.dlg_resumen_final.br_fd.isChecked():
            return self.dlg_resumen_final.br_fd.text()
        elif self.dlg_resumen_final.br_ha.isChecked():
            return self.dlg_resumen_final.br_ha.text()
        elif self.dlg_resumen_final.br_hc.isChecked():
            return self.dlg_resumen_final.br_hc.text()
        elif self.dlg_resumen_final.br_hs.isChecked():
            return self.dlg_resumen_final.br_hs.text()
        elif self.dlg_resumen_final.br_a.isChecked():
            return self.dlg_resumen_final.br_a.text()
        elif self.dlg_resumen_final.br_ac.isChecked():
            return self.dlg_resumen_final.br_ac.text()
        elif self.dlg_resumen_final.br_vi.isChecked():
            return self.dlg_resumen_final.br_vi.text()
        elif self.dlg_resumen_final.br_pe.isChecked():
            return self.dlg_resumen_final.br_pe.text()
        elif self.dlg_resumen_final.br_pead.isChecked():
            return self.dlg_resumen_final.br_pead.text()
        elif self.dlg_resumen_final.br_pp.isChecked():
            return self.dlg_resumen_final.br_pp.text()
        elif self.dlg_resumen_final.br_mam.isChecked():
            return self.dlg_resumen_final.br_mam.text()
    
    def restoreEnabled(self):
        self.dlg_symbol_final.rb_final_pld.setEnabled(True)
        self.dlg_symbol_final.rb_final_des.setEnabled(True)
        self.dlg_symbol_final.rb_final_cal.setEnabled(True)
        self.dlg_symbol_final.rb_final_des.setEnabled(True)
        self.dlg_symbol_final.rb_final_brv.setEnabled(True)
        self.dlg_symbol_final.rb_final_ese.setEnabled(True)
        self.dlg_symbol_final.rb_final_brh.setEnabled(True)
        self.dlg_symbol_final.rb_final_brs.setEnabled(True)
        self.dlg_symbol_final.rb_final_til.setEnabled(True)
        
    def setInfoResumenFinal(self, id_tramo, nro_rel_inicio, nro_rel_final, tipo_sim_inicio, tipo_sim_final, longitud_linea):
        
        self.dlg_resumen_final.id_tramo_text.setText(id_tramo)
        self.dlg_resumen_final.nro_rel_inicio.setText(nro_rel_inicio)
        self.dlg_resumen_final.nro_rel_final.setText(nro_rel_final)
        self.dlg_resumen_final.tipo_sim_inicio.setText(tipo_sim_inicio)
        self.dlg_resumen_final.tipo_sim_final.setText(tipo_sim_final)
        self.dlg_resumen_final.longitud_linea.setText(str(longitud_linea))
        
    def resetAll(self):
        
        self.dlg_tramos.n_nodo_inicial.clear() 
        self.dlg_tramos.ztn_inicial.clear()
        
        self.dlg_tramos.tipo_z_inicial.setCurrentIndex(0)
        self.dlg_nodo_final.n_nodo_final.clear()
        self.dlg_nodo_final.ztn_final.clear()
        self.dlg_nodo_final.tipo_z_final.setCurrentIndex(0)
        
        self.dlg_resumen_final.nro_conforme.clear()
        self.dlg_resumen_final.cota_cano_inicio.clear()
        self.dlg_resumen_final.cota_cano_final.clear()
        self.dlg_resumen_final.diametro.clear()
        
        
        