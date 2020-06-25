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
from colours import cMap


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
    return outArray

def dateFromFilename(fn):
    s1 = fn.split('_')[-2]
    s2 = s1.split('.')[0]
    return s2

def plotHistogramsForTif(filepath, targetDir=''):
    
    if len(targetDir) < 1:
        targetDir = os.path.dirname(filepath)+'/hist/'
    
    splitDate = dateFromFilename(os.path.split(filepath)[-1])
    print(splitDate)
    figName = targetDir+'hist_'+splitDate[3]+'.png'
    
    HH, HV = readBands(filepath)
    
    if np.isnan(HV).all():
        raise Exception('HV band of file '+filepath+' is empty! \n Plotting histogram for HH band only')
        plt.hist(HH)
        plt.title('HH reflection histogram for the entire image')
    else:
        # subplot with shared x-axis
        fig=plt.figure()
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        
        ax1.hist(HH)
        ax2.hist(HV)
        
        ax1.set_title('HH polarisation')
        ax2.set_title('HV polarisation')
        
        fig.suptitle('Histogram for polarisation on '+splitDate, fontsize=14)
    
        ax1.get_shared_x_axes().join(ax1, ax2)
        ax1.set_xticklabels([])
        # ax2.autoscale() ## call autoscale if needed
        
    plt.show()
    Path(targetDir).mkdir(parents=True, exist_ok=True)
    
    
    plt.savefig(figName)
