# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flightmapper
                                 A QGIS plugin
 flightmapp creation programm
                             -------------------
        begin                : 2015-01-31
        copyright            : (C) 2015 by Riccardo Klinger
        email                : riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr
from osgeo import gdal
import processing
import shutil
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web
from urlparse import parse_qs
import time
import tempfile
import re
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 

def flightmapper_exec(basemap, resolution, point_layer, folder, title):
	# supply path to where is your qgis installed
	pluginDir = os.path.dirname(os.path.realpath(__file__))
	
	# load providers
	QgsApplication.initQgis()
	# let's determine the current work folder of qgis:
	print os.getcwd()		
	# let's create the overall folder structure:
	outputProjectFileName = os.path.join(folder, 'export_' + str(time.strftime("%Y_%m_%d")) + '_' + str(time.strftime("%I_%M_%S")))
	jsStore = os.path.join(os.getcwd(),outputProjectFileName, 'js')
	os.makedirs(jsStore)
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'Autolinker.min.js', jsStore + os.sep + 'Autolinker.min.js')
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'leaflet-hash.js', jsStore + os.sep + 'leaflet-hash.js')
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'leaflet.markercluster.js', jsStore + os.sep + 'leaflet.markercluster.js')
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'label.js', jsStore + os.sep + 'label.js')
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'proj4.js', jsStore + os.sep + 'proj4.js')
	#shutil.copyfile(pluginDir + os.sep + 'js' + os.sep + 'proj4leaflet.js', jsStore + os.sep + 'proj4leaflet.js')
	dataStore = os.path.join(os.getcwd(),outputProjectFileName, 'data')
	os.makedirs(dataStore)
	cssStore = os.path.join(os.getcwd(),outputProjectFileName, 'css')
	os.makedirs(cssStore)
	#shutil.copyfile(pluginDir + os.sep + 'css' + os.sep + 'MarkerCluster.css', cssStore + os.sep + 'MarkerCluster.css')
	#shutil.copyfile(pluginDir + os.sep + 'css' + os.sep + 'label.css', cssStore + os.sep + 'label.css')
	#shutil.copyfile(pluginDir + os.sep + 'css' + os.sep + 'MarkerCluster.Default.css', cssStore + os.sep + 'MarkerCluster.Default.css')
	picturesStore = os.path.join(os.getcwd(),outputProjectFileName, 'pictures')
	os.makedirs(picturesStore)
	miscStore = os.path.join(os.getcwd(),outputProjectFileName, 'misc')
	os.makedirs(miscStore)
	#lets create a css file for own css:
	
	#the index file has an easy beginning. we will store it right away:
	canvas = qgis.utils.iface.mapCanvas()
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'w') as f_html:
		base = """
<!DOCTYPE html>
<html>
<head> """
		if title == "":
			base +="""
	<title>QGIS2leaf webmap</title>
	"""
		else:
			base +="""
	<title>""" + (title).encode('utf-8') + """</title>
	"""
		base += """
	<meta charset="utf-8" />
	<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css" /> <!-- we will us e this as the styling script for our webmap-->
	<link rel="stylesheet" type="text/css" href="css/own_style.css">
	<!--script src="http://code.jquery.com/jquery-1.11.1.min.js"></script-->
	"""
		base += """
</head>
<body>
	<div id="map"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
	"""
		f_html.write(base)
		f_html.close()
	# let's create the js files in the data folder of input vector files:

	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		safeLayerName = re.sub('[\W_]+', '', i.name())
		if safeLayerName == re.sub('[\W_]+', '', point_layer):
			qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + 'exp_' + safeLayerName + '.js', 'utf-8', exp_crs, 'GeoJson', 1, layerOptions=["COORDINATE_PRECISION=4"])
			with open(dataStore + os.sep + 'exp_' + safeLayerName + '.js', "r+") as f2:
				old = f2.read() # read everything in the file
				f2.seek(0) # rewind
				f2.write("var exp_" + str(safeLayerName) + " = " + old) # write the new line before
				f2.close()

	webbrowser.open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html')

