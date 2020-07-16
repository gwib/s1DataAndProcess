# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:30:29 2020

@author: galinavj
"""
import rasterio as rio
import matplotlib.pyplot as plt
#import rasterio.warp as warp
#import rasterio.plot as rioPlt
import numpy as np
import re
import os
from pathlib import Path
from colours import cMap

# decision tree
from sklearn import tree
import graphviz # to visualise graph

win_dataPath = r'C://Users/galinavj/OneDrive - NTNU/thesisAnalysis/DecisionTreeFiles'

#dem_f =
def readBands(filepath):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    file_HH = file.read(1)
    file_HV = file.read(2)
    #HH_nan = removeNansFromArray(file_HH)
    #HV_nan = removeNansFromArray(file_HV)
    return HH_nan, HV_nan

## reading input rasters

#----INPUT data
# DEM
# tifs of satellite img

#---TARGET DEFINITION file---
#geology groups


#---TEST data---



# Training decision tree
clf = tree.DecisionTreeClassifier(random_state=0, max_depth=5)
clf.fit(X,y)

# with HH
# with HV

# plot decision tree
tree.plot_tree(clf)


