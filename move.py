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

def move_by_points(inputfile,outputfile,value):

    """move by number of points"""

    f=open(inputfile,'rb')
    g=open(outputfile,'wb')
    g.write(f.readline())

    if value>0: # bodu 1 dam hodnoty a cislo bodu 2
        for x in range(value):
            a=f.readline()

        while a:
            a=f.readline()
            if a:
                a=a.split(',',2) # changing the number of point
                a[1]=str(int(a[1])-value)
                a=','.join(a)
                g.write(a)

    else:
        a=[1]

        while a:
            a=f.readline()
            if a:
                a=a.split(',',2) # changing the number of point
                a[1]=str(int(a[1])-value)
                a=','.join(a)
                g.write(a)

    f.close()
    g.close()