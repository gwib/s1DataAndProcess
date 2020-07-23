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

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split


geolNames[-9999]='NaN'

win_dataPath = r'C://Users/galinavj/OneDrive - NTNU/thesisAnalysis/DecisionTreeFiles'

el_dataPath = '/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'

decisionTree_folder =  '/Volumes/ElementsSE/thesisData/decisionTrees/'

def setMskValue(inArray):
    #print('setting mask value')
    outArray = inArray.copy()
    outArray[np.isnan(outArray)] = -9999
    outArray[outArray == 0] = -9999
    outArray[outArray < -999] = -9999
    outArray = np.nan_to_num(outArray, nan=-9999,posinf=-9999,neginf=-9999)
    return outArray


def readBands(filepath):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    df_hh = file.read(1)
    df_hv = file.read(2)
    HH_nan = setMskValue(df_hh)
    HV_nan = setMskValue(df_hv)
    HH_non = np.nan_to_num(HH_nan, nan=-9999,posinf=-9999,neginf=-9999)
    #HH_non[np.isnan(HH_non)] = -9999
    HV_non = np.nan_to_num(HV_nan, nan=-9999,posinf=-9999,neginf=-9999)
    #HV_non[np.isnan(HV_non)] = -9999
    
    return HH_non, HV_non

def readBand(filepath):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    b1_arr = file.read(1)
    b1_nan = setMskValue(b1_arr)
    return b1_nan
## reading input rasters

#----INPUT data
# DEM
# tifs of satellite img
geoFp = '/Volumes/ElementsSE/thesisData/Datasets/geologicalMap/geolTypesRaster_12600.tif' # contains 8 target group plus nan group
binFp = '/Volumes/ElementsSE/thesisData/Datasets/GlacierOutline/glimsBinary_12600.tif'
#---TARGET DEFINITION file---
#geology groups
def readTargetFile(targetFp=geoFp):
    #target_f = 'geolMap_8groups.tif'
    target_raster = rio.open(targetFp)
    target_arr = target_raster.read(1)
    target_arr_nan = setMskValue(target_arr)
    target_msk_flat = target_arr_nan.flatten()
    return target_msk_flat

geo_msk_flat = readTargetFile(geoFp)
bin_msk_raster = rio.open(binFp)
bin_msk_arr = bin_msk_raster.read(1)
binMsk_arr_nan = bin_msk_arr.copy()
binMsk_arr_nan[bin_msk_arr < -999] = -9999
bin_msk_flat = binMsk_arr_nan.flatten()

#---TEST data---
inDir = '/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'
inFile = 'FCC_Sigma0_HHHV_20191009_clipped_msk_12600.tif'


snowProbFile = '/Volumes/ElementsSE/thesisData/validation/s2Mask/maskBool/s2mskAligned_new_12600.tif'
snwMsk = rio.open(snowProbFile)
snwMsk_arr = snwMsk.read(1)
snwprb_flat = snwMsk_arr.flatten()


def readAndStackBands(fp):
    hh_msk,hv_msk = readBands(fp)
    #print('HH read msk contains nan: '+str(np.isnan(hh_msk).any()))
    #print('HV read msk contains nan: '+str(np.isnan(hv_msk).any()))
    hh_msk_flat = hh_msk.flatten()
    hv_msk_flat = hv_msk.flatten()
    
    # --- probably don't need these as nan_to_num is supposed to solve it but keep them just in case ---
    hh_msk_flat_nonan = hh_msk_flat.copy()
    hh_msk_flat_nonan[np.isnan(hh_msk_flat_nonan)] = -9999
    hv_msk_flat_nonan = hv_msk_flat.copy()
    hv_msk_flat_nonan[np.isnan(hv_msk_flat_nonan)] = -9999
    #print('HH contains nan: '+str(np.isnan(hh_msk_flat_nonan).any()))
    #print('HV contains nan: '+str(np.isnan(hv_msk_flat_nonan).any()))
# =============================================================================

    # stack hh hv arrays as input features for classification
    #hhhv_stacked = np.stack((hh_msk_flat,hv_msk_flat),axis=1)
    hhhv_stacked = np.stack((hh_msk_flat_nonan,hv_msk_flat_nonan),axis=1)
    return hhhv_stacked

def readAndStackBandsInclSnwProb(fp,snwprobfp=''):
    if len(snwprobfp)<3:
        snwprob_flat = snwprb_flat
    else:
        snwprb = rio.open(snwprobfp)
        snwprb_arr = snwprb.read(1)
        snwprob_flat = snwprb_arr.flatten()
    
    hh_msk,hv_msk = readBands(fp)
    
    hh_msk_flat = hh_msk.flatten()
    hv_msk_flat = hv_msk.flatten()
    
    # stack hh hv arrays as input features for classification
    stacked = np.stack((hh_msk_flat,hv_msk_flat,snwprob_flat),axis=1)
    return stacked

def decTreeHHHV(fp=inDir+inFile,targetMsk=geo_msk_flat,tree_depth=3,b=True):
    # reading bands, flatting them and preparing them for classification
    hhhv_stacked=readAndStackBands(fp)
    
    # Training decision tree
    if b==True:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth,class_weight='balanced')
        clf.fit(hhhv_stacked,targetMsk)
    else:
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

def decTreeHHHVsnwprb(fp=inDir+inFile,targetMsk=bin_msk_flat,tree_depth=3,b=True):
    stacked = readAndStackBandsInclSnwProb(fp,snwprobfp='')
        # Training decision tree
    if b==True:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth,class_weight='balanced')
        clf.fit(stacked,targetMsk)
    else:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth)
        clf.fit(stacked,targetMsk)
    
    
    # to visualise
    clf_classes = clf.classes_
    classNames = []
    if len(clf_classes) > 4:
        for c in clf_classes:
            classNames.append(geolNames[c])
    else:
        classNames = ['NULL','Not Ice', 'Ice']
        
    
    clfTree_hhhv_dot = tree.export_graphviz(clf,feature_names=['HH','HV', 'Snow Probability'],class_names=classNames)
    
    graph = graphviz.Source(clfTree_hhhv_dot)
    
    return clf, graph

def predictFromTree(inFp, dtree,outfn):
    hhhv_stacked = readAndStackBands(inFp)
    pred = dtree.predict(hhhv_stacked)
    pred_reshaped = pred.reshape(-1,11908)
    meta_outFile = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0, 'width': 11908, 'height': 12600, 'count': 1, 'crs': CRS.from_epsg(3413), 'transform': Affine(10.0, 0.0, -384702.1263054441,
           0.0, -10.0, -2122443.806211936)}
    with rio.open(outfn,'w',**meta_outFile) as outTif:
        outTif.write(pred_reshaped,indexes=1)

def predictFromTreeSnwprb(inFp, dtree,outfn,snwPrbfp=''):
    hhhv_stacked = readAndStackBandsInclSnwProb(inFp)
    pred = dtree.predict(hhhv_stacked)
    pred_reshaped = pred.reshape(-1,11908)
    meta_outFile = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0, 'width': 11908, 'height': 12600, 'count': 1, 'crs': CRS.from_epsg(3413), 'transform': Affine(10.0, 0.0, -384702.1263054441,
           0.0, -10.0, -2122443.806211936)}
    with rio.open(outfn,'w',**meta_outFile) as outTif:
        outTif.write(pred_reshaped,indexes=1)



def treeWithCrossVal(fp=inDir+inFile,target=bin_msk_flat,tree_depth=3,b=True):
    hhhv_stacked=readAndStackBands(fp)
    # split data in training and test set
    X_train, X_test, y_train, y_test = train_test_split(hhhv_stacked,target,test_size=0.33, random_state=13)
    #print(set(X_train[0]))
    if b==True:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth,class_weight='balanced')
        clf.fit(X_train,y_train)
    else:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth)
        clf.fit(X_train,y_train)
        
    print('--Cross validation score for tree with depth '+str(tree_depth)+' on training file '+fp+'--')
    print(cross_val_score(clf, X_test, y_test))
    
        # to visualise
    clf_classes = clf.classes_
    classNames = []
    if len(clf_classes) > 4:
        for c in clf_classes:
            classNames.append(geolNames[c])
    else:
        classNames = ['NULL','Not Ice', 'Ice']
    
    clfTree_dot = tree.export_graphviz(clf,feature_names=['HH','HV'],class_names=classNames)
    
    graph = graphviz.Source(clfTree_dot)
    
    return clf, graph

dem_fp = '/Volumes/ElementsSE/thesisData/Datasets/DEM/arcticDEM_10m_12600.tif'
dem = readBand(dem_fp)
dem_flat = dem.flatten()

def treeCrossValInclDEM(fp=inDir+inFile,target=bin_msk_flat,tree_depth=3,b=True):
    hh_msk,hv_msk = readBands(fp)
    #print('HH read msk contains nan: '+str(np.isnan(hh_msk).any()))
    #print('HV read msk contains nan: '+str(np.isnan(hv_msk).any()))
    hh_msk_flat = hh_msk.flatten()
    hv_msk_flat = hv_msk.flatten()
    
    hhhvDEM_stacked = np.stack((hh_msk_flat,hv_msk_flat,dem_flat),axis=1)
    # split data in training and test set
    X_train, X_test, y_train, y_test = train_test_split(hhhvDEM_stacked,target,test_size=0.33, random_state=13)
    #print(set(X_train[0]))
    if b==True:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth,class_weight='balanced')
        clf.fit(X_train,y_train)
    else:
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=tree_depth)
        clf.fit(X_train,y_train)
        
    print('--Cross validation score for tree with depth '+str(tree_depth)+' on training file '+fp+'--')
    print(cross_val_score(clf, X_test, y_test))
    
        # to visualise
    clf_classes = clf.classes_
    classNames = []
    if len(clf_classes) > 4:
        for c in clf_classes:
            classNames.append(geolNames[c])
    else:
        classNames = ['NULL','Not Ice', 'Ice']
    
    clfTree_dot = tree.export_graphviz(clf,feature_names=['HH','HV','DEM'],class_names=classNames)
    
    graph = graphviz.Source(clfTree_dot)
    
    return clf, graph

def predictFromTreeDEM(fp, dtree,outfn):
    hh_msk,hv_msk = readBands(fp)
    #print('HH read msk contains nan: '+str(np.isnan(hh_msk).any()))
    #print('HV read msk contains nan: '+str(np.isnan(hv_msk).any()))
    hh_msk_flat = hh_msk.flatten()
    hv_msk_flat = hv_msk.flatten()
    
    hhhvDEM_stacked = np.stack((hh_msk_flat,hv_msk_flat,dem_flat),axis=1)
    pred = dtree.predict(hhhvDEM_stacked)
    pred_reshaped = pred.reshape(-1,11908)
    meta_outFile = {'driver': 'GTiff', 'dtype': 'float32', 'nodata': -9999.0, 'width': 11908, 'height': 12600, 'count': 1, 'crs': CRS.from_epsg(3413), 'transform': Affine(10.0, 0.0, -384702.1263054441,
           0.0, -10.0, -2122443.806211936)}
    with rio.open(outfn,'w',**meta_outFile) as outTif:
        outTif.write(pred_reshaped,indexes=1)
