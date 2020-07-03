#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:59:04 2020

@author: GalinaJonat
"""
from colour import Color
import matplotlib
import matplotlib.pyplot as plt

blue = Color('#00338D')
azure = Color('#0098DB')
green = Color('#008542')
orange = Color('#E37222')
read = Color('#D0103A')
yelow = Color('#FDC82F')

colorList = ['#00338D','#0098DB','#008542','#E37222','#D0103A','#FDC82F']
cMap = matplotlib.colors.ListedColormap(colorList)