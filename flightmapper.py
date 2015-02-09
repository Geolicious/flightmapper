# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flightmapper
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from flightmapper_dialog import flightmapperDialog
import os.path
import qgis.utils

class flightmapper:
	"""QGIS Plugin Implementation."""

	def __init__(self, iface):
		"""Constructor.

		:param iface: An interface instance that will be passed to this class
			which provides the hook by which you can manipulate the QGIS
			application at run time.
		:type iface: QgsInterface
		"""
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value('locale/userLocale')[0:2]
		locale_path = os.path.join(
			self.plugin_dir,
			'i18n',
			'flightmapper_{}.qm'.format(locale))

		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)

		# Create the dialog (after translation) and keep reference
		self.dlg = flightmapperDialog()

		# Declare instance attributes
		self.actions = []
		self.menu = self.tr(u'&flightmapper')
		# TODO: We are going to let the user set this up in a future iteration
		self.toolbar = self.iface.addToolBar(u'flightmapper')
		self.toolbar.setObjectName(u'flightmapper')

	# noinspection PyMethodMayBeStatic
	def tr(self, message):
		"""Get the translation for a string using Qt translation API.

		We implement this ourselves since we do not inherit QObject.

		:param message: String for translation.
		:type message: str, QString

		:returns: Translated version of message.
		:rtype: QString
		"""
		# noinspection PyTypeChecker,PyArgumentList,PyCallByClass
		return QCoreApplication.translate('flightmapper', message)


	def add_action(
		self,
		icon_path,
		text,
		callback,
		enabled_flag=True,
		add_to_menu=True,
		add_to_toolbar=True,
		status_tip=None,
		whats_this=None,
		parent=None):


		icon = QIcon(icon_path)
		action = QAction(icon, text, parent)
		action.triggered.connect(callback)
		action.setEnabled(enabled_flag)

		if status_tip is not None:
			action.setStatusTip(status_tip)

		if whats_this is not None:
			action.setWhatsThis(whats_this)

		if add_to_toolbar:
			self.toolbar.addAction(action)

		if add_to_menu:
			self.iface.addPluginToMenu(
				self.menu,
				action)

		self.actions.append(action)

		return action

	def initGui(self):
		"""Create the menu entries and toolbar icons inside the QGIS GUI."""

		icon_path = ':/plugins/flightmapper/icon.png'
		self.add_action(
			icon_path,
			text=self.tr(u'create flightmap'),
			callback=self.run,
			parent=self.iface.mainWindow())


	def unload(self):
		"""Removes the plugin menu item and icon from QGIS GUI."""
		for action in self.actions:
			self.iface.removePluginMenu(
				self.tr(u'&flightmapper'),
				action)
			self.iface.removeToolBarIcon(action)


	def run(self):
		"""Run method that performs all the real work"""
		# show the dialog
		self.dlg.show()
		#clear old entries:
		self.dlg.comboBox.clear()
		self.dlg.comboBox_3.clear()
		self.dlg.comboBox_2.clear()
		#add all "possible" layers:
		canvas = qgis.utils.iface.mapCanvas()
		allLayers = canvas.layers()
		for layer in allLayers:
			if layer.type() == 0 and layer.geometryType() == 0:
	  			self.dlg.comboBox.addItem(layer.name())
		#add basemaps
		self.dlg.comboBox_3.addItem("OSM")
		self.dlg.comboBox_3.addItem("WaterColor")
		#add resolutions:
		self.dlg.comboBox_2.addItem("1 km")
		self.dlg.comboBox_2.addItem("5 km")
		self.dlg.comboBox_2.addItem("10 km")
		self.dlg.comboBox_2.addItem("50 km")
		self.dlg.comboBox_2.addItem("100 km")
		self.dlg.comboBox_2.addItem("500 km")

		# Run the dialog event loop
		result = self.dlg.exec_()