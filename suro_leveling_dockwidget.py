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

from move import Move, MoveError
import show_as_layer
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

        self.input.textChanged.connect(self.able_solve) # enable solve button
        self.output.textChanged.connect(self.able_solve)
        self.value.textChanged.connect(self.able_solve)
        self.input.textChanged.connect(self.able_show) # enable showInput button

        self.solve.clicked.connect(self.move_by)

    def select_input(self):
        """select csv file to edit"""

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

    def show_input(self):
        """show input csv as layer"""

        show_as_layer.show(self.input.text())

    def move_by(self):
        """move"""
        try:
            move = Move(self.input.text(),self.output.text())
        except IOError as e:
            QMessageBox.critical(None, "Error", "{0}".format(e), QMessageBox.Abort)
            return

        try:
            if self.units.currentText() == 'values':
                try:
                    move.by_points(int(self.value.text()))
                except ValueError as e:
                    QMessageBox.critical(None, "ERROR: Invalid number of values", "{0}".format(e), QMessageBox.Abort)
                    return

            elif self.units.currentText() == 'meters':
                try:
                    move.by_distance(float(self.value.text()))
                except ValueError as e:
                    QMessageBox.critical(None, "ERROR: Invalid number of values", "{0}".format(e), QMessageBox.Abort)
                    return
        except MoveError as e:
            QMessageBox.critical(None, "Error", "{0}".format(e), QMessageBox.Abort)
            return

        show_as_layer.show(self.output.text())

    def close_event(self, event): #closeEvent
        self.closingPlugin.emit()
        event.accept()

