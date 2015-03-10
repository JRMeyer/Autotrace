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
from PyQt4 import QtGui, QtCore


class Renamer(QtGui.QWidget):
    def __init__(self):
        super(Renamer, self).__init__()
        self.initUI()
        
    def initUI(self):
        selectFiles = QtGui.QLabel('Select Files:')                             # initialize all widgets
        btnSource = QtGui.QPushButton('Open')
        selectFilesEdit = QtGui.QLineEdit()
        saveTo = QtGui.QLabel('Save To:')
        btnDest = QtGui.QPushButton('Open')
        saveToEdit = QtGui.QLineEdit()
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
        grid.addWidget(selectFilesEdit, 2, 0, 1, -1)
        QtCore.QObject.connect(btnSource, QtCore.SIGNAL("clicked()"), 
                               self.choose_source)
        
        grid.addWidget(saveTo, 3, 0)
        grid.addWidget(btnDest, 3, 2)
        grid.addWidget(saveToEdit, 4, 0, 1, -1)
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
        fileName = QtGui.QFileDialog.getOpenFileNames(self, "Open File(s)")
        for file in fileName:
            print file

    def choose_dest(self):
        fileName = QtGui.QFileDialog.getOpenFileNames(self, "Save To")
          
     
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Renamer()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



        
    # def onOK(self, event):
    #     studycode = self.studycodeentry.get_text() 
    #     subjnum = self.subjnumentry.get_text() 
    #     item = self.tracerentry.get_text() if self.tracerentry.get_text() else "??"
    #     tracer = self.tracerentry.get_text()
    #     logfile = open(self.dstpath+'log.txt', 'w')
    #     for i in self.srcfilelist:
    #         shortname = os.path.basename(i)
    #         image_extension = re.search(image_extension_pattern, i).group(1)
    #         extension = "traced.txt" if "traced.txt" in shortname else image_extension
    #         print "shortname: {0}\textension: {1}".format(shortname, extension) #debug
    #         itemname = shortname.split('_')[2] if (shortname.count("_") >= 3) else item
    #         framenumber = re.search(frame_number_pattern, shortname).group(1)
    #         #make basic filename and image name...
    #         print "studycode: {0}".format(studycode) #debug
    #         print "subjnum: {0}".format(subjnum) #debug
    #         print "itemname: {0}".format(itemname) #debug
    #         print "framenumber: {0}".format(framenumber) #debug
    #         f_basename = str(studycode) + "_" + str(subjnum) + "_" + itemname + "_" + framenumber
    #         image_name = f_basename + image_extension
    #         #see if this is a trace file...
    #         if extension == "traced.txt":
    #             #if tracer isn't specified, find appropriate tracer...
    #             tracer = self.tracerentry.get_text() if self.tracerentry.get_text() else re.search(tracer_pattern, shortname).group(1).upper()
    #             traced = '.' + tracer + '.' + extension
    #         else:
    #             traced = ""
    #         #make new file name...
    #         dstname = self.dstpath + image_name + traced
    #         print 'renaming', i, '->', dstname 
    #         logfile.write('%s -> %s\n' %(i, dstname))
    #         cmd = ['cp', i, dstname]
    #         p = subprocess.Popen(cmd)
    #         p.wait()
    #     logfile.close()
    #     print "log file saved to", self.dstpath+'log.txt'
    #     print "done"
    #     gtk.main_quit()

# if __name__ == "__main__":
#     main()    
