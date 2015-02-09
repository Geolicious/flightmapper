# -*- coding: utf-8 -*-
"""
/***************************************************************************
 flightmapper
								 A QGIS plugin
 flightmapp creation programm
							 -------------------
		begin				: 2015-01-31
		copyright			: (C) 2015 by Riccardo Klinger
		email				: riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""

#from PyQt4.QtCore import QFileInfo
from PyQt4.QtCore import *
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
import math
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 

def flightmapper_exec(basemap, resolution, point_layer_im, folder, title, addit):
	# supply path to where is your qgis installed
	pluginDir = os.path.dirname(os.path.realpath(__file__))
	
	# load providers
	QgsApplication.initQgis()
	# let's determine the current work folder of qgis:
	print os.getcwd()		
	
## let's create the overall folder structure:
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
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'css' + os.sep + 'own_style.css', 'w') as f_css:
		text = """
<style>
	body {
		padding: 0;
		margin: 0;
	}
	html, body, #map {
		height: 100%;
		width: 100%;
		padding: 0;
		margin: 0;
	}
</style>
"""
		f_css.write(text)
		f_css.close()
	#the call for densifying a line:
	#processing.runalg("qgis:densifygeometries","C:\\Users\\ricckli\\.qgis2\\python\\plugins\\qgis2leaf\\test_data\\line_feature.shp",10,None)
##lets write the beginning of the index.html	
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
	<div id="map" width="95%" height="400"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
	<script src="data/exp_line.js"></script>
	<script src="data/exp_point.js"></script>
	"""
		f_html.write(base)
		f_html.close()
# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		safeLayerName = re.sub('[\W_]+', '', i.name())
		if safeLayerName == re.sub('[\W_]+', '', point_layer_im):
			point_layer = i #this is my pointlayer
			point_layer_dp=point_layer.dataProvider()
			vlayer_crs=point_layer_dp.crs()
			vertexes = []
			features = point_layer.getFeatures()

			for f in features:
			    geom = f.geometry()
			    point = geom.asPoint()
			    vertexes.append(point)
			## now let's create several layers to with his own CRS to densify and transfomr the densified vertexes back to 4326:
			crs_src = QgsCoordinateReferenceSystem(vlayer_crs)
			layers = []
			for i in range(0, len(vertexes)-1):
			    crs = QgsCoordinateReferenceSystem()
			    #try with only one CRS fails...: 
			    #crs.createFromProj4("+proj=eqdc +lat_0=0 +lon_0=0 +lat_1=60 +lat_2=60 +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs")

			    crs.createFromProj4("+proj=aeqd +lat_0=" + str(vertexes[i][1])+ " +lon_0=" + str(vertexes[i][0]) +" +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs")
			    #crs.saveAsUserCRS('azimuthal equidistant point' + str(i+1))
			    qgis.utils.iface.mapCanvas().mapRenderer().setDestinationCrs(crs) 
			    layer = QgsVectorLayer('LineString?crs=' + crs.toWkt(), 'line'+str(i), "memory")
			    layer.setCrs(crs)
			    pr = layer.dataProvider() 
			    line = QgsFeature()
			    xform = QgsCoordinateTransform(crs_src, crs)
			    xform2 = QgsCoordinateTransform(crs, crs_src)
			    start_point = QgsPoint(0,0)
			    end_point = xform.transform(QgsPoint(vertexes[i+1]))
			    seg = [start_point, end_point]
			    line.setGeometry(QgsGeometry.fromPolyline(seg))
			    pr.addFeatures([line])
			    layer.updateExtents()
			    QgsMapLayerRegistry.instance().addMapLayer(layer)
			    dens_layer = processing.runalg("qgis:densifygeometriesgivenaninterval",'line'+str(i),resolution,None)
			    vlayer=QgsVectorLayer(dens_layer.get('OUTPUT'), "densified_layer" + str(i), "ogr")
			    
			    #QgsMapLayerRegistry.instance().addMapLayer(vlayer2)
			    #qgis.core.QgsVectorFileWriter.writeAsVectorFormat(vlayer, "densified_layer" + str(i) + '.shp', 'utf-8', exp_crs, 'ShapeFile')
			    ##store dens_layers in 4326:
			    crs_4326 = QgsCoordinateReferenceSystem(4326)
			    layer_4326 = QgsVectorLayer('LineString?crs=' + crs_4326.toWkt(), 'line'+str(i), "memory")
			    layer_4326.setCrs(crs_4326)
			    pr_4326 = layer_4326.dataProvider() 
			    outFeat = QgsFeature()
			    for f in vlayer.getFeatures():
			        geom = f.geometry()
			        geom.transform(xform2)
			        outFeat.setGeometry(geom)
			        outFeat.setAttributes(f.attributes())
			    pr_4326.addFeatures([outFeat])
			    layer_4326.updateExtents()
			    #QgsMapLayerRegistry.instance().addMapLayer(layer_4326)
			    QgsMapLayerRegistry.instance().removeMapLayer(layer.id())
			    layers.append(layer_4326)
			

			#layer_merge= processing.runalg('qgis:mergevectorlayers', layers[1], layers[3], None)
			#layer_merge2 = QgsVectorLayer(layer_merge.get('OUTPUT'), "layer merge", "ogr")
			#QgsMapLayerRegistry.instance().addMapLayer(layer_merge2)
			#for i in range(2,len(layers)):
			    #layer_merge= processing.runalg('qgis:mergevectorlayers', layer_merge, layers[i], None)
			    #layer_merge = processing.runalg('qgis:mergevectorlayers', layer_merge, layers[i+2], None)
			qgis.utils.iface.mapCanvas().mapRenderer().setDestinationCrs(crs_src) 
			#def pairs(list):
			    # list pairs iteration 
			    #for i in range(1, 2):
			        #yield list[i-1], list[i]


			vertexes_merge = []
			for f in range(0, len(layers)):
			    layer = layers[f]
			    for f in layer.getFeatures():
			        line = f.geometry()
			        for i in line.asPolyline():
			            vertexes_merge.append(QgsPoint(i))
			breaks = []
			for i in range(0,len(vertexes_merge)-1):
			    if math.sqrt((vertexes_merge[i][0]-vertexes_merge[i+1][0])**2) > 2:
			        breaks.append(i)
			breaks.append(len(vertexes_merge)-1)

			layer_merge = QgsVectorLayer('LineString', 'line', "memory")
			layer_merge.setCrs(crs_4326)
			pr_merge = layer_merge.dataProvider() 
			start = 0
			for index in range(0,len(breaks)):
			    end = breaks[index]
			    line_merge = QgsFeature()
			    line_merge.setGeometry(QgsGeometry.fromPolyline(vertexes_merge[start:end]))
			    start = breaks[index] + 1
			#   end = breaks[index]
			    pr_merge.addFeatures([line_merge])
			    layer_merge.updateExtents()
			if addit == True:
				QgsMapLayerRegistry.instance().addMapLayer(layer_merge)
			for f in range(0, len(layers)):
			    QgsMapLayerRegistry.instance().removeMapLayer(layers[f].id())

			#print len(vertexes_merge)
			del layers, pr_4326, vertexes_merge, breaks, line_merge
			qgis.core.QgsVectorFileWriter.writeAsVectorFormat(layer_merge,dataStore + os.sep + 'exp_line.js', 'utf-8', exp_crs, 'GeoJson', 0, layerOptions=["COORDINATE_PRECISION=4"])
			qgis.core.QgsVectorFileWriter.writeAsVectorFormat(point_layer,dataStore + os.sep + 'exp_point.js', 'utf-8', exp_crs, 'GeoJson', 0, layerOptions=["COORDINATE_PRECISION=4"])

			with open(dataStore + os.sep + 'exp_line.js', "r+") as f2:
				old = f2.read() # read everything in the file
				f2.seek(0) # rewind
				f2.write("var exp_line = " + old) # write the new line before
				f2.close()
			with open(dataStore + os.sep + 'exp_point.js', "r+") as f3:
				old = f3.read() # read everything in the file
				f3.seek(0) # rewind
				f3.write("var exp_point = " + old) # write the new line before
				f3.close()
	#now create the webmap:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f_html2:
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true }).fitBounds([[-90,-180],[90,180]]);
		var basemap_0 = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
			attribution: "made with <a href='http://www.geolicious.de'>flightmapper</a> &copy; <a href='http://openstreetmap.org'>OpenStreetMap</a> contributors,<a href='http://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>"});	
		basemap_0.addTo(map);
		var poin = new L.geoJson(exp_point);
		var line = new L.geoJson(exp_line);
		line.addTo(map);
	</script>
 </body>
 """
		f_html2.write(middle)
		f_html2.close()
	webbrowser.open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html')