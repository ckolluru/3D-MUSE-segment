from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import zarr
import os

class MainWindow(QMainWindow):
	
	def __init__(self):
		
		QMainWindow.__init__(self)

		loadUi("mainwindow.ui",self)

		self.addToolBar(NavigationToolbar(self.Mplwidget.canvas, self))
		self.Mplwidget.canvas.axes.axis('off')
		
		self.intermediateSlices = None
		self.zarr_file = None


	def updatePlotWindow(self, image, overlay = None):

		self.Mplwidget.canvas.axes.clear()
		self.Mplwidget.canvas.axes.imshow(image)
		self.Mplwidget.canvas.draw()
		
		# Overlay is the segmentation masks
		# if overlay is not None:
		# ...
	  
	def openDataset(self):

		title = "Open Zarr dataset directory"
		flags = QFileDialog.ShowDirsOnly
		self.zarr_file = QFileDialog.getExistingDirectory(self,
														title,
														os.path.expanduser("."),
														flags)

		if self.zarr_file == '':
			self.zarr_file = None
			return
		
		# Get the spacing between slices to load in via a dialog box
		# dialog = DatasetInfoDialogBox()
		
		# if dialog.exec_() == QDialog.Accepted:
		# 	z_step = dialog.get_z_spacing()
   
		# dataset = self.zarr_file["muse"]
		# self.intermediateSlices = np.array(dataset[:z_step:, :, :])
		return
	
	def saveModelPredictions(self):
		
		return
	
	def saveTrainedModel(self):
		
		return
	
	def saveUserAnnotations(self):
		
		return
	
	def saveUserCorrections(self):
		
		return

	def lowEdit(self):
    
		lowValue = int(self.lowLineEdit.text())
		return
		
if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()