#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 01:04:42 2020

@author: GalinaJonat
"""

import pandas as pd
import numpy as np
from examineGeologz import geolNames
import matplotlib.pyplot as plt


clusterCSVFolder = '/Volumes/ElementsSE/thesisData/toHist/mskClipped/clusterAftermath/zonalHistograms/'


#TODO: Compare clusters to GLIMS
# cluster count for GLIMS classification April 2016
#fp_glimsCluster201606 = '/Volumes/ElementsSE/thesisData/toHist/mskClipped/clusterAftermath/zonalStatsGLIMS_20160614_HHclusters.csv'

#glimsCluster201606 = pd.read_csv(fp_glimsCluster201606)

#clusterCounts = glimsCluster201606[['HISTO20160614_1', 'HISTO20160614_2',
#       'HISTO20160614_3', 'HISTO20160614_4', 'HISTO20160614_5',
#       'HISTO20160614_6']]

#print(clusterCounts.sum(axis=0, skipna=True))


def plotClusterCountByGeotype(df,hist_prefix='HISTO201'):
    aggr_func_geol = {hist_prefix+'_1':'sum', hist_prefix+'_2':'sum', hist_prefix+'_3':'sum',
           hist_prefix+'_4':'sum', hist_prefix+'_5':'sum', hist_prefix+'_6': 'sum'} # summing area and classCount
    
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

        
        
def plotClusterPercByGeotype(df,hist_prefix='HISTO201'):
    aggr_func_geol = {hist_prefix+'_1':'sum', hist_prefix+'_2':'sum', hist_prefix+'_3':'sum',
           hist_prefix+'_4':'sum', hist_prefix+'_5':'sum', hist_prefix+'_6': 'sum'} # summing area and classCount
    
    df_classCount = df.groupby(df['geol_group']).aggregate(aggr_func_geol)
    df_classCount["sum"] = df_classCount.sum(axis=1)
    
    for i in df_classCount.index:
        x = [1,2,3,4,5,6]
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
