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
red = Color('#D0103A')
yellow = Color('#FDC82F')

colorDict = {}
colorDict['darkblue'] = '#002664'
colorDict['darkAzure'] = '#00549f'
colorDict['darkGreen'] = '#284e36'
colorDict['darkOrange'] = '#9d5116'
colorDict['darkRed'] = '#B22433'
colorDict['darkYellow'] = '#b88b00'

colorDict['black15'] = '#d5d6d2'
colorDict['black45'] = '#9a9b9c'
colorDict['black75'] = '#747678'
colorDict['black85'] = '#4d4f53'
colorDict['black'] = '#000000'

primColorNames = ['blue', 'azure', 'green', 'orange', 'red', 'yellow']
primColorList = ['#00338D','#0098DB','#008542','#E37222','#D0103A','#FDC82F']
cMap = matplotlib.colors.LinearSegmentedColormap.from_list("", primColorList)

for i in range(len(primColorNames)):
    colorDict[primColorNames[i]] = primColorList[i]

