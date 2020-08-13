#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:55:40 2020

@author: GalinaJonat
"""
import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
import os
#from colours import colorList, cMap
#from colour import Color
import fnmatch
import datetime as dt
from colours import colorDict
### predefined vars
#mskFile = '/Volumes/ElementsSE/thesisData/validation/s2Mask/maskBool/aligned_s2Mask.tif'
mskFile = '/Volumes/ElementsSE/thesisData/validation/s2Mask/maskBool/s2mskAligned_new_12600.tif'
glimsMsk_fp = '/Volumes/ElementsSE/thesisData/Datasets/GlacierOutline/glimsNodataAndGlac_12600.tif' 
# directory containing clipped tifs
directory = r'/Volumes/ElementsSE/thesisData/FCCclippedMsk2/'

def readSnwPrbMask(fp = mskFile, threshold=60):
    # import and create binary snow mask
    snwPrbMask=rio.open(fp)
    snwPrbMask.meta
    
    a_snwPrb = snwPrbMask.read(1)
    a_snwPrb[a_snwPrb < -1] = np.nan
    #plt.imshow(a_snwPrb)
    
    a_snwMaskBool = a_snwPrb.copy()
    
    # & for element-wise boolean-and
    mask_Zero = (~np.isnan(a_snwPrb)) & (a_snwPrb <= threshold)
    mask_Nan = np.isnan(a_snwPrb)
    a_snwMaskBool = np.ones((a_snwPrb.shape[0],a_snwPrb.shape[1]),dtype=np.float32)
    
    a_snwMaskBool[mask_Zero] = 0
    a_snwMaskBool[mask_Nan] = np.nan
    
    # testplot    
    fig, axs = plt.subplots(1, 2)
    ax1 = axs[0].imshow(a_snwPrb, interpolation='nearest', cmap='pink')
    fig.colorbar(ax1, ax=axs[0])
    ax2 = axs[1].imshow(a_snwMaskBool, interpolation='none', cmap='binary')
    fig.colorbar(ax2, ax=axs[1])
    
    axs[0].set_title('Snow/ice probability mask')
    axs[1].set_title('Boolean snow/ice mask')
    fig.suptitle('Snow/ice mask from Sentinel-2', fontsize=14)
    
    return a_snwPrb, a_snwMaskBool


# extract bands from FCC to dict
# read all files from directory

def meanSdForTifSnowMsk(direc=directory,msk=mskFile):
    # read boolean snow mask
    _, snwBool = readSnwPrbMask(msk) # modify threshold
    print (snwBool.shape)
    hhMeanDict = {}
    hhSdDict = {}
    hvMeanDict = {}
    hvSdDict = {}
    
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            # read fcc file
            p = entry.path
        else: continue
        
        
        splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        #print(splitDate)
        
        date = splitDate.date()
        print(date)
        
        hh, hv = readFcc(p) # original hh and hv with nan values
        #print (hh.shape)
        hhMean, hhSd = calcMeanSd(snwBool, hh)
        
        try:
            hvMean, hvSd = calcMeanSd(snwBool, hv)
        except:
            hvMean = np.nan

        hhMeanDict[date] = hhMean
        hhSdDict[date] = hhSd
            
        hvMeanDict[date] = hvMean
        hvSdDict[date] = hvSd
        
    plotMeanSd(hhMeanDict, hhSdDict, hvMeanDict, hvSdDict)
    
    return hhMeanDict, hhSdDict, hvMeanDict, hvSdDict

def meanSdForGlims(direc=directory,msk=glimsMsk_fp):
    # read boolean snow mask
    glacMsk = rio.open(msk)
    glacMsk_arr = glacMsk.read(1)
    
    hhMeanDict = {}
    hhSdDict = {}
    hvMeanDict = {}
    hvSdDict = {}
    
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            print(entry)
            # read fcc file
            p = entry.path
        else: continue
        
        
        splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        #print(splitDate)
        
        date = splitDate.date()
        print(date)
        
        hh, hv = readFcc(p) # original hh and hv with nan values
        #print (max(hh))
        #print(max(hv))
        hhMean, hhSd = calcMeanSd(glacMsk_arr, hh)
        
        try:
            hvMean, hvSd = calcMeanSd(glacMsk_arr, hv)
        except:
            hvMean = np.nan
            hvSd = np.nan
         
        hhMeanDict[date] = hhMean
        hhSdDict[date] = hhSd
            
        hvMeanDict[date] = hvMean
        hvSdDict[date] = hvSd
        
    plotMeanSd(hhMeanDict, hhSdDict, hvMeanDict, hvSdDict)
    
    return hhMeanDict, hhSdDict, hvMeanDict, hvSdDict


def calcPolRatioGLIMS(direc=directory,msk=glimsMsk_fp):
    # read boolean snow mask
    glacMsk = rio.open(msk)
    glacMsk_arr = glacMsk.read(1)
    
    hhhvMeanDict = {}
    hhhvSdDict = {}

    
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            print(entry)
            # read fcc file
            p = entry.path
        else: continue
        
        
        splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        #print(splitDate)
        
        date = splitDate.date()
        print(date)
        
        hh, hv = readFcc(p) # original hh and hv with nan values
        
        hhhv = hh - hv
        
        hhhvMean, hhhvSd = calcMeanSd(glacMsk_arr, hhhv)

        hhhvMeanDict[date] = hhhvMean
        hhhvSdDict[date] = hhhvSd
        
    plotPolRatio(hhhvMeanDict, hhhvSdDict)

    return hhhvMeanDict, hhhvSdDict

def calcPolRatioSnwMsk(direc=directory,msk=mskFile):
    # read boolean snow mask
    _, snwBool = readSnwPrbMask(msk) # modify threshold
    
    hhhvMeanDict = {}
    hhhvSdDict = {}

    
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            print(entry)
            # read fcc file
            p = entry.path
        else: continue
        
        
        splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        #print(splitDate)
        
        date = splitDate.date()
        print(date)
        
        hh, hv = readFcc(p) # original hh and hv with nan values
        
        hhhv = hh - hv
        
        hhhvMean, hhhvSd = calcMeanSd(snwBool, hhhv)

        hhhvMeanDict[date] = hhhvMean
        hhhvSdDict[date] = hhhvSd
        
    plotPolRatio(hhhvMeanDict, hhhvSdDict)

    return hhhvMeanDict, hhhvSdDict
            
def calcMeanSd(boolMsk, pol):
    # multiply glacier mask with polarisations
    pol_masked = np.multiply(boolMsk, pol)
     
    #extract values for glaciarised areas
    pol_msk_val = extractVals(pol_masked)
        
    # calculate mean and sd for glacierised areas
    polMean = pol_msk_val.mean()
    polSd = pol_msk_val.std()
    
    return polMean, polSd
    

def readFcc(fPath):
    
    fcc = rio.open(fPath)
    #print(fcc.meta) # print metadata
    
    fcc_hh = fcc.read(1)
    
    try: fcc_hv = fcc.read(2)
    except: fcc_hv = np.nan
    
    fcc_hh[fcc_hh == 0] = np.nan
    fcc_hh[fcc_hh < -999] = np.nan
    try:
        fcc_hv[fcc_hv < -999] = np.nan
        fcc_hv[fcc_hv == 0] = np.nan
    except: print('HV not available.')
    
    #plotPols(fcc_hh, fcc_hv, splitDate)
    
    #printMinMax(fcc_hh, fcc_hv)
    
    return fcc_hh, fcc_hv


####### PLOTS ######
def plotPols(hh, hv, date):
    
    # normalizing colormap to constant boundaries
    mynorm = plt.Normalize(vmin=-37, vmax=21) #TODO: numbers are subject to change
    
    fig, axs = plt.subplots(1, 2)
    ax1 = axs[0].imshow(hh, interpolation='nearest', cmap='magma', norm=mynorm)
    fig.colorbar(ax1, ax=axs[0])
    ax2 = axs[1].imshow(hv, interpolation='nearest', cmap='magma', norm=mynorm)
    fig.colorbar(ax2, ax=axs[1])
    
    axs[0].set_title('HH band')
    axs[1].set_title('HV band')
    fig.suptitle('Radiometrically calibrated backscatter from: '+date, fontsize=14)
    
def plotMeanSd(hhMeanDict, hhSdDict, hvMeanDict, hvSdDict, saveFile=''):
    # Create a figure with customized size
    fig,ax = plt.subplots(dpi=200)
    #ax = fig.add_subplot(111)
    
    # Set the axis lables
    #ax.set_xlabel('Date',fontsize=14)
    ax.set_ylabel(r'Mean backscatter in $dB$',fontsize=12)
    
    # X axis is day numbers from 1 to 15
    dates = list(hhMeanDict.keys())
    dates.sort()
    #print(dates)
    xaxis = dates
    
    # Y values
    HHmean_y = []
    HVmean_y = []
    HHsd = []
    HVsd = []
    for d in dates:
        HHmean_y.append(hhMeanDict[d])
        HVmean_y.append(hvMeanDict[d])
        HHsd.append(hhSdDict[d])
        HVsd.append(hvSdDict[d])
    
    # Line color for error bar
    color_HH = colorDict['orange'] # orange
    color_HV = colorDict['green'] # green
    
    # Line style for each dataset
    lineStyle_HH={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    lineStyle_HV={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    
    # Create an error bar for each dataset
    line_HH=ax.errorbar(xaxis, HHmean_y, yerr=HHsd, **lineStyle_HH, color=color_HH, label='HH')
    line_HV=ax.errorbar(xaxis, HVmean_y, yerr=HVsd, **lineStyle_HV, color=color_HV, label='HV')
      
    
    # Draw a legend bar
    plt.legend(handles=[line_HH, line_HV],bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    
    
    # Customize the tickes on the graph
    #plt.xticks(xaxis,rotation=45,fontsize=8)           
    #plt.xlabel('Date',fontsize=10)    
    #plt.yticks(np.arange(20, 47, 2))
    
    # Customize the legend font and handle length
    params = {'legend.fontsize': 12,
              'legend.handlelength': 2}
    plt.rcParams.update(params)

    
    # Draw a grid for the graph
    plt.grid(color=colorDict['black15'])
    
    for ax in fig.get_axes():
        if ax.is_last_row():
            for label in ax.get_xticklabels():
                label.set_ha('right')
                label.set_rotation(30.)
        else:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.set_xlabel('')
    fig.subplots_adjust(bottom=0.2)#bottom=0.34, right=0.15)
    #ax.set_title('Mean Backscatter of glaciarised areas', fontsize=16)
    
    plt.show()
    if len(saveFile) > 0:
        plt.savefig(saveFile)
        
def plotPolRatio(hhhvMeanDict, hhhvSdDict, saveFile=''):
    # Create a figure with customized size
    fig,ax = plt.subplots(dpi=200)
    #ax = fig.add_subplot(111)
    
    # Set the axis lables
    #ax.set_xlabel('Date',fontsize=14)
    ax.set_ylabel(r'Backscatter ratio',fontsize=12)
    
    # X axis is day numbers from 1 to 15
    dates = list(hhhvMeanDict.keys())
    dates.sort()
    #print(dates)
    xaxis = dates
    
    # Y values
    mean_y = []
    sd = []
    for d in dates:
        mean_y.append(hhhvMeanDict[d])
        
        sd.append(hhhvSdDict[d])
    
    # Line color for error bar
    color_HHHV = colorDict['darkYellow'] # orange
    
    # Line style for each dataset
    lineStyle={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    #lineStyle_HV={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    
    # Create an error bar for each dataset
    line=ax.errorbar(xaxis, mean_y, yerr=sd, **lineStyle, color=color_HHHV, label='HH/HV ratio')
   
    
    # Draw a legend bar
    #plt.legend(handles=[line_HH, line_HV],bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    
    
    # Draw a grid for the graph
    plt.grid(color=colorDict['black15'])
    
    for ax in fig.get_axes():
        if ax.is_last_row():
            for label in ax.get_xticklabels():
                label.set_ha('right')
                label.set_rotation(30.)
        else:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.set_xlabel('')
    fig.subplots_adjust(bottom=0.2)#, right=0.05)#bottom=0.34, right=0.15)
    #ax.set_title('Mean Backscatter of glaciarised areas', fontsize=16)
    
    plt.show()
    if len(saveFile) > 0:
        plt.savefig(saveFile)

def plotMeans(hhMeanDict, hvMeanDict):
    hh = []
    hv =  [] 
    dates = list(hhMeanDict.keys())
    dates.sort()
    for d in dates:
        hh.append(hhMeanDict[d])
        hv.append(hvMeanDict[d])
        
    plt.scatter(hh,hv)
    plt.xlabel('HH')
    plt.ylabel('HV')
    plt.show()


def plotMeanDiff(hhMeanDict, hvMeanDict):
    hh = []
    hv = []
    dates = list(hhMeanDict.keys())
    dates.sort()
    for d in dates:
        hh.append(hhMeanDict[d])
        hv.append(hvMeanDict[d])
    hhMinusHv = [a_i - b_i for a_i, b_i in zip(hh, hv)]
    
    fig,ax = plt.subplots(dpi=180)
    ax.plot(dates, hhMinusHv, color=colorDict['darkYellow'])
    plt.grid(color=colorDict['black15'])
    #plt.xticks(dates,rotation=45)
    plt.ylabel(r'HH - HV in $dB$', fontsize=13)
    #plt.ylim(bottom=6,top=10.5)
    
    for ax in fig.get_axes():
        if ax.is_last_row():
            for label in ax.get_xticklabels():
                label.set_ha('right')
                label.set_rotation(30.)
        else:
            for label in ax.get_xticklabels():
                label.set_visible(False)
            ax.set_xlabel('')
    fig.subplots_adjust(bottom=0.15)
    
def maskedHistogram(boolMsk,direc,pltDir):
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            print(entry)
            # read fcc file
            p = entry.path
        else: continue
        
        
        splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        #print(splitDate)
        
        date = splitDate.date()
        print(date)
        
        hh, hv = readFcc(p)
        
        HH_flat = hh.flatten()
        HV_flat = hv.flatten()
    
        if np.isnan(HV_flat).all():
            figName = pltDir+'hist_'+str(splitDate.date())+'_HH.pdf'
            raise Exception('HV band of file '+str(entry)+' is empty! \n Plotting histogram for HH band only')
            np.histogram(HH_flat)
            fig_HH = plt.figure(dpi=200)
            fig_HH.hist(HH_flat,color=colorDict['green'])
            plt.ylabel('Pixel Count')
            plt.xlabel('HH backscatter ([$\sigma_0$]=dB)')
            plt.savefig(figName)
            plt.show()
            return
        else:
            HH_flat_nonan =  HH_flat[~ np.isnan(HH_flat)]
            HV_flat_nonan =  HV_flat[~ np.isnan(HV_flat)]
            print('---HH Hist---')
            print(np.histogram(HH_flat_nonan))
            print('---HV Hist---')
            print(np.histogram(HV_flat_nonan))
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
            HHHVratio = hh - hv
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
            
            figName_HH = pltDir+'glachist_'+str(date)+'_HH.pdf'
            figName_HV = pltDir+'glachist_'+str(date)+'_HV.pdf'
            figName_HHHV = pltDir+'glachist_'+str(date)+'_HHHV.pdf'
        
        fig_HH.savefig(figName_HH)
        fig_HV.savefig(figName_HV)
        fig_HHHV.savefig(figName_HHHV)


    
    
###### HELPER FUNCTIONS #####
def printMinMax(hh, hv):
    hh = hh[~np.isnan(hh)]
    hv = hv[~np.isnan(hv)]

    print ('HH min: '+ str(hh.min()))
    print ('HH max: '+ str(hh.max()))
    print ('HV min: '+ str(hv.min()))
    print ('HV max: '+ str(hv.max()))

def extractVals(a):
    a_Val = a[(~np.isnan(a)) & (a !=0)] # extract values that are neither nan or zero
    return a_Val

# extracting date from filename
def dateFromFilename(fn,dloc=1):
    #s1 = os.path.split(fn)[-1]
    s_tuple = fn.split('_')
    d_str = fnmatch.filter(s_tuple, '20*')[0]
    d_dt = dt.datetime.strptime(d_str, '%Y%m%d')
    return d_dt


# define binary colormap
def binCmap(base_cmap):
    base = plt.cm.get_cmap(base_cmap)
    N=2
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)

