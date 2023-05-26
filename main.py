from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from os.path import expanduser

import load_intermediate_slices
import intensity_corrections_module
import stitching_module
import register_module
	 
class SBFPreprocess(QMainWindow):
	
	def __init__(self):
		
		QMainWindow.__init__(self)

		loadUi("mainwindow.ui",self)
		self.setWindowTitle("SBFpreprocess v1.0")
		self.addToolBar(NavigationToolbar(self.MatplotlibWidget.canvas, self))
  
		self.inputFolder = None
		self.outputFolder = None
		self.subsetVolume = None

	def openFolder(self):
		title = "Open the root folder with the dataset, from Micromanager"
		flags = QFileDialog.ShowDirsOnly
		self.inputFolder = QFileDialog.getExistingDirectory(self,
															title,
															expanduser("."),
															flags)

		if self.inputFolder == '':
			self.inputFolder = None
			return
		
		self.statusBar().showMessage('Image folder location saved', 2000)

	def selectOutputFolder(self):
		title = "Open the folder to save the dataset"
		flags = QFileDialog.ShowDirsOnly
		self.outputFolder = QFileDialog.getExistingDirectory(self,
															title,
															expanduser("."),
															flags)

		if self.outputFolder == '':
			self.outputFolder = None
			return
		
		self.outputFolderLocationLineEdit.setText(str(self.outputFolder))
		self.statusBar().showMessage('Output folder location saved', 2000)
  	
	def processSubsetForVisualization(self):
	 
		# Check whether an input directory was provided
		if self.inputFolder == None:
			msgBox = QMessageBox()
			msgBox.setText("Input image directory was not provided, please set it first.")
			msgBox.setWindowTitle("Error")
			msgBox.exec()
			return

		# Get information from the UI
		self.processEvery = int(self.processEveryLineEdit.text())
		self.tilesX = int(self.tilesXLineEdit.text())
		self.tilesY = int(self.tilesYLineEdit.text())
		self.correctIntensityVariationFlag = self.correctIntensityVariationsCheckbox.isChecked()
		self.gamma = float(self.gammaValueLineEdit.text())
		self.registerSlicesFlag = self.registerSlicesCheckBox.isChecked()
  
		# Load intermediate slices 
		# Output is in a list format - each element is the substack for a particular tile
		self.subsetVolume = load_intermediate_slices.load(self.inputFolder, self.processEvery, self.tilesX, self.tilesY)
  
		# Intensity corrections
		# Output is in a list format - each element is the substack for a particular tile
		self.subsetVolume = intensity_corrections_module.correct(self.subsetVolume, self.correctIntensityVariationFlag, self.gamma)
  
		# Stitch slices
		# Output is in a list format - single element, stitched output
		if self.tilesX != 1 and self.tilesY != 1:
			self.subsetVolume = stitching_module.stitch(self.stitchVolume)

			# Register slices
			if self.registerSlicesFlag:
				self.subsetVolume = register_module.register(self.subsetVolume)
   
		# Update slider limits
		self.xySlider.SetMaximum(self.subsetVolume.shape[2])
  
	def changeViewingSlice(self, value):
	 
		self.MatplotlibWidget.canvas.axes.clear()
		self.MatplotlibWidget.canvas.axes.imshow(self.subsetVolume[:,:,int(value)])
		self.MatplotlibWidget.canvas.draw()	  
  
	def processStack(self):
		# Check whether an input directory was provided
		if self.inputFolder == None:
			msgBox = QMessageBox()
			msgBox.setText("Input image directory was not provided, please set it first.")
			msgBox.setWindowTitle("Error")
			msgBox.exec()
			return

		# Check whether an output directory was provided
		if self.outputFolder == None:
			msgBox = QMessageBox()
			msgBox.setText("Output directory was not provided, please set it first.")
			msgBox.setWindowTitle("Error")
			msgBox.exec()
			return		

	def fileExit(self):
		app.quit()
  
if __name__ == '__main__':
	app = QApplication([])
	window = SBFPreprocess()
	window.show()
	app.exec_()