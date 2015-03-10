#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
FileRename.py
Josh Meyer - March 2015 PyQt4
Gus Hahn-Powell - March 6 2014 gtk
Jeff Berry - 2011

purpose:
    assists the user in adding experiment, 
    subject and tracer information to files
    
usage:
    python FileRename.py

image files...
<study-name>_<subject-id>_<item-name>_<frame-number>.<image-extension>

if a trace file...
<study-name>_<subject-id>_<item-name>_<frame-number>.<image-extension>.
                                                 <tracer-id>_traced.txt      
'''


import sys
import os
from PyQt4 import QtGui, QtCore


class Renamer(QtGui.QWidget):
    def __init__(self):
        super(Renamer, self).__init__()
        self.initUI()
        
    def initUI(self):
        selectFiles = QtGui.QLabel('Select Files:')                             # initialize all widgets
        btnSource = QtGui.QPushButton('Open')
        self.selectFilesEdit = QtGui.QLineEdit()
        saveTo = QtGui.QLabel('Save To:')
        btnDest = QtGui.QPushButton('Open')
        self.saveToEdit = QtGui.QLineEdit()
        studyCode = QtGui.QLabel('Study Code:')
        studyCodeEdit = QtGui.QLineEdit()   
        subNum = QtGui.QLabel('Subject Number:')
        subNumEdit = QtGui.QLineEdit()   
        item = QtGui.QLabel('Item:')
        itemEdit = QtGui.QLineEdit()   
        tracer = QtGui.QLabel('Tracer:')
        tracerEdit = QtGui.QLineEdit() 
        btnOK = QtGui.QPushButton('OK')
        grid = QtGui.QGridLayout()

        grid.addWidget(selectFiles, 1, 0)
        grid.addWidget(btnSource, 1, 2)
        grid.addWidget(self.selectFilesEdit, 2, 0, 1, -1)
        QtCore.QObject.connect(btnSource, QtCore.SIGNAL("clicked()"), 
                               self.choose_source)
        
        grid.addWidget(saveTo, 3, 0)
        grid.addWidget(btnDest, 3, 2)
        grid.addWidget(self.saveToEdit, 4, 0, 1, -1)
        QtCore.QObject.connect(btnDest, QtCore.SIGNAL("clicked()"), 
                               self.choose_dest)

        grid.addWidget(studyCode, 5, 0)
        grid.addWidget(studyCodeEdit, 5, 1, 1, -1)

        grid.addWidget(subNum, 6, 0)
        grid.addWidget(subNumEdit, 6, 1, 1, -1)

        grid.addWidget(item, 7, 0)
        grid.addWidget(itemEdit, 7, 1, 1, -1)

        grid.addWidget(tracer, 8, 0)
        grid.addWidget(tracerEdit, 8, 1, 1, -1)

        grid.addWidget(btnOK, 9, 0, 1, -1)

        self.setLayout(grid) 
        self.setGeometry(0, 0, 400, 300)
        self.setWindowTitle('File Renamer')    
        self.show()
   
    def choose_source(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, "Open File(s)")
        self.selectFilesEdit.setText(os.path.dirname(str(fileNames[0])))

    def choose_dest(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "Save To")
        self.saveToEdit.setText(str(dirName))

     
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Renamer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
