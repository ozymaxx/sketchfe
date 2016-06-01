# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:18:35 2016

@author: kurmanbek & ozan
oaltiok15@ku.edu.tr
kkaiyrbekov15@ku.edu.tr
"""

import Point
import numpy as np

class Stroke:
    
    def __init__( self, sid ):
        self.sid = sid
        self.points = [] ##HERE IS PROBLEM STATIC?????
    
    #Add stroke points takes point instance as an argument
    def addPoint( self, point ):
        self.points.append( point )
    
    def listCoordinates(self):
        xs = []
        ys = []
        
        for point in self.points:
            xs.append(point.x)
            ys.append(point.y)
            
        return np.array((np.asarray(xs).T,np.asarray(ys).T)).T
