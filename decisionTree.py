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
import gdal
from rasterio.crs import CRS
from rasterio.transform import Affine
from examineGeologz import geolNames

# decision tree
from sklearn import tree
import graphviz # to visualise graph


geolNames[-9999]='NaN'

win_dataPath = r'C://Users/galinavj/OneDrive - NTNU/thesisAnalysis/DecisionTreeFiles'

el_dataPath = '/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'

decisionTree_folder =  '/Volumes/ElementsSE/thesisData/decisionTrees/'

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
def readTargetFile():
    targetFile_dir = '/Volumes/ElementsSE/thesisData/Datasets/geologicalMap/'
    target_f = 'geolTypesRaster_12600.tif'
    target_raster = rio.open(targetFile_dir+target_f)
    target_arr = target_raster.read(1)
    target_arr_nan = setMskValue(target_arr)
    target_msk_flat = target_arr_nan.flatten()
    return target_msk_flat


target_msk_flat = readTargetFile()
#---TEST data---
inDir = '/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'
inFile = 'FCC_Sigma0_HHHV_20191009_clipped_msk_12600.tif'

def readAndStackBands(fp):
    hh_msk,hv_msk = readBands(fp)
    
    hh_msk_flat = hh_msk.flatten()
    hv_msk_flat = hv_msk.flatten()
    
    # stack hh hv arrays as input features for classification
    hhhv_stacked = np.stack((hh_msk_flat,hv_msk_flat),axis=1)
    return hhhv_stacked

def decTreeHHHV(fp=inDir+inFile,targetMsk=target_msk_flat,tree_depth=3):
    # reading bands, flatting them and preparing them for classification
    hhhv_stacked=readAndStackBands(fp)
    
    # Training decision tree
    clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth)
    clf.fit(hhhv_stacked,targetMsk)
    
    
    # to visualise
    clf_classes = clf.classes_
    classNames = []
    for c in clf_classes:
        classNames.append(geolNames[c])
        
    
    clfTree_hhhv_dot = tree.export_graphviz(clf,feature_names=['HH','HV'],class_names=classNames)
    
    graph = graphviz.Source(clfTree_hhhv_dot)
    
    return clf, graph


def predictFromTree(inFp, dtree,outfn):
    hhhv_stacked = readAndStackBands(inFp)
    pred = dtree.predict(hhhv_stacked)
    pred_reshaped = pred.reshape(-1,11908)
    meta_outFile = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0, 'width': 11908, 'height': 12600, 'count': 1, 'crs': CRS.from_epsg(3413), 'transform': Affine(10.0, 0.0, -384702.1263054441,
           0.0, -10.0, -2122443.806211936)}
    with rio.open(decisionTree_folder+outfn,'w',**meta_outFile) as outTif:
        outTif.write(pred_reshaped,indexes=1)


# with HH
# with HV
def predictExample():
    # plot decision tree
    #tree.plot_tree(clf)
    decTreeOct9_3,graphOct9_3 = decTreeHHHV()
    hhhv_stacked_Oct21 = readAndStackBands(inDir+'FCC_Sigma0_HHHV_20191021_clipped_msk_12600.tif')
    predOct21 = decTreeOct9_3.predict(hhhv_stacked_Oct21)
    predOct21_reshaped = predOct21.reshape(-1,11908)
    
    hhhv_stacked_Dec08 = readAndStackBands(inDir+'FCC_Sigma0_HHHV_20191208_clipped_msk_12600.tif')
    predDec08 = decTreeOct9_3.predict(hhhv_stacked_Dec08)
    predDec08_reshaped = predDec08.reshape(-1,11908)
    ###EXAMPLE OCTOBER 2019####
    meta_outFile = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0, 'width': 11908, 'height': 12600, 'count': 1, 'crs': CRS.from_epsg(3413), 'transform': Affine(10.0, 0.0, -384702.1263054441,
           0.0, -10.0, -2122443.806211936)}
    with rio.open(decisionTree_folder+'Oct21pred-tree_3_new.tif','w',**meta_outFile) as outTif:
        outTif.write(predOct21_reshaped,indexes=1)
        
    with rio.open(decisionTree_folder+'Dec08pred-tree_3_new.tif','w',**meta_outFile) as outTif:
        outTif.write(predDec08_reshaped,indexes=1)
    return decTreeOct9_3,graphOct9_3

