# -*- coding: utf-8 -*-


from PyQt4 import QtGui
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import cv2
import os, PIL
from PIL import Image
import sys


class image_summation():
    def __init__(self,imgDir):
        allFiles = os.listdir(imgDir)
        imgPaths = [fileName for fileName in allFiles if  fileName[-4:] in      # read dir contents
                   [".jpg", ".png"]]                                            # only get image files
        w,h = Image.open(os.path.join(imgDir, imgPaths[0])).size                # Assuming all images are same size, get 
                                                                                # dimensions of first image
        numImgs = len(imgPaths)
        arr = np.zeros((h,w,3),np.float)                                        # Create an empty numpy array of floats to store the 
                                                                                # average (assume RGB images)
        for path in imgPaths:
            imgArr = np.array(Image.open(os.path.join(imgDir,path)),            # read an image to numpy array
                              dtype=np.float)
            arr = arr+imgArr/numImgs                                            # add and average
        self.sumImg = np.array(np.round(arr),dtype=np.uint8)                    # Round values in array and cast as 8-bit integer
        #out  = Image.fromarray(self.sumImg,mode="RGB")                          # Generate averaged image
        #out.show()



# class myGUI(pg.GraphicsWindow):
#     def __init__(self, numpyArray):
#         super(myGUI, self).__init__()
#         self.setWindowTitle('pyqtgraph example: ROI Examples')
#         text = """Select your region of interest"""
#         w1 = self.addLayout(row=0, col=0)
#         label1 = w1.addLabel(text, row=0, col=0)

#         v1a = w1.addViewBox(row=1, col=0, lockAspect=True)
#         img1a = pg.ImageItem(numpyArray)
#         v1a.addItem(img1a)
#         v1a.disableAutoRange('xy')
#         v1a.autoRange()

#         v1b = w1.addViewBox(row=2, col=0, lockAspect=True)
#         img1b = pg.ImageItem()
#         v1b.addItem(img1b)
#         v1b.disableAutoRange('xy')
#         v1b.autoRange()

#         roi = (pg.RectROI([50, 50], [50, 50]))

#         def update(roi):
#             img1b.setImage(roi.getArrayRegion(numpyArray, img1a), 
#                            levels=(0, numpyArray.max()))
#             v1b.autoRange()

#         roi.sigRegionChanged.connect(update)
#         v1a.addItem(roi)
#         update(roi)
    

# def main():
#     summerizer = image_summation(imgDir = '/home/josh/google_drive/spring_2015/APIL/foo/')
#     trans = summerizer.sumImg.transpose((1,0,2))                                # y,x,z ==> x,y,z, so we aren't on our side
#     numpyArray = trans[:,::-1,:]                                                # flip the y, so we aren't upside down
#     # app = QtGui.QApplication([])
#     GUI = myGUI(numpyArray)

# ## Start Qt event loop unless running in interactive mode or using pyside.
# if __name__ == '__main__':
#     main()




summerizer = image_summation(imgDir = 
                             '/home/josh/google_drive/spring_2015/APIL/foo/')
trans = summerizer.sumImg.transpose((1,0,2))                                    # y,x,z ==> x,y,z, so we aren't on our side
numpyArray = trans[:,::-1,:]                                                    # flip the y, so we aren't upside down




## create GUI
#app = QtGui.QApplication([])
w = pg.GraphicsWindow(size=(1000,800), border=True)
w.setWindowTitle('pyqtgraph example: ROI Examples')

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
