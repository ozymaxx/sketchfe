# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 18:05:21 2016

@author: kurmanbek & ozan
oaltiok15@ku.edu.tr
kkaiyrbekov15@ku.edu.tr
"""
import xml.etree.ElementTree as ET
import Point
import Stroke
import Sketch

#Extracts a sketch from an XML
def extractFromXML( string ):
    root = ET.fromstring( string )
    points = getPoints(root)
    strokes = getStrokes(points, root)
    sketch = Sketch.Sketch( root.get('id'), strokes)
    return sketch

#Gets all points from an XML file  
def getPoints( root ):
    points = dict()
    #for each point insert point data to dictionary
    for child in root:
        if child.tag == 'point':
            pid = child.get('id')
            x = child.get('x')
            y = child.get('y')
            t = child.get('time')
            points[pid] = Point.Point( pid, float(t), float(x), float(y) )
    
    return points

#Gets all strokes with corresponding points from XML file
def getStrokes(points, root):
    strokes = []
    #find all stroke elements
    for st in root.findall('stroke'):
        stroke_id = st.get('id')
        stroke = Stroke.Stroke( stroke_id )
        #for each stroke get point id's
        for pnt in st.findall('arg'):
            pid = pnt.text
            stroke.addPoint( points[pid] )
        strokes.append( stroke )
        
    return strokes
    
# a basic tester method
def test():
    str2 = '''<sketch id="asdasd">
                <point id="qwe" y="9" x="1" time="4.6" />
                <point id="aty" y="5" x="6" time="8" />
                <point id="uio" y="44.4" x="10.2" time="9" />
                <point id="asd" y="77" x="3" time="12" />
                <point id="cvb" y="7" x="5" time="13" />
                <stroke id="1">
                    <arg type="point">qwe</arg>
                    <arg type="point">aty</arg>
                </stroke>
                <stroke id="21">
                    <arg type="point">uio</arg>
                    <arg type="point">asd</arg>
                    <arg type="point">cvb</arg>
                </stroke>
            </sketch>'''
    sketch2 = extractFromXML(str2)
    
    print('Sketch 2')
    for stroke in sketch2.strokes:
        print('A stroke')
        for point in stroke.points:
            print(point.time,point.x,point.y)
	
	return sketch2
