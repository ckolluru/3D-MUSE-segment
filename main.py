from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import zarr
import os
import numpy as np

from file_functions import read_images

class MainWindow(QMainWindow):
	
	def __init__(self):
		
		QMainWindow.__init__(self)

		loadUi("mainwindow_tab2.ui",self)

		self.addToolBar(NavigationToolbar(self.Mplwidget.canvas, self))
		self.Mplwidget.canvas.axes.axis('off')
		
		self.intermediateSlices = None
		self.zarr_file = None
		self.img_stack = None
		self.img_delete = []
		self.slice_to_annotate = None
		self.annotate_stack = None
		self.slide1_idx = 0
		self.slide2_idx = 0

	def updatePlotWindow(self, image, overlay = None):

		if self.tabWidget_2.currentIndex() == 0:
			self.Mplwidget.canvas.axes.clear()
			self.Mplwidget.canvas.axes.axis('off')
			self.Mplwidget.canvas.axes.imshow(image, cmap = 'gray')
			self.Mplwidget.canvas.draw()
		else:
			self.Mplwidget_2.canvas.axes.clear()
			self.Mplwidget_2.canvas.axes.axis('off')
			self.Mplwidget_2.canvas.axes.imshow(image, cmap = 'gray')
			self.Mplwidget_2.canvas.draw()
		
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

		self.img_stack = read_images(self.zarr_file)

		# Set maximum of slice slider to the number of images in the stack
		self.sliceSlider.setMaximum(len(self.img_stack)-1)
		
		# Display the first image of the stack
		image = self.img_stack[0]
		self.updatePlotWindow(image, overlay=None)

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
		
	def sliceSliderUpdate(self, value):

		# Display the corresponding image
		if self.tabWidget_2.currentIndex() == 0:
			# Update the number is the Line Edit text box
			self.sliceLineEdit.setText(str(value))
			# Display Full Stack Image
			image = self.img_stack[value]
		else:
			# Update the number is the Line Edit text box
			self.sliceLineEdit_2.setText(str(value))
			# Display Full Stack Image
			image = self.annotate_stack[value]
		self.updatePlotWindow(image, overlay=None)
		#self.SceneManager.visualizeXYSlice(value)		

	def sliceEdit_changed(self):
	 
		value = self.sender().text()
  
		try:
			if self.tabWidget_2.currentIndex() == 0:
				self.sliceSlider.setValue(int(value))
			else:
				self.sliceSlider_2.setValue(int(value))
		
		except:			
			msgBox = QMessageBox()
			msgBox.setText("Incorrect value for image slice, expect integer")
			msgBox.exec()
			self.sender().setText(str(0))
			self.sliceSliderUpdate(0)
			return None
		
		self.sliceSliderUpdate(int(value))
		#self.SceneManager.visualizeXYSlice(int(self.sliceLineEdit.text()))

	def deleteslice_button(self):

		if not self.img_delete:
			self.img_delete.append(self.sliceSlider.value())

		elif self.sliceSlider.value() not in self.img_delete:
			self.img_delete.append(self.sliceSlider.value())

		else:
			msgBox = QMessageBox()
			msgBox.setText("This slice has already been recorded for deletion")
			msgBox.exec()
		
		print(self.img_delete)

	def slicesforannotate(self):

		# Create a QMessageBox with two buttons: Even intervals and Clustering
		msgBox = QMessageBox()
		msgBox.setText = ("Choose a selection option")
		msgBox.addButton("Even Interval", QMessageBox.AcceptRole)
		msgBox.addButton("Cluster Option", QMessageBox.RejectRole)

		# Show the QMessageBox and get the user's choice
		choice = msgBox.exec_()

		# Handle the user's choice
		if choice == QMessageBox.AcceptRole: # Even Interval
			# Open a QInputDialog for the user to enter a number
			self.slice_to_annotate, ok = QInputDialog.getInt(self, "Enter a Number",
				    "Please enter the number of image slices you would like to annotate:")
			if ok:
				# The user entered a number
				# Use this number to select the number of slices for annotation
				print("Number entered:", self.slice_to_annotate)

				# Select the slices for annotation
				if self.slice_to_annotate > len(self.img_stack):
					# Cannot annotate more slices than are in the image stack
					msgBox = QMessageBox()
					msgBox.setText("This number exceeds the number of image slices available.")
					msgBox.exec()
				else:
					# Create an annotation stack

					self.annotate_stack = self.img_stack[np.linspace(0, len(self.img_stack)-1, self.slice_to_annotate, dtype = int)]
					print(self.annotate_stack.shape)
					self.tabWidget_2.setCurrentIndex(1)
					self.sliceSlider_2.setMaximum(len(self.annotate_stack)-1)
					image = self.annotate_stack[0]
					self.updatePlotWindow(image, overlay=None)

		else: # Clustering Option

			print("Determining slices to annotate using clustering")


if __name__ == '__main__':
	app = QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()