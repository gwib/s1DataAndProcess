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
import os
import datetime as dt
import fnmatch

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
    return a_nan
    #a[~np.isnan(a).all(axis=1)] # remove rows in which all values are nan

def nansInArray(inArray):
    outArray = inArray.astype('float32')
    outArray[outArray == 0] = np.nan
    outArray[outArray < -999] = np.nan
    return outArray

#dict with locations of cluster pixels
def clusterPol(cluster_array, pol_array):
    clusterloc = {}
    for cl in range(1,7): # for clusters 1-6:
        # identify rows and columns with value in this cluster
        r,c = np.where(cluster_array == cl)
        # extract polarisation values of clusters in list
        l_cluster = []
        for i in range(0,len(r)):
            l_cluster.append(pol_array[r[i],c[i]])
            
        clusterloc[cl] = l_cluster
        
    return clusterloc
        
# standard deviation for each cluster 
def sdDict(clusterPolDict):
    sdDict = {}
    for k in clusterPolDict.keys():
        sdDict[k] = np.std(clusterPolDict[k])

    return sdDict

# extracting date from filename
def dateFromFilename(fn,dloc=1):
    #s1 = os.path.split(fn)[-1]
    s_tuple = fn.split('_')
    print(s_tuple)
    d_str = fnmatch.filter(s_tuple, '20*')[0]
    d_dt = dt.datetime.strptime(d_str, '%Y%m%d')
    return d_dt

# apply cluster pic to orig imag --> extract list of values in cluster
# calculate standard deviation


# ---WORKFLOW---
# im = readBand(fpImg,pol)
#cl = readBand(fpImg,'')
#polClusterDict = clusterPol(cluster_df, pol_df)
#sdDictPrCluster = sdDict(polClusterDict)


def workAll(inFolder,pol):
    polAll = {}
    clusterAll = {}
    for f in os.listdir(inFolder):
        if f.endswith('.tif'):
            d = dateFromFilename(f)
            clustersFp = inFolder+'/clusters/'+f.split('.')[0]+'_clusters'+pol+'.data/class_indices.img'
            im=readBands(inFolder+f)
            cl=readBands(clustersFp)
            polClusterDict = clusterPol(cl, im)
            sdDictPrCluster = sdDict(polClusterDict)
            polAll[d] = polClusterDict
            clusterAll[d] = sdDictPrCluster
            
    return polAll, clusterAll