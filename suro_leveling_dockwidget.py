# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SuroLevelingDockWidget
                                 A QGIS plugin
 todo
                             -------------------
        begin                : 2016-02-12
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Ondřej Pešek
        email                : ondra.lobo@seznam.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon, QDialog, QDialogButtonBox, QFileDialog, QListWidgetItem, QMessageBox
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry
#import resources

import move
#import csv
#from PyQt4.QtGui import *
#from PyQt4.QtCore import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'suro_leveling_dockwidget_base.ui'))


class SuroLevelingDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""

        super(SuroLevelingDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.inputButton.clicked.connect(self.select_input)
        self.outputButton.clicked.connect(self.select_output)
        self.showInput.clicked.connect(self.show_input)
        #self.showInput.clicked.connect(self.show_as_layer(self.input.text())) #***************************************


        self.input.textChanged.connect(self.able_solve) # enable solve button
        self.output.textChanged.connect(self.able_solve)
        self.value.textChanged.connect(self.able_solve)
        self.input.textChanged.connect(self.able_show) # enable showInput button

        self.solve.clicked.connect(self.move_by)

    def select_input(self):
        """select .csv file to edit"""

        self.filePath = QFileDialog.getOpenFileName(self, 'Load file','.', 'Comma Seperated Values (*.csv)')

        if self.filePath:
            self.filePath=os.path.normpath(self.filePath)
        else:
            return

        self.input.setText(self.filePath)
        self.output.setText(self.filePath[:-4]+u'_leveled.csv')

    def select_output(self):
        """choose directory to save returned data"""
        self.outputDir = QFileDialog.getExistingDirectory(self, 'Save to file')
        if not self.outputDir:
            return

        self.directory = os.path.normpath(self.outputDir) + os.path.sep + u'leveled_data.csv'
        self.output.setText(self.directory)

    def able_solve(self):
        """set Solve button enable"""

        if self.input.text() and self.output.text() and self.value.text():
            self.solve.setEnabled(True)
        else:
            self.solve.setEnabled(False)

    def able_show(self):
        """set showInput button enable"""

        if self.input.text():
            self.showInput.setEnabled(True)
        else:
            self.showInput.setEnabled(False)

#************************************************************************************************************
    def show_as_layer(self,filePath):
        """show input csv as layer"""

        uri = "file:" + 3*os.path.sep + filePath + "?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s" % ("EPSG:4326",",", "Lat_deg", "Lon_deg", ".")
        uri = os.path.join(uri).replace('\\','/')
        layerName = filePath.rsplit(os.path.sep,1)
        layerName = layerName[1][:-4]
        layer = QgsVectorLayer(uri, layerName, "delimitedtext")
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def show_input(self):
        """show input csv as layer"""

        uri = "file:" + 3*os.path.sep + self.input.text() + "?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s" % ("EPSG:4326",",", "Lon_deg", "Lat_deg", ".")
        uri = os.path.join(uri).replace('\\','/')
        layerName = self.input.text().rsplit(os.path.sep,1)
        layerName = layerName[1][:-4]
        layer = QgsVectorLayer(uri, layerName, "delimitedtext")
        QgsMapLayerRegistry.instance().addMapLayer(layer)


    def move_by(self):
        """move"""

        move.move_by_points(self.input.text(),self.output.text(),int(self.value.text()))
        uri = "file:" + 3*os.path.sep + self.output.text() + "?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s" % ("EPSG:4326",",", "Lon_deg", "Lat_deg", ".")
        uri = os.path.join(uri).replace('\\','/')
        layerName = self.output.text().rsplit(os.path.sep,1)
        layerName = layerName[1][:-4]
        layer = QgsVectorLayer(uri, layerName, "delimitedtext")
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def close_event(self, event): #closeEvent
        self.closingPlugin.emit()
        event.accept()

