# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SuroLevelingDockWidget
                                 A QGIS plugin
 todo
                             -------------------
        begin                : 2016-02-12
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Ondřej Pešek
        email                : ondra.lobo@seznam.cz
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.core import QgsVectorLayer, QgsMapLayerRegistry

def show(filePath,styleName):
    """show csv as layer"""

    uri = "file:" + 3*os.path.sep + filePath + "?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s" % ("EPSG:4326",",", "Lon_deg", "Lat_deg", ".")
    uri = os.path.join(uri).replace('\\','/')
    layerName = filePath.rsplit(os.path.sep,1)
    layerName = layerName[1][:-4]
    layer = QgsVectorLayer(uri, layerName, "delimitedtext")
    style=os.path.dirname(__file__) + os.path.sep + 'styles' + os.path.sep + styleName + '.qml'
    style = os.path.join(style).replace('\\','/')
    layer.loadNamedStyle(style)
    QgsMapLayerRegistry.instance().addMapLayer(layer)