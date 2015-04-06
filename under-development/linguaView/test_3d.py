# -*- coding: utf-8 -*-
"""
This example demonstrates the use of GLSurfacePlotItem.
"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

## Create a GL View widget to display data
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('GLSurfacePlot')
# w.setCameraPosition(distance=20)

## Add a grid to the view
g = gl.GLGridItem()
g.setSize(50,50,100)
w.addItem(g)

z = pg.gaussianFilter(np.random.normal(size=(50,50)), (1,1))
p1 = gl.GLSurfacePlotItem(z=z, shader='shaded', color=(0.5, 0.5, 1, 1))
# p1.scale(8./20., 8./20., 1.0)
# p1.translate(-18, 2, 0)
w.addItem(p1)




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    QtGui.QApplication.instance().exec_()
