# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Move (the main function)
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

from qgis.core import QgsDistanceArea, QgsPoint
from math import sqrt,pi,pow,fabs,sin,cos,tan,ceil

import time

class MoveError(StandardError):
    pass

class MoveBase:
    def __init__(self, inputfile, outputfile):
        self.inputfile = open(inputfile,'rb')
        self.outputfile = open(outputfile,'wb')

    def _close(self):
        for f in (self.inputfile, self.outputfile):
            if not f.closed:
                f.close()

    def _check(self):
        if not self.inputfile or self.inputfile.closed:
            raise MoveError("Input file is not open")

        if not self.outputfile or self.outputfile.closed:
            raise MoveError("Output file is not open")

    def by_points(self, value):
        """move by number of points"""

        def mereni_values(self):
            """reading values in mereni"""

            header=self.inputfile.readline()
            beforeMereni=header.split('mereni')
            numberOfMereniColumn=beforeMereni[0].split(',')
            mereni=[]
            a=self.inputfile.readline()
            while a:
                a=a.split(',')
                mereni.append(a[len(numberOfMereniColumn)-1])
                a=self.inputfile.readline()

            self.inputfile.seek(0)
            return mereni

        self._check()

        mereni=mereni_values(self)
        header=self.inputfile.readline()
        self.outputfile.write(header)
        beforeMereni=header.split('mereni')
        numberOfMereniColumn=beforeMereni[0].split(',')

        if value>0:
            a=self.inputfile.readline()

            while a:
                a=a.split(',')
                try:
                    a[len(numberOfMereniColumn)-1]=mereni.pop(value)
                except: break
                a=','.join(a)
                self.outputfile.write(a)
                a=self.inputfile.readline()

        elif value<0:
            for x in range(abs(value)):
                self.inputfile.readline()

            beforeRECS=header.split('RECS')
            numberOfRECSColumn=beforeRECS[0].split(',')
            a=self.inputfile.readline()
            while a:
                a=a.split(',')
                a[len(numberOfRECSColumn)-1]=str(int(a[len(numberOfRECSColumn)-1])+value)
                a[len(numberOfMereniColumn)-1]=mereni.pop(0)
                a=','.join(a)
                self.outputfile.write(a)
                a=self.inputfile.readline()

        else:
            a=self.inputfile.readline()
            while a:
                self.outputfile.write(a)
                a=self.inputfile.readline()

        self._close()

    def by_distance(self, distance):
        """move by constant distance"""

        def iterations(distance,h):
            FIe1=0
            LAMe1=0
            FI=100
            LAM=100

            # iterations
            while fabs(FI-FIe1)>0.0000000001 and fabs(LAM -LAMe1)>0.0000000001:
                FI=FIe1
                LAM=LAMe1
                for i in range(0,int(ceil(distance/h))):
                    kfi=[]
                    klam=[]
                    kazi=[]
                    kfi.append(cos(azi[i])/(a*(1-(e2))/(pow((sqrt(1-(e2)*pow(sin(fi[i]),2))),3))))
                    klam.append(sin(azi[i])/((a/(sqrt(1-(e2)*pow(sin(fi[i]),2))))*cos(fi[i])))
                    kazi.append(sin(azi[i])*tan(fi[i])/(a/(sqrt(1-(e2)*pow(sin(fi[i]),2)))))
                    for j in range(1,3):
                        kfi.append(cos(azi[i]+kazi[j-1]*h/2)/(a*(1-(e2))/(pow(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2)),3))))
                        klam.append(sin(azi[i]+kazi[j-1]*h/2)/((a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2))))*cos(fi[i]+kfi[j-1]*h/2)))
                        kazi.append(sin(azi[i]+kazi[j-1]*h/2)*tan(fi[i]+kfi[j-1]*h/2)/(a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2)))))

                    kfi.append(cos(azi[i]+kazi[2]*h)/(a*(1-(e2))/(pow(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2)),3))))
                    klam.append(sin(azi[i]+kazi[2]*h)/((a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2))))*cos(fi[i]+kfi[2]*h)))
                    kazi.append(sin(azi[i]+kazi[2]*h)*tan(fi[i]+kfi[2]*h)/(a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2)))))

                    fi.append(fi[i]+(h/6.0)*(kfi[0]+2*kfi[1]+2*kfi[2]+kfi[3]))
                    lam.append(lam[i]+(h/6.0)*(klam[0]+2*klam[1]+2*klam[2]+klam[3]))
                    azi.append(azi[i]+(h/6.0)*(kazi[0]+2*kazi[1]+2*kazi[2]+kazi[3]))

                FIe1=fi[i+1]
                LAMe1=lam[i+1]
                h=h/2
                fi[1:]=[]
                lam[1:]=[]
                azi[1:]=[]

            return FIe1,LAMe1

        self._check()
        header=self.inputfile.readline()
        beforeLat=header.split('Lat_deg')
        numberOfLatColumn=beforeLat[0].split(',')
        beforeLong=header.split('Lon_deg')
        numberOfLonColumn=beforeLong[0].split(',')
        self.outputfile.write(header)

        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')
        #d.ellipsoidalEnabled()
        d.setEllipsoidalMode(True)
        d.ellipsoid()
        a = 6378137.0 # WGS84 ellipsoid parametres
        e2 = 0.081819190842622
        line1=self.inputfile.readline()

        if distance>0:
            line1=line1.split(',')
            while line1:
                line2=self.inputfile.readline()
                if line2:
                    line2=line2.split(',')
                    p1=QgsPoint(float(line1[len(numberOfLonColumn)-1]),float(line1[len(numberOfLatColumn)-1]))
                    p2=QgsPoint(float(line2[len(numberOfLonColumn)-1]),float(line2[len(numberOfLatColumn)-1]))

                    if p1!=p2:
                        aziA = d.bearing(p1,p2)

                        h=distance/2.0
                        fi=[float(line1[len(numberOfLatColumn)-1])*pi/180]
                        lam=[float(line1[len(numberOfLonColumn)-1])*pi/180]
                        azi=[aziA]

                        FIe1,LAMe1 = iterations(distance,h)
                        line1[len(numberOfLatColumn)-1]=str(FIe1*180/pi) # changing latitude and longitude of new point
                        line1[len(numberOfLonColumn)-1]=str(LAMe1*180/pi)

                    line1=','.join(line1)
                    self.outputfile.write(line1)
                    line1=1*line2

                else: break
        elif distance<0:
            distance=fabs(distance)
            line1=line1.split(',')
            while line1:
                line2=self.inputfile.readline()

                if line2:
                    line2=line2.split(',')
                    p1=QgsPoint(float(line1[len(numberOfLonColumn)-1]),float(line1[len(numberOfLatColumn)-1]))
                    p2=QgsPoint(float(line2[len(numberOfLonColumn)-1]),float(line2[len(numberOfLatColumn)-1]))

                    if p1!=p2:
                        aziA = d.bearing(p2,p1)

                        h=distance/2.0
                        fi=[float(line2[len(numberOfLatColumn)-1])*pi/180]
                        lam=[float(line2[len(numberOfLonColumn)-1])*pi/180]
                        azi=[aziA]

                        FIe1,LAMe1 = iterations(distance,h)
                        line1=1*line2
                        line1[len(numberOfLatColumn)-1]=str(FIe1*180/pi) # changing latitude and longitude of new point
                        line1[len(numberOfLonColumn)-1]=str(LAMe1*180/pi)

                    line1=','.join(line1)
                    self.outputfile.write(line1)
                    line1=1*line2

                else: break
        else:
            while line1:
                self.outputfile.write(line1)
                line1=self.inputfile.readline()

        self._close()

    def by_seconds(self, seconds):
        raise NotImplementedError()

class MovePyProj(MoveBase):
    def __init__(self, inputfile, outputfile):
        MoveBase.__init__(self, inputfile, outputfile)

    def by_seconds(self, seconds):
        raise NotImplementedError()

class Move(MoveBase):
    def __init__(self, inputfile, outputfile):
        MoveBase.__init__(self, inputfile, outputfile)
    
    def by_seconds(self, seconds):
        """move by variable distance"""

        def iterations(distance,h):
            FIe1=0
            LAMe1=0
            FI=100
            LAM=100

            # iterations
            while fabs(FI-FIe1)>0.0000000001 and fabs(LAM -LAMe1)>0.0000000001:
                FI=FIe1
                LAM=LAMe1
                for i in range(0,int(ceil(distance/h))):
                    kfi=[]
                    klam=[]
                    kazi=[]
                    kfi.append(cos(azi[i])/(a*(1-(e2))/(pow((sqrt(1-(e2)*pow(sin(fi[i]),2))),3))))
                    klam.append(sin(azi[i])/((a/(sqrt(1-(e2)*pow(sin(fi[i]),2))))*cos(fi[i])))
                    kazi.append(sin(azi[i])*tan(fi[i])/(a/(sqrt(1-(e2)*pow(sin(fi[i]),2)))))
                    for j in range(1,3):
                        kfi.append(cos(azi[i]+kazi[j-1]*h/2)/(a*(1-(e2))/(pow(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2)),3))))
                        klam.append(sin(azi[i]+kazi[j-1]*h/2)/((a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2))))*cos(fi[i]+kfi[j-1]*h/2)))
                        kazi.append(sin(azi[i]+kazi[j-1]*h/2)*tan(fi[i]+kfi[j-1]*h/2)/(a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[j-1]*h/2),2)))))

                    kfi.append(cos(azi[i]+kazi[2]*h)/(a*(1-(e2))/(pow(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2)),3))))
                    klam.append(sin(azi[i]+kazi[2]*h)/((a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2))))*cos(fi[i]+kfi[2]*h)))
                    kazi.append(sin(azi[i]+kazi[2]*h)*tan(fi[i]+kfi[2]*h)/(a/(sqrt(1-(e2)*pow(sin(fi[i]+kfi[2]*h),2)))))

                    fi.append(fi[i]+(h/6.0)*(kfi[0]+2*kfi[1]+2*kfi[2]+kfi[3]))
                    lam.append(lam[i]+(h/6.0)*(klam[0]+2*klam[1]+2*klam[2]+klam[3]))
                    azi.append(azi[i]+(h/6.0)*(kazi[0]+2*kazi[1]+2*kazi[2]+kazi[3]))

                FIe1=fi[i+1]
                LAMe1=lam[i+1]
                h=h/2
                fi[1:]=[]
                lam[1:]=[]
                azi[1:]=[]

            return FIe1,LAMe1

        self._check()
        header=self.inputfile.readline()
        beforeLat=header.split('Lat_deg')
        numberOfLatColumn=beforeLat[0].split(',')
        beforeLong=header.split('Lon_deg')
        numberOfLonColumn=beforeLong[0].split(',')
        beforeSec=header.split('Gtm_sec')
        numberOfSecColumn=beforeSec[0].split(',')
        self.outputfile.write(header)

        d = QgsDistanceArea()
        d.setEllipsoid('WGS84')
        #d.ellipsoidalEnabled()
        d.setEllipsoidalMode(True)
        d.ellipsoid()
        a = 6378137.0 # WGS84 ellipsoid parametres
        e2 = 0.081819190842622
        line1=self.inputfile.readline()

        if seconds>0:
            linePos=self.inputfile.tell()
            line1=line1.split(',')
            while line1:
                self.inputfile.seek(linePos)
                line2=self.inputfile.readline()
                linePos=self.inputfile.tell()
                moveTime=1*seconds
                outline=1*line1
                inline=line2.split(',')

                if line2:
                    for i in range(int(seconds)+1): # for case of more than 1 second
                        if line2:
                            line2=line2.split(',')
                            p1=QgsPoint(float(line1[len(numberOfLonColumn)-1]),float(line1[len(numberOfLatColumn)-1]))
                            p2=QgsPoint(float(line2[len(numberOfLonColumn)-1]),float(line2[len(numberOfLatColumn)-1]))

                            if p1!=p2:
                                aziA = d.bearing(p1,p2)
                                l = d.computeDistanceBearing(p1,p2)[0]

                                if moveTime>1:
                                    moveTime=moveTime-1
                                elif moveTime!=0 and moveTime!=1: #first geodetic problem
                                    distance=l/(float(line2[len(numberOfSecColumn)-1])-float(line1[len(numberOfSecColumn)-1]))*moveTime
                                    h=distance/2.0
                                    fi=[float(line1[len(numberOfLatColumn)-1])*pi/180]
                                    lam=[float(line1[len(numberOfLonColumn)-1])*pi/180]
                                    azi=[aziA]

                                    FIe1,LAMe1 = iterations(distance,h)
                                    moveTime=0

                                else:
                                    FIe1=float(line2[len(numberOfLatColumn)-1])*pi/180
                                    LAMe1=float(line2[len(numberOfLonColumn)-1])*pi/180
                                    moveTime=0
                                    break

                        else:break
                        line1=1*line2
                        line2=self.inputfile.readline()

                else: break
                line1=1*inline
                if moveTime==0:
                    outline[len(numberOfLatColumn)-1]=str(FIe1*180/pi) # changing latitude and longitude of new point
                    outline[len(numberOfLonColumn)-1]=str(LAMe1*180/pi)
                    outline=','.join(outline)
                    self.outputfile.write(outline)

        elif seconds<0:
            line=[]
            line.append(line1)
            line[0]=line[0].split(',')
            if line:
                if int(seconds)!=seconds:
                    for x in range(1,int(fabs(seconds))+2):
                        line.append(self.inputfile.readline())
                        line[x]=line[x].split(',')
                else:
                    for x in range(1,int(fabs(seconds)+1)):
                        line.append(self.inputfile.readline())
                        line[x]=line[x].split(',')

                while line[x]!=['']:
                    moveTime=1*seconds
                    for i in reversed(range(x+1)):
                        p1=QgsPoint(float(line[i-1][len(numberOfLonColumn)-1]),float(line[i-1][len(numberOfLatColumn)-1]))
                        p2=QgsPoint(float(line[i][len(numberOfLonColumn)-1]),float(line[i][len(numberOfLatColumn)-1]))

                        if p1!=p2:
                            aziA = d.bearing(p2,p1)
                            l = d.computeDistanceBearing(p1,p2)[0]

                            if moveTime<-1:
                                moveTime=moveTime+1
                            elif moveTime!=0 and moveTime!=-1: #first geodetic problem
                                distance=l/(float(line[i][len(numberOfSecColumn)-1])-float(line[i-1][len(numberOfSecColumn)-1]))*fabs(moveTime)
                                h=distance/2.0
                                fi=[float(line[i][len(numberOfLatColumn)-1])*pi/180]
                                lam=[float(line[i][len(numberOfLonColumn)-1])*pi/180]
                                azi=[aziA]

                                FIe1,LAMe1 = iterations(distance,h)
                                break

                            else:
                                FIe1=float(line[i-1][len(numberOfLatColumn)-1])*pi/180
                                LAMe1=float(line[i-1][len(numberOfLonColumn)-1])*pi/180
                                break

                    outline=1*line[x]
                    outline[len(numberOfLatColumn)-1]=str(FIe1*180/pi) # changing latitude and longitude of new point
                    outline[len(numberOfLonColumn)-1]=str(LAMe1*180/pi)
                    outline=','.join(outline)
                    self.outputfile.write(outline)

                    del line[0]
                    line.append(self.inputfile.readline())
                    line[x]=line[x].split(',')

        else:
            while line1:
                self.outputfile.write(line1)
                line1=self.inputfile.readline()

        self._close()


