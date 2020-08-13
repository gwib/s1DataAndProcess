#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 18:39:33 2020

@author: GalinaJonat
"""
import numpy as np
import datetime as dt
from saveVars import readHHHVdicts
from examineWeather import temp1920,snowDepthDaily1920
import matplotlib.pyplot as plt
from colours import colorDict

def plotTempAndBs(d1=dt.date(2019,9,16),d2=dt.date(2019,3,15)):
    mHH, sHH, mHV, sHV = readHHHVdicts('/Users/GalinaJonat/Documents/IIKT/Thesis/analysis/meanSd1920GLIMS.pkl')
    
    dates = np.array(list(mHH.keys()))
    datesSel = dates[(dates < d1) & (dates > d2)]
    print(datesSel)
    
    temp1920.set_index('Date', inplace=True)
    
    t =  list(temp1920.at[d,'Middel'] for d in datesSel)
    #s = list(snowDepthDaily1920.at[d,'SnwDepth_avg'] for d in datesSel)
    
    mHH_s = list(mHH[d] for d in datesSel)
    
    mHV_s = list(mHV[d] for d in datesSel)
    
    fig, ax = plt.subplots(dpi=200)
    
    color_HH = colorDict['orange'] # orange
    color_HV = colorDict['green'] # green
    
        # Line style for each dataset
    lineStyle_HH={"linestyle":"-", "linewidth":2, "markeredgewidth":1}
    lineStyle_HV={"linestyle":"-", "linewidth":2, "markeredgewidth":1}
    line_HH = ax.plot(datesSel,mHH_s, **lineStyle_HH, color=color_HH, label='HH')
    line_HV = ax.plot(datesSel,mHV_s, **lineStyle_HV, color=color_HV, label='HV')
    ax2 = ax.twinx()
    
    lineStyle_temp={"linestyle":"--", "linewidth":1, "markeredgewidth":1}
    line_temp = ax2.plot(datesSel,t,**lineStyle_temp,color=colorDict['blue'],label='Temperature')
    
    
    print(type(line_HH))
    print(type(line_temp))
    
    ax.set_ylabel('Backscatter in $dB$')
    ax2.set_ylabel('Temperature in $\degree C$')
    
    plt.legend(handles=[line_HH[0], line_HV[0],line_temp[0]],bbox_to_anchor=(1.08, 1.05), loc='upper left')
    plt.tight_layout()
    
    params = {'legend.fontsize': 8,
              'legend.handlelength': 2}
    plt.rcParams.update(params)

    
    # Draw a grid for the graph
    plt.grid(color=colorDict['black15'])