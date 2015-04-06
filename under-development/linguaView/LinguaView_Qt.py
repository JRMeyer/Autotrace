#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

import os
import sys
from PyQt4 import QtGui, QtCore
# import neutralContour as nc
# import LabelWindow as lw
# import AnalysisWindow as aw

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        center = MainWidget()
        self.setCentralWidget(center)

        imgDir = 'imgDir/'

        exitAction = QtGui.QAction(QtGui.QIcon(imgDir + 'open_file.svg'), 'Open', self)
        exitAction.setShortcut('Ctrl+O')
        exitAction.setStatusTip('Open File(s)')
        exitAction.triggered.connect(center.select_files)

        openAction = QtGui.QAction(QtGui.QIcon(imgDir + 'exit.svg'), 'Exit', self)
        openAction.setShortcut('Ctrl+Q')
        openAction.setStatusTip('Exit application')
        openAction.triggered.connect(self.close)

        vizAction = QtGui.QAction(QtGui.QIcon(imgDir + 'mag_glass.svg'), 'MAG', self)
        vizAction.setShortcut('Ctrl+Q')
        vizAction.setStatusTip('MAG')
        vizAction.triggered.connect(self.close)

        editAction = QtGui.QAction(QtGui.QIcon(imgDir + 'pencil.svg'), 'PEN', self)
        editAction.setShortcut('Ctrl+Q')
        editAction.setStatusTip('PEN')
        editAction.triggered.connect(self.close)

        runAction = QtGui.QAction(QtGui.QIcon(imgDir + 'gears.svg'), 'GEAR', self)
        runAction.setShortcut('Ctrl+Q')
        runAction.setStatusTip('GEAR')
        runAction.triggered.connect(self.close)

        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(exitAction)
        toolbar.addAction(openAction)
        toolbar.addAction(vizAction)
        toolbar.addAction(editAction)
        toolbar.addAction(runAction)
        self.statusBar()

        self.setWindowTitle('Main window')
        self.setGeometry(0, 0, 400, 400)

        self.show()
        
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                               

class MainWidget(QtGui.QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        labelSelectFiles = QtGui.QLabel('Data Files:')
        self.editSelectFiles = QtGui.QTextEdit()
        radio = self.createNonExclusiveGroup()
        btnViz = QtGui.QPushButton('Visualize')

        QtCore.QObject.connect(btnViz, QtCore.SIGNAL("clicked()"), 
                               self.close)

        grid = QtGui.QGridLayout()

        grid.addWidget(labelSelectFiles, 1, 0)
        grid.addWidget(self.editSelectFiles, 2, 0, 1, -1)
        grid.addWidget(radio, 9,0)
        grid.addWidget(btnViz, 10, 0, 1, -1)

        self.setLayout(grid) 
        self.show()
   

    def select_files(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, "Choose File(s)")
        for fileName in fileNames:
            self.editSelectFiles.append(str(fileName))


    def createNonExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("Visualization Options")
        groupBox.setFlat(True)

        checkBox1 = QtGui.QCheckBox("Linguagram")
        checkBox2 = QtGui.QCheckBox("Neutral Contours")
        checkBox3 = QtGui.QCheckBox("Waveform")
        checkBox4 = QtGui.QCheckBox("Spectragram")

        box = QtGui.QGridLayout()
        box.addWidget(checkBox1, 1,0)
        box.addWidget(checkBox2, 1,1)
        box.addWidget(checkBox3, 2,0)
        box.addWidget(checkBox4, 2,1)

        box.setColumnStretch(0, 1)                                              # addStrech is nice for when window size changes
        box.setColumnStretch(1, 1)

        groupBox.setLayout(box)

        return groupBox

def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    
