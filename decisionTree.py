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

el_dataPath = '/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'

def setMskValue(inArray):
    outArray = inArray.copy()
    outArray[outArray == 0] = -9999
    outArray[outArray < -999] = -9999
    return outArray


def readBands(filepath):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    df_hh = file.read(1)
    df_hv = file.read(2)
    HH_nan = setMskValue(df_hh)
    HV_nan = setMskValue(df_hv)
    return HH_nan, HV_nan

## reading input rasters

#----INPUT data
# DEM
# tifs of satellite img


#---TARGET DEFINITION file---
#geology groups
targetFile_dir = '/Volumes/ElementsSE/thesisData/Datasets/geologicalMap/'
target_f = 'geolTypesRaster_12600.tif'
target_raster = rio.open(targetFile_dir+target_f)
target_arr = target_raster.read(1)
target_arr_nan = setMskValue(target_arr)
#---TEST data---



# Training decision tree
clf = tree.DecisionTreeClassifier(random_state=0, max_depth=5)
#clf.fit(X,y)

# with HH
# with HV

# plot decision tree
#tree.plot_tree(clf)


