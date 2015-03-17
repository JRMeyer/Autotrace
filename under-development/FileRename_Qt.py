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

This file renamer expects the format of the source files to be 

      <name>_<frame>.jpg

<name> can be a combination of letters and numbers, and <frame> is numbers.

The program will split on the underscore, so if filenames are not in this format
the behavior will be unpredictable.

'''


import sys
import os
from PyQt4 import QtGui, QtCore
import shutil

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
        self.studyCodeEdit = QtGui.QLineEdit()   
        subNum = QtGui.QLabel('Subject Number:')
        self.subNumEdit = QtGui.QLineEdit()   
        item = QtGui.QLabel('Item:')
        self.itemEdit = QtGui.QLineEdit()   
        tracer = QtGui.QLabel('Tracer:')
        self.tracerEdit = QtGui.QLineEdit() 
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
        grid.addWidget(self.studyCodeEdit, 5, 1, 1, -1)

        grid.addWidget(subNum, 6, 0)
        grid.addWidget(self.subNumEdit, 6, 1, 1, -1)

        grid.addWidget(item, 7, 0)
        grid.addWidget(self.itemEdit, 7, 1, 1, -1)

        grid.addWidget(tracer, 8, 0)
        grid.addWidget(self.tracerEdit, 8, 1, 1, -1)

        grid.addWidget(btnOK, 9, 0, 1, -1)
        QtCore.QObject.connect(btnOK, QtCore.SIGNAL("clicked()"), 
                               self.rename)

        self.setLayout(grid) 
        self.setGeometry(0, 0, 400, 300)
        self.setWindowTitle('File Renamer')    
        self.show()
   
    def choose_source(self):
        fileNames = QtGui.QFileDialog.getOpenFileNames(self, "Open File(s)")
        self.selectFilesEdit.setText(os.path.dirname(str(fileNames[0])))
        self.origNames = fileNames

    def choose_dest(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self, "Save To")
        self.saveToEdit.setText(str(dirName))

    def rename(self):
        images=[]
        traces=[]
        for name in self.origNames:
            name = str(name)
            if ".txt" in name:
                traces.append(name)
            else:
                images.append(name)

        for origName in images:
            base, ext = os.path.splitext(os.path.basename(origName))
            frameNum = base.split("_")[1]                                       # assumes the orig filename format as aforementioned
            newName =(self.saveToEdit.text() +"/"+                              # /new/directory/
                   self.studyCodeEdit.text() +"_"+                              # <study-name>_ 
                   self.subNumEdit.text() +"_"+                                 # <subject-id>_
                   self.itemEdit.text()+"_"+                                    # <item-name>_
                   frameNum +                                                   # <frame-number>.
                   ext)                                                         # <image-extension>
            shutil.copy(origName, newName)

        for origName in traces:
            base, ext = os.path.splitext(os.path.basename(origName))   
            frameNum = (base.split("_")[1]).split(".")[0]
            imgExt = (base.split("_")[1]).split(".")[1]
            
            newName = (self.saveToEdit.text() +"/"+                             # /new/directory/
                   self.studyCodeEdit.text() +"_"+                              # <study-name>_ 
                   self.subNumEdit.text() +"_"+                                 # <subject-id>_
                   self.itemEdit.text()+"_"+                                    # <item-name>_
                   frameNum +"."+                                               # <frame-number>.
                   imgExt +"."+                                                 # <image-extension>.
                   self.tracerEdit.text() +"_"+                                 # <tracer-id>_
                   "traced." +                                                  # traced.
                   "txt")                                                       # txt
            shutil.copy(origName, newName)

        quit_msg = "You should find your renamed files in the specified folder"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                                           quit_msg, QtGui.QMessageBox.Ok)

    def closeEvent(self, event):

        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
                                                 
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Renamer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
