# -*- coding: utf-8 -*-


from PyQt4 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import cv2

fileName = '/home/josh/google_drive/spring_2015/APIL/foo/20110518JF_0215.jpg'

## create GUI
app = QtGui.QApplication([])
w = pg.GraphicsWindow(size=(1000,800), border=True)
w.setWindowTitle('pyqtgraph example: ROI Examples')

numpyArray = cv2.imread(fileName)
print type(numpyArray)
print numpyArray.shape
trans = numpyArray.transpose((1,0,2))                                           # y,x,z ==> x,y,z, so we aren't on our side
numpyArray=trans[:,::-1,:]                                                        # flip the y, so we aren't upside down

text = """Select your region of interest"""
w1 = w.addLayout(row=0, col=0)
label1 = w1.addLabel(text, row=0, col=0)

v1a = w1.addViewBox(row=1, col=0, lockAspect=True)
img1a = pg.ImageItem(numpyArray)
v1a.addItem(img1a)
v1a.disableAutoRange('xy')
v1a.autoRange()


v1b = w1.addViewBox(row=2, col=0, lockAspect=True)
img1b = pg.ImageItem()
v1b.addItem(img1b)
v1b.disableAutoRange('xy')
v1b.autoRange()

roi = (pg.RectROI([50, 50], [50, 50]))


def update(roi):
    img1b.setImage(roi.getArrayRegion(numpyArray, img1a), 
                   levels=(0, numpyArray.max()))
    v1b.autoRange()
    

roi.sigRegionChanged.connect(update)
v1a.addItem(roi)

update(roi)
    


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
