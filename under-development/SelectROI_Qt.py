# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import pyqtgraph as pg
import numpy as np
import cv2
import os, PIL
from PIL import Image
import sys



def sum_images(imgDir):
    allFiles = os.listdir(imgDir)                                        
    imgPaths = [fileName for fileName in allFiles if  fileName[-4:] in          # only get image files
               [".jpg", ".png"]]  
    w,h = Image.open(os.path.join(imgDir, imgPaths[0])).size                    # Assuming all images are same size, get 
                                                                                # dimensions of first image
    numImgs = len(imgPaths)
    arr = np.zeros((h,w,3),np.float)                                            # Create an empty numpy array of floats to store the 
                                                                                # average (assume RGB images)
    for path in imgPaths:
        imgArr = np.array(Image.open(os.path.join(imgDir,path)),                # read an image to numpy array
                          dtype=np.float)
        arr = arr+imgArr/numImgs                                                # add and average
    sumImg = np.array(np.round(arr),dtype=np.uint8)                             # Round values in array and cast as 8-bit integer
    transImg = sumImg.transpose((1,0,2))                                        # y,x,z ==> x,y,z, so we aren't on our side
    # numpyArray = transImg[:,::-1,:]                                           # flip the y, so we aren't upside down
    numpyArray = transImg[:,::-1]                                               # we can leave off the RGB values if we want
    return numpyArray


def update(roi):
    img1b.setImage(roi.getArrayRegion(numpyArray, img1a), 
                   levels=(0, numpyArray.max()))
    v1b.autoRange()


def printCoords():
    left = roi.pos()[0]                                                         # bottom left corner
    bottom = roi.pos()[1]                                                       # bottom left corner
    right = left + roi.size()[0]                                                # left + width
    top = bottom + roi.size()[1]                                                # bottom + height
    coords = [('top', top), ('bottom', bottom), ('left', left), ('right', right)]

    fileName = QtGui.QFileDialog.getSaveFileName(directory = "ROI_config.txt",
                                                 filter = "txt (*.txt *.)")
    with open(fileName, 'a') as f:
        for coord in coords:
            label = str(coord[0])
            value = str(coord[1])
            f.write(label + "\t" + value + "\n")
    app.exit()



if __name__ == '__main__':
    app = QtGui.QApplication([])
    imgDir = str(pg.FileDialog.getExistingDirectory())
    numpyArray = sum_images(imgDir)

    w = QtGui.QWidget()                                                         # make main widget to hold all others
    layout = QtGui.QHBoxLayout()
    w.setLayout(layout)

    w1 = pg.GraphicsWindow()

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

    roi = (pg.RectROI([100, 100], [100, 100]))
    roi.addScaleHandle([0,0],[1,1])
    roi.sigRegionChanged.connect(update)
    v1a.addItem(roi)
    update(roi)

    layout.addWidget(w1)

    btn = QtGui.QPushButton('Save')                                             # make button
    btn.clicked.connect(printCoords)
    layout.addWidget(btn)

    w.setWindowTitle('Select Region of Interest')
    w.show()
    app.exec_()
    


