# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flightmapperDialog
								 A QGIS plugin
 create flightroutes and publish them as a webmap
							 -------------------
		begin				: 2015-02-01
		git sha			  : $Format:%H$
		copyright			: (C) 2015 by Riccardo Klinger/ Geolicious
		email				: riccardo.klinger@geolicious.de
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""

import os
from PyQt4 import QtGui, uic
from  qgis.utils import *
#from Ui_flightmapperDialogBase import setupUi
from qgis import *
import os.path
import tempfile
#here is the executable:
from flightmapper_exec import flightmapper_exec



FORM_CLASS, _ = uic.loadUiType(os.path.join(
	os.path.dirname(__file__), 'flightmapper_dialog_base.ui'))


class flightmapperDialog(QtGui.QDialog, FORM_CLASS):
	def __init__(self, parent=None):
		"""Constructor."""
		super(flightmapperDialog, self).__init__(parent)
		# Set up the user interface from Designer.
		# After setupUI you can access any designer object by doing
		# self.<objectname>, and you can use autoconnect slots - see
		# http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
		# #widgets-and-dialogs-with-auto-connect
		self.setupUi(self)
		self.setWindowTitle("QGIS flightmapper")
		self.okButton.clicked.connect(self.flightmapper)	  
		self.cancelButton.clicked.connect(self.close)
		self.lineEdit.setText(tempfile.gettempdir())


		def loadlayer(self):
			print "Interface loaded"
			#canvas = Qgis.utils.iface.mapCanvas()
			#allLayers = canvas.layers()
			#for i in allLayers:
			#	if i.type() == 0: 
			#		self.ui.comboBox.addItem(i.name())
		#loadlayer(self)
	def flightmapper(self):
		self.basemap = self.comboBox_3.currentText()
		self.resolution = self.comboBox_2.currentText()
		self.point_layer = self.comboBox.currentText()
		self.folder = self.lineEdit.text()
		self.title = self.lineEdit_2.text()
		flightmapper_exec(self.basemap, self.resolution, self.point_layer, self.folder, self.title)
		#self.close()