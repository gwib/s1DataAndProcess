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

### predefined vars
mskFile = '/Volumes/ElementsSE/thesisData/validation/s2Mask/maskBool/aligned_s2Mask.tif'
#for testing purposes
fccPath = '/Volumes/ElementsSE/thesisData/FCCbatch_clipped/FCC_Sigma0_HHHV_20190412_clipped.tif'


def readSnwPrbMask(fp = mskFile):
    # import and create binary snow mask
    snwPrbMask=rio.open(fp)
    snwPrbMask.meta
    
    a_snwPrb = snwPrbMask.read(1)
    a_snwPrb[a_snwPrb < -1] = np.nan
    #plt.imshow(a_snwPrb)
    
    a_snwMaskBool = a_snwPrb.copy()
    
    # & for element-wise boolean-and
    #a_snwMaskBool[(~np.isnan(a_snwPrb)) & (a_snwPrb <= 60)] = 0.0
    #a_snwMaskBool[(~np.isnan(a_snwPrb)) & (a_snwPrb > 60)] = 1.0
    mask_Zero = (~np.isnan(a_snwPrb)) & (a_snwPrb <= 60)
    mask_Nan = np.isnan(a_snwPrb)
    a_snwMaskBool = np.ones((a_snwPrb.shape[0],a_snwPrb.shape[1]),dtype=np.float32)
    #print(a_snwMaskBool)
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

def readFcc(fPath=fccPath):
    
    splitDate = dateFromFilename(os.path.split(fPath)[-1])
    print(splitDate)
    
    fcc = rio.open(fPath)
    print(fcc.meta) # print metadata
    
    fcc_hh = fcc.read(1)
    fcc_hv = fcc.read(2)
    
    fcc_hh[fcc_hh == 0] = np.nan
    fcc_hv[fcc_hv == 0] = np.nan
    
    plotPols(fcc_hh, fcc_hv, splitDate)
    
    printMinMax(fcc_hh, fcc_hv)
    
    return fcc_hh, fcc_hv





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
    
    
def printMinMax(hh, hv):
    hh = hh[~np.isnan(hh)]
    hv = hv[~np.isnan(hv)]

    print ('HH min: '+ str(hh.min()))
    print ('HH max: '+ str(hh.max()))
    print ('HV min: '+ str(hv.min()))
    print ('HV max: '+ str(hv.max()))

###### HELPER FUNCTIONS #####
# extracting date from filename
def dateFromFilename(fn):
    s1 = fn.split('_')[-2]
    #s2 = s1.split('.')[0]
    return s1


# define binary colormap
def binCmap(base_cmap):
    base = plt.cm.get_cmap(base_cmap)
    N=2
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)
