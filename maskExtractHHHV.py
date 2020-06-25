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
from colours import cMap

### predefined vars
mskFile = '/Volumes/ElementsSE/thesisData/validation/s2Mask/maskBool/aligned_s2Mask.tif'
#for testing purposes
fccPath = '/Volumes/ElementsSE/thesisData/FCCbatch_clipped/FCC_Sigma0_HHHV_20190412_clipped.tif'
# directory containing clipped tifs
directory = r'/Volumes/ElementsSE/thesisData/FCCbatch_clipped'

def readSnwPrbMask(fp = mskFile, threshold=80):
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


# next up --> extract bands from FCC to dict
# read all files from directory

def meanSdForTif(direc=directory,t=95,msk=mskFile):
    # read boolean snow mask
    _, snwBool = readSnwPrbMask(msk,threshold=t) # modify threshold
    hhMeanDict = {}
    hhSdDict = {}
    hvMeanDict = {}
    hvSdDict = {}
    
    for entry in os.scandir(direc):
        if entry.path.endswith(".tif") and entry.is_file():
            # read fcc file
            p = entry.path
        else: continue
        
        if entry.path.endswith('_clipped.tif'):
            splitDate = dateFromFilename(os.path.split(p)[-1], 2)
        else: 
            splitDate = dateFromFilename(os.path.split(p)[-1])
        print(splitDate)
        hh, hv = readFcc(p) # original hh and hv with nan values
        
        hhMean, hhSd = calcMeanSd(snwBool, hh)
        
        try:
            hvMean, hvSd = calcMeanSd(snwBool, hv)
        except:
            hvMean = np.nan
            hvSd = np.nan
            
# =============================================================================
#         # multiply glacier mask with polarisations
#         hh_masked = np.multiply(snwBool, hh)
#         hv_masked = np.multiply(snwBool, hv)
#         
#         #extract values for glaciarised areas
#         hh_msk_val = extractVals(hh_masked)
#         hv_msk_val = extractVals(hv_masked)
#         
#         # calculate mean and sd for glacierised areas
#         hhMean = hh_msk_val.mean()
#         hhSd = hh_msk_val.std()
#         #print('Mean HH: ' + str(hhMean))
#         #print('Standard dev HH: ' + str(hhSd))
#             
#         hvMean = hv_msk_val.mean()
#         hvSd = hv_msk_val.std()
#         #print('Mean HV: ' + str(hvMean))
#         #print('Standard dev HV: ' + str(hvSd))
# =============================================================================
        
        hhMeanDict[splitDate] = hhMean
        hhSdDict[splitDate] = hhSd
            
        hvMeanDict[splitDate] = hvMean
        hvSdDict[splitDate] = hvSd
        
    plotMeanSd(hhMeanDict, hhSdDict, hvMeanDict, hvSdDict)
    
    return hhMeanDict, hhSdDict, hvMeanDict, hvSdDict
            
def calcMeanSd(boolMsk, pol):
    # multiply glacier mask with polarisations
    pol_masked = np.multiply(boolMsk, pol)
     
    #extract values for glaciarised areas
    pol_msk_val = extractVals(pol_masked)
        
    # calculate mean and sd for glacierised areas
    polMean = pol_msk_val.mean()
    polSd = pol_msk_val.std()
    
    return polMean, polSd
    


def readFcc(fPath=fccPath):
    
    #splitDate = dateFromFilename(os.path.split(fPath)[-1])
    #print(splitDate)
    
    fcc = rio.open(fPath)
    #print(fcc.meta) # print metadata
    
    fcc_hh = fcc.read(1)
    
    try: fcc_hv = fcc.read(2)
    except: fcc_hv = np.nan
    
    fcc_hh[fcc_hh == 0] = np.nan
    try: fcc_hv[fcc_hv == 0] = np.nan
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
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Set the axis lables
    ax.set_xlabel('Day', fontsize = 14)
    ax.set_ylabel('Mean sigma_0 [dB]', fontsize = 14)
    
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
    color_HH = 'orange'
    color_HV = 'darkgreen'
    
    # Line style for each dataset
    lineStyle_HH={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    lineStyle_HV={"linestyle":"-", "linewidth":2, "markeredgewidth":1, "elinewidth":0.8, "capsize":1}
    
    # Create an error bar for each dataset
    line_HH=ax.errorbar(xaxis, HHmean_y, yerr=HHsd, **lineStyle_HH, color=color_HH, label='HH')
    line_HV=ax.errorbar(xaxis, HVmean_y, yerr=HVsd, **lineStyle_HV, color=color_HV, label='HV')
    
    # Label each dataset on the graph, xytext is the label's position 
    #for i, txt in enumerate(HHmean_y):
    #        ax.annotate(txt, xy=(xaxis[i], HHmean_y[i]), xytext=(xaxis[i]+0.03, HHmean_y[i]+0.3),color=color_HH)
    
    #for i, txt in enumerate(HVmean_y):
    #        ax.annotate(txt, xy=(xaxis[i], HVmean_y[i]), xytext=(xaxis[i]+0.03, HVmean_y[i]+0.3),color=color_HV)
            
    
    # Draw a legend bar
    plt.legend(handles=[line_HH, line_HV], loc='upper right')
    
    # Customize the tickes on the graph
    plt.xticks(xaxis,rotation=45, fontsize=10)               
    #plt.yticks(np.arange(20, 47, 2))
    
    # Customize the legend font and handle length
    params = {'legend.fontsize': 12,
              'legend.handlelength': 2}
    plt.rcParams.update(params)

    
    # Draw a grid for the graph
    ax.grid(color='lightgrey', linestyle='-')
    ax.set_facecolor('w')
    
    ax.set_title('Mean Backscatter of glaciarised areas', fontsize=16)
    
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
    s1 = fn.split('_')[-dloc]
    #s2 = s1.split('.')[0]
    return s1


# define binary colormap
def binCmap(base_cmap):
    base = plt.cm.get_cmap(base_cmap)
    N=2
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)
