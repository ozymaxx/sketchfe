# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:32:45 2016

@author: kurmanbek & ozan
oaltiok15@ku.edu.tr
kkaiyrbekov15@ku.edu.tr
"""

import Point
import Stroke
import numpy as np
import math
import matplotlib.pyplot as plt
import xml.etree.cElementTree as ET
import os
import uuid
import copy

class Sketch:
    
    #Instantiate sketch
    def __init__( self, sketch_id, strokes=[]):
        self.sketch_id = sketch_id
        self.strokes = copy.copy(strokes)
    
    #Add stroke to a list of strokes of the sketch,
    #takes stroke instance as a parameter  
    def addStrokes( self, stroke ):
        self.strokes.append( stroke )
    
    #Normalize symbol by:
    #translating center of mass to the origin and
    #scaling it horizontally and vertically so it ha unit standard deviation in both axes
    def normalize( self, verbose=False):
        #list_of_points, point_count, stroke_count = self.getListOfXYPoints( self )
        #coords = np.array( list_of_points ).reshape( point_count, 2 )
        coords = self.listCoordinates()
        point_count,ccrd = coords.shape
        stroke_count = len(self.strokes)
        mean = np.mean(coords, 0)
        sdev = np.std(coords, 0)
        coords = coords - mean
        
        if sdev[0] != 0 and sdev[1] != 0:
			coords = coords * ( 1 / sdev )
			
        new_sketch = self.constructNormalizedSketch(coords, point_count, stroke_count )
        
        if verbose:
            print(mean, sdev)
            print(np.std(coords, 0))
            print(np.mean(coords, 0))
            for i in range(0, point_count):
                print( coords[i, 0], coords[i, 1] )
            
            plt.figure(1)            
            allpts = new_sketch.listCoordinates()
            plt.plot(allpts[:,0],allpts[:,1])
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('New Sketch with Normalized Points')
            new_sketch.printContents()
        
        return new_sketch
    
    #Returns a new sketch which is centered and nomalized
    def constructNormalizedSketch( self, coords, point_count, stroke_count ):
        #instantiate new sketch
        new_sketch = Sketch(self.sketch_id,strokes=[])
        ptr = 0
        #Add each stroke to a sketch with corresponding new coordinates
        for i in range( 0, stroke_count ):
            stroke        = Stroke.Stroke( self.strokes[i].sid )
            num_of_points = len( self.strokes[i].points ) 
            for j in range( 0, num_of_points ):
                point = Point.Point( self.strokes[i].points[j].pid, self.strokes[i].points[j].time, coords[j + ptr, 0], coords[j + ptr, 1] )
                stroke.addPoint(point)                
            ptr += num_of_points
            new_sketch.addStrokes(stroke)
        #return a new sketch
        return new_sketch
    
    # lists the coordinates of all points in the sketch
    def listCoordinates(self):
        xs = []
        ys = []
        
        # add all points of the sketch to a single coords list
        for stroke in self.strokes:
            for point in stroke.points:
                xs.append(point.x)
                ys.append(point.y)
        
        return np.array((np.asarray(xs).T,np.asarray(ys).T)).T
        
    # finds the max. distance from the centroid of the sketch
    def findMaxDistance(self):
        coords = self.listCoordinates()
        
        # find the centroid
        meancoord = np.mean(coords,axis=0)        
        numpoints,numcoords = coords.shape
        
        # find the difference of every point from the centroid
        distances = coords - meancoord ##
        
        return np.max(np.sqrt(np.sum(distances*distances, 1)))
        
    def printContents(self):
        print('Sketch: '+self.sketch_id)
        for stroke in self.strokes:
            print('A stroke')
            for point in stroke.points:
                print(point.time,point.x,point.y)
                
    def toXML(self, name):
        sketch = ET.Element("sketch")
        sketch.attrib["id"] = str(self.sketch_id)

        for stk in self.strokes:
            for pnt in stk.points:
                ET.SubElement(sketch, "point", id = str(pnt.pid), time = str(pnt.time), x = str(pnt.x), y = str(pnt.y))
                
        for stk in self.strokes:
            stroke = ET.SubElement(sketch, "stroke")
            stroke.attrib["id"] = str(stk.sid)
            stroke.attrib["visible"] = "true"
            for pnt in stk.points:
                ET.SubElement(stroke, "arg", type = "point").text = str(pnt.pid)
        
        tree = ET.ElementTree(sketch)
        tree.write( os.path.join(os.getcwd(), 'XMLfiles', 'AfterTraining' , str(name) + ".xml") )
    
    # resamples the sketch before IDM feature extraction        
    def resample(self, ratio, verbose=False):
        if verbose:
            print 'resample: Initialization...'
        
        # init an empty sketch
        newsketch = Sketch(sketch_id='sampled_'+self.sketch_id,strokes=[])
        
        # find the max. distance from the sketch centroid
        maxdist = self.findMaxDistance()*1.01
        
        # find the spatial sampling interval
        interval = maxdist / ratio
        
        if verbose:
            print 'resample: Resampling strokes...'
        
        # for each stroke
        for stroke in self.strokes:
            if verbose:
                print 'resample: On stroke ', stroke.sid
            
            # init an empty stroke
            newstroke = Stroke.Stroke(stroke.sid)
            
            # get the points of stroke
            strokecoords = stroke.listCoordinates()
            
            # construct sample linear points at a given ratio
            prev = np.copy(strokecoords[0])
            pcount = 0
            newstroke.addPoint( Point.Point('p'+str(pcount),pcount,prev[0],prev[1]) )
            pcount = pcount + 1
            strptcount,strptcr = strokecoords.shape
            
            for ptindex in range(1,strptcount):
                sampdif = strokecoords[ptindex] - prev
                sampdistance = np.sqrt(np.dot(sampdif.T,sampdif))
                
                while sampdistance > interval:
                    c = np.copy(prev)
                    angle = math.atan2(strokecoords[ptindex,1] - c[1], strokecoords[ptindex,0] - c[0])
                    newx = c[0] + math.cos(angle)*interval
                    newy = c[1] + math.sin(angle)*interval
                    prev = [newx, newy]
                    newstroke.addPoint( Point.Point('p'+str(pcount),pcount,newx,newy) )
                    pcount = pcount + 1
                    sampdif = strokecoords[ptindex] - prev
                    sampdistance = np.sqrt(np.dot(sampdif.T,sampdif))
                    
            newsketch.addStrokes(newstroke)
        
        if verbose:
            plt.figure(1)
            plt.subplot(211)
            allpts = newsketch.listCoordinates()
            plt.plot(allpts[:,0],allpts[:,1], '.')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('New Sketch with Sampled Points')
            plt.subplot(212)
            allpts = self.listCoordinates()
            plt.plot(allpts[:,0],allpts[:,1], '.')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Old Sketch')
            newsketch.printContents()
        
        return newsketch
        
    def plotSketch(self):
        plt.figure(1)
        allpts = self.listCoordinates()
        plt.plot(allpts[:,0],allpts[:,1])
        plt.xlabel('x')
        plt.ylabel('y')
        
    def saveStrokesToXML(self):
        strokeSketches = []
        for ind in range(0, len(self.strokes)):
            sketch = Sketch(str( uuid.uuid4() ), strokes = [])
            sketch.addStrokes(self.strokes[ind])
            strokeSketches.append(sketch)
            name = "stroke" + str(ind)
            sketch.toXML(name)
        return strokeSketches
        
    def getMean(self):
        ''' Return mean of all points as and (x, y) tuple
        '''
        coords = self.listCoordinates()
        mean = np.mean(coords, axis = 0)
        return mean
        
    def getMaxPoints(self):
        '''Return (X, Y) tuple with maximum Y point
        and return indices of maximum X and Y
        '''
        coords = self.listCoordinates()
        index = np.argmax(coords, axis = 0)
        value = coords[index[1]]
        
        return index, value
        
    def getMinPoints(self):
        '''Return (X, Y) tuple with minimum Y point
        and return indices of minimum X and Y
        '''
        coords = self.listCoordinates()
        index = np.argmin(coords, axis = 0)
        value = coords[index[1]]
        
        return index, value
        
    def getDiameter(self):
        ''' Return the diameter of the Sketch 
        '''
        coords = self.listCoordinates()
        indMax = np.argmax(coords, axis = 0)
        indMin = np.argmin(coords, axis = 0)
        dX = np.absolute(coords[indMax[0]] - coords[indMin[0]]) 
        dY = np.absolute(coords[indMax[1]] - coords[indMin[1]])
        dX = np.sqrt(np.sum(dX*dX)) 
        dY = np.sqrt(np.sum(dY*dY))
        if(dX > dY):
            return dX
        else:
            return dY
