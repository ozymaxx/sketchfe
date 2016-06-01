# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 13:08:45 2016

@author: kurmanbek & ozan
oaltiok15@ku.edu.tr
kkaiyrbekov15@ku.edu.tr
"""

# an abstraction of a sketch point
class Point:
    def __init__(self, pid, time, x, y ):
        self.pid = pid
        self.time = time
        self.x = x
        self.y = y
