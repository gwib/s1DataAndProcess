#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 13:54:06 2020

@author: GalinaJonat
"""

import rasterio as rio
import matplotlib.pyplot as plt
#import rasterio.warp as warp
#import rasterio.plot as rioPlt
import numpy as np
import re
import os
from pathlib import Path
from colours import cMap,colorDict
import fnmatch
import datetime as dt


#filepath = '/Volumes/ElementsSE/thesisData/FCCbatch/FCC_Sigma0_HHHV_20190412.tif'
targetDir = '/Volumes/ElementsSE/thesisData/hist/'

def readBands(filepath):
    file = rio.open(filepath)
    print('----File Information ----')
    print(file.meta)
    file_HH = file.read(1)
    file_HV = file.read(2)
    HH_nan = removeNansFromArray(file_HH)
    HV_nan = removeNansFromArray(file_HV)
    return HH_nan, HV_nan
    
    
    
def removeNansFromArray(inArray):
    outArray = inArray.copy()
    outArray[outArray == 0] = np.nan
    outArray[outArray < -999] = np.nan
    return outArray

# extracting date from filename
def dateFromFilename(fn,dloc=1):
    #s1 = os.path.split(fn)[-1]
    s_tuple = fn.split('_')
    d_str = fnmatch.filter(s_tuple, '20*')[0]
    d_dt = dt.datetime.strptime(d_str, '%Y%m%d')
    return d_dt

# =============================================================================
# def dateFromFilename(fn):
#     s1 = fn.split('_')[-2]
#     s2 = s1.split('.')[0]
#     return s2
# =============================================================================

def plotHistogramsForTif(filepath, targetDir=''):
    
    if len(targetDir) < 1:
        targetDir = os.path.dirname(filepath)+'/hist/'
    
    splitDate = dateFromFilename(os.path.split(filepath)[-1])
    print(splitDate)
    figName = targetDir+'hist_'+str(splitDate.date())+'.pdf'
    print(figName)
    HH, HV = readBands(filepath)
    # flatten tif values, such that histogram can be in one colour

    HH_flat = HH.flatten()
    HV_flat = HV.flatten()
    
    if np.isnan(HV).all():
        raise Exception('HV band of file '+filepath+' is empty! \n Plotting histogram for HH band only')
        plt.hist(HH_flat,color=colorDict['green'])
        plt.ylabel('Pixel Count')
        plt.xlabel('HH backscatter ([$\sigma_0$]==dB)')
        #plt.title('HH reflection histogram for the entire image')
    else:
        # subplot with shared x-axis
        fig=plt.figure(dpi=200)
        ax1, ax2 = fig.subplots(2)
        #ax1 = fig.subplot(211)
        #ax2 = fig.subplot(212)
        
        ax1.hist(HH_flat,color=colorDict['green'], bins=12)
        ax2.hist(HV_flat,color=colorDict['orange'], bins=12)
        
        ax1.set_xlabel('HH backscatter ([$\sigma_0$] = dB)')
        ax2.set_xlabel('HV backscatter ([$\sigma_0$] = dB)')
        ax1.set_ylabel('Pixel Count')
        ax2.set_ylabel('Pixel Count')
        #fig.suptitle('Histogram for polarisation on '+str(splitDate.date()), fontsize=14)
        
        ax1.get_shared_x_axes().join(ax1, ax2)
        #ax1.set_xticklabels([])
        # ax2.autoscale() ## call autoscale if needed
    
    fig.subplots_adjust(hspace=0.42, bottom=0.15)
    plt.show()
    Path(targetDir).mkdir(parents=True, exist_ok=True)
    
    
    plt.savefig(figName)
    
def histForPols(inFolder,histFolder):
    for f in os.listdir(inFolder):
        if f.endswith('.tif'):
            plotHistogramsForTif(inFolder+'/'+f,histFolder)


#TODO:
    # histogram between HH/HV ratio