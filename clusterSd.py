#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 15:54:52 2020

@author: GalinaJonat
"""

# standard deviation:: https://docs.python.org/3/library/statistics.html
import statistics
import rasterio as rio
import numpy as np

folder='/Volumes/ElementsSE/thesisData/toHist/mskClipped/'

img1 = folder+"FCC_Sigma0_HHHV_20190412_clipped_msk.tif"
clustersImg1 = folder+"clusters/FCC_Sigma0_HHHV_20190412_clipped_msk_clustersHH.data/class_indices.img"
# read rasters to array

def readBands(filepath,pol=''):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    if (pol == 'HH' or pol==''): # hh bands or clusters
        a = file.read(1)
    elif pol == 'HV':
        a = file.read(2) # hv band
    a_nan = nansInArray(a)
    return a
    #a[~np.isnan(a).all(axis=1)] # remove rows in which all values are nan

def nansInArray(inArray):
    outArray = inArray.astype('float32')
    outArray[outArray == 0] = np.nan
    outArray[outArray < -999] = np.nan
    return outArray



clusterloc = {}
for i in range(1,7): # for clusters 1-6: 
    #dict with locations of cluster pixels




# apply cluster pic to orig imag --> extract list of values in cluster
# calculate standard deviation