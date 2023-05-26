from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
     
class MPLWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("mainwindow.ui",self)
        self.setWindowTitle("SBFpreprocess v1.0")
        self.addToolBar(NavigationToolbar(self.MatplotlibWidget.canvas, self))


    def update_graph(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MatplotlibWidget.canvas.axes.clear()
        self.MatplotlibWidget.canvas.axes.plot(t, cosinus_signal)
        self.MatplotlibWidget.canvas.axes.plot(t, sinus_signal)
        self.MatplotlibWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MatplotlibWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MatplotlibWidget.canvas.draw()
        

app = QApplication([])
window = MPLWidget()
window.show()
app.exec_()