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
    print(fn)
    s_tuple = fn.split('_')
    print(s_tuple)
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

def histForEachPol(fp,targetDir):
    if len(targetDir) < 1:
        targetDir = os.path.dirname(fp)+'/hist/'
    Path(targetDir).mkdir(parents=True, exist_ok=True)
    splitDate = dateFromFilename(os.path.split(fp)[-1])
    print(splitDate)
    
    HH, HV = readBands(fp)
    HH_flat = HH.flatten()
    HV_flat = HV.flatten()
    
    if np.isnan(HV).all():
        figName = targetDir+'hist_'+str(splitDate.date())+'_HH.pdf'
        raise Exception('HV band of file '+fp+' is empty! \n Plotting histogram for HH band only')
        plt.hist(HH_flat,color=colorDict['green'])
        plt.ylabel('Pixel Count')
        plt.xlabel('HH backscatter ([$\sigma_0$]=dB)')
        plt.savefig(figName)
        plt.show()
        return
    else:
        HH_flat_nonan =  HH_flat[~ np.isnan(HH_flat)]
        HV_flat_nonan =  HV_flat[~ np.isnan(HV_flat)]
        
        HH_flat = HH_flat_nonan
        HV_flat = HV_flat_nonan
        #print(np.histogram(HH_flat))
        # HH histogram
        fig_HH = plt.figure(dpi=200)
        ax_HH = fig_HH.subplots(1)
        ax_HH.hist(HH_flat,color=colorDict['green'])#, bins=12)
        #ax_HH.hist(HH)
        ax_HH.set_xlim(-32,13)
        ax_HH.set_ylim(0,3.55e7)
        ax_HH.set_xlabel('HH backscatter ([$\sigma_0$] = dB)')
        ax_HH.set_ylabel('Pixel Count')
        fig_HH.subplots_adjust(bottom=0.24)
        plt.show()
        
        # HV histogram
        fig_HV = plt.figure(dpi=200)
        ax_HV = fig_HV.subplots(1)
        ax_HV.hist(HV_flat,color=colorDict['orange'])#, bins=12)
        ax_HV.set_xlim(-32,13)
        ax_HV.set_ylim(0,3.55e7)
        ax_HV.set_xlabel('HV backscatter ([$\sigma_0$] = dB)')
        ax_HV.set_ylabel('Pixel Count')
        fig_HV.subplots_adjust(bottom=0.24)
        plt.show()
        
        # HH-HV ratio
        HHHVratio = HH - HV
        HHHV_flat = HHHVratio.flatten()
        
        # plot
        fig_HHHV = plt.figure(dpi=200)
        ax_HHHV = fig_HHHV.subplots(1)
        ax_HHHV.hist(HHHV_flat,color=colorDict['darkYellow'])
        ax_HHHV.set_xlim(0,30)
        ax_HHHV.set_ylim(0,6e7)
        ax_HHHV.set_xlabel('HH/HV backscatter ratio ([$\sigma_0$] = dB)')
        ax_HHHV.set_ylabel('Pixel Count')
        fig_HHHV.subplots_adjust(bottom=0.24)
        plt.show()
        
        figName_HH = targetDir+'hist_'+str(splitDate.date())+'_HH.pdf'
        figName_HV = targetDir+'hist_'+str(splitDate.date())+'_HV.pdf'
        figName_HHHV = targetDir+'hist_'+str(splitDate.date())+'_HHHV.pdf'
    
    fig_HH.savefig(figName_HH)
    fig_HV.savefig(figName_HV)
    fig_HHHV.savefig(figName_HHHV)

def histForPols(inFolder,histFolder):
    for f in os.listdir(inFolder):
        if f.endswith('.tif'):
            plotHistogramsForTif(inFolder+'/'+f,histFolder)

def histForEachPols2(inFolder, histFolder):
    for f in os.listdir(inFolder):
        if f.endswith('.tif'):
            histForEachPol(inFolder+f, histFolder)

#TODO:
    # histogram between HH/HV ratio