from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

from ClDirectionEntity import ClDirectionEntity

class DirectionChange():

    def __init__(self, iface, toolbar):
        self.iface = iface
        self.toolbar = toolbar
        self.canvas = self.iface.mapCanvas()

        # Create actions
        self.direction_change = QAction(QIcon(":/plugins/AGCloacas/dir_change.png"),
                                        QCoreApplication.translate("AG_Cloacas", "Cambiar Sentido"),
                                        self.iface.mainWindow())

        self.direction_change.setCheckable(True)

        # Connect to signals for button behaviour
        self.direction_change.triggered.connect(self.direction_change_action)

        # Add actions to the toolbar
        self.toolbar.addAction(self.direction_change)


    def direction_change_action(self):
        if self.direction_change.isChecked():
            res_dialog = self.showdialog()


            if (res_dialog == 1):

                try:

                    layer_cl_direction = QgsMapLayerRegistry.instance().mapLayersByName('cl_direction')[0]

                    # instanciio las clases e inicializo
                    cl_direction_entity = ClDirectionEntity()
                    cl_direction_entity.initialize(layer_cl_direction)

                    try:
                        layer_dir_selected = layer_cl_direction.selectedFeatures()

                        if (len(layer_dir_selected) >= 1):

                            dir_selected = layer_cl_direction.selectedFeatures()[0]

                            if cl_direction_entity.changeDirection(dir_selected):
                                pass

                                #instanciar la clase de CLTRAMOS_ENTITY


                        else:
                            self.iface.messageBar().pushMessage("Error", "Seleccione una Direccion",
                                                                level=QgsMessageBar.WARNING)


                    except(IndexError):
                        self.iface.messageBar().pushMessage("Error", "Seleccione una Direccion",
                                                            level=QgsMessageBar.WARNING)

                except (IndexError):
                    self.iface.messageBar().pushMessage("Error", "Debe cargar la capa 'cl_direction'", level=QgsMessageBar.CRITICAL)
                    self.direction_change.setChecked(False)
            self.direction_change.setChecked(False)




    def showdialog(self):
        """msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)

        msg.setText("Insertar CL_NODO?")
        msg.setWindowTitle("Insertar CL_NODOS")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()"""

        retval = QMessageBox.question(self.iface.mainWindow(),
                                      "Question", "Cambiar Direccion?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        val = None

        if retval == QMessageBox.Yes:

            val = 1
        else:
            val = 0

        return val
