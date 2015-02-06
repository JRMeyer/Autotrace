#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import os
import cv2
import sys
import numpy
from PyQt4 import QtGui


class ROI_selector(QtGui.QMainWindow):
    def __init__(self):
        super(ROI_selector, self).__init__()
        self.selectImages()
        self.getSumImage()
    
    def selectImages(self):
        self.datafiles = QtGui.QFileDialog.getOpenFileNames(self,
                "Select file(s) to open",
                "/home",
                "Images (*.png *.xpm *.jpg)")
        self.pathToFiles = os.path.dirname(str(self.datafiles[0]))
        self.csize = cv2.imread(str(self.datafiles[0])).shape[:2] # get just the x,y lengths out of the x,y,z that is returned by numpy.ndarray.shape

    def getSumImage(self):
	 	sum_img = numpy.zeros(self.csize)
	 	for i in self.datafiles:
	 		img = cv2.imread(str(i))   
	 		tmp = numpy.zeros(self.csize)
	 		tmp += img
	 		sum_img += tmp 
	 	sum_img = sum_img/len(self.datafiles)
	 	cv2.imwrite(self.pathToFiles + 'SumImage.png', cv.imshow(sum_img))   
def main():
    app = QtGui.QApplication(sys.argv)
    roi = ROI_selector()
    roi.destroy()
    sys.exit()


if __name__ == '__main__':
    main()