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
import csv

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal, QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon, QDialog, QDialogButtonBox, QFileDialog, QListWidgetItem, QMessageBox
import resources

#***************************************************************************************************************
#import move

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

        self.input.textChanged.connect(self.ablesolve) # enable of Solve button
        self.output.textChanged.connect(self.ablesolve)
        self.value.textChanged.connect(self.ablesolve)
        #***************************************************************************************************
        #self.solve.clicked.connect(move.move_by_points)

    def select_input(self):
        """select .csv file to edit"""

        self.filepath = QFileDialog.getOpenFileName(self, 'Load file','.', 'Comma Seperated Values (*.csv)')

        if not self.filepath:
            return

        self.input.setText(self.filepath)
        self.output.setText(self.filepath[:-4]+u'_leveled.csv')

    def select_output(self):
        """choose directory to save returned data"""

        self.directory = QFileDialog.getExistingDirectory(self, 'Save to file') + u'\leveled_data.csv'
        if not self.directory:
            return

        self.output.setText(self.directory) #** divna lomitka * musi se zmenit na jmeno souboru ***********************

    def ablesolve(self):
        """set Solve button enable"""

        if self.input.text() and self.output.text() and self.value.text():
            self.solve.setEnabled(True)
        else:
            self.solve.setEnabled(False)


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

