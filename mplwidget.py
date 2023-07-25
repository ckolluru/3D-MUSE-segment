from PyQt5 import QtWidgets
from PyQt5.QtWidgets import*
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

    
class Mplwidget(QWidget):
    
    def __init__(self, parent = None):

        # Inherit from QWidget
        QWidget.__init__(self, parent)
        
        # Create canvas object
        #self.canvas = MplCanvas()
        self.canvas = FigureCanvas(Figure())
        
        # Set box for plotting
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

# class MplCanvas(Canvas):
#     def __init__(self):
#         self.fig = Figure()
#         self.ax = self.fig.add_subplot(111)
#         Canvas.__init__(self, self.fig)
#         Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
#         Canvas.updateGeometry(self)