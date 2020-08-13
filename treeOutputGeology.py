#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 13:00:51 2020

@author: GalinaJonat
"""
import pandas as pd
import numpy as np
from examineGeologz import geolNames,geolColours
import matplotlib.pyplot as plt

example_fp = '/Volumes/ElementsSE/thesisData/decisionTrees/longTerm/Jun2017/zonalHist/'

geolList = [geolNames[i] for i in geolNames.keys()]

def classPercByGeotype(dfp,hist_prefix):
    df = pd.read_csv(dfp)
    aggr_func_geol = {hist_prefix+'_NODATA':'sum', hist_prefix+'_0':'sum', hist_prefix+'_1':'sum'
           } # summing area and classCount
    
    df_classCount = df.groupby(df['geol_group']).aggregate(aggr_func_geol)
    df_classCount["sum"] = df_classCount.sum(axis=1)
    
    classPerc = []
    for i in df_classCount.index:
        x = ['NODATA','0','1']
        y = []
        cSum = df_classCount.loc[i,'sum']
        #print('GeologyType '+str(i))
        #print(cSum)
        for c in x:
            cc = df_classCount.loc[i,hist_prefix+'_'+str(c)]
            #print(cc/cSum)
            y.append(cc/cSum * 100)
        
        classPerc.append(y)
     
    classPerc_arr = np.asarray(classPerc)
    
    return classPerc_arr



def classPercByGeotypePlotAll(dfp,hist_prefix):
    classPerc_arr = classPercByGeotype(dfp, hist_prefix)
    ice_perc = classPerc_arr[:,2]
    
    y_pos = np.arange(0,1.5*len(geolNames),1.5)
    
    fig, ax = plt.subplots(dpi=200)

    ax.barh(y_pos,ice_perc,color=geolColours)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(geolList)
    
    ax.set_xlabel('Percent categorised as "Ice"',fontsize=9)
    
    ax.invert_yaxis()
    
    ax.tick_params(axis='y', labelsize=7)
    ax.tick_params(axis='x', labelsize=8)
    
    ax.set_xlim(0,100)
    
    fig.subplots_adjust(bottom=0.15)
    
    plt.show()
    
def plotClassCountByGeotype(df,hist_prefix):
    aggr_func_geol = {hist_prefix+'_NODATA':'sum', hist_prefix+'_0':'sum', hist_prefix+'_1':'sum',
           } # summing area and classCount
    
    df_classCount = df.groupby(df['geol_group']).aggregate(aggr_func_geol)
    
    for i in df_classCount.index:
        x = [1,2,3,4,5,6]
        y = []
        for c in x:
            y.append(df_classCount.loc[i,hist_prefix+'_'+str(c)])
        
        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_ylabel(geolNames[i]+'\nclass count')
        #fig.autofmt_xdate(bottom=0.2)
        fig.set_dpi(200)
        fig.show()

        
        
def plotClassPercByGeotype(dfp,hist_prefix):
    df = pd.read_csv(dfp)
    aggr_func_geol = {hist_prefix+'_NODATA':'sum', hist_prefix+'_0':'sum', hist_prefix+'_1':'sum'
           } # summing area and classCount
    
    df_classCount = df.groupby(df['geol_group']).aggregate(aggr_func_geol)
    df_classCount["sum"] = df_classCount.sum(axis=1)
    
    for i in df_classCount.index:
        x = ['NODATA','0','1']
        y = []
        cSum = df_classCount.loc[i,'sum']
        #print('GeologyType '+str(i))
        #print(cSum)
        for c in x:
            cc = df_classCount.loc[i,hist_prefix+'_'+str(c)]
            #print(cc/cSum)
            y.append(cc/cSum * 100)
        
        #print(sum(y))
        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_ylabel(geolNames[i]+'\nclass Percent')
        fig.set_dpi(200)
        fig.subplots_adjust(left=0.2)
        fig.show()