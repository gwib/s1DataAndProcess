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

filepath = '/Volumes/ElementsSE/thesisData/FCCbatch/FCC_Sigma0_HHHV_20190412.tif'

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

def plotHistogramsForTif(filepath):
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
    
        ax1.get_shared_x_axes().join(ax1, ax2)
        ax1.set_xticklabels([])
        # ax2.autoscale() ## call autoscale if needed
        
    plt.show()
