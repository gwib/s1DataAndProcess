#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:56:40 2020

@author: GalinaJonat
"""

import rasterio as rio
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import silhouette_score
from matplotlib import colors as mcolors
from colours import cMap # thesis colour scheme
import xarray as xr

 ###HELPER FUNCTIONS###
# =============================================================================
# def readFcc(fPath):
#     
#     #splitDate = dateFromFilename(os.path.split(fPath)[-1])
#     #print(splitDate)
#     
#     fcc = rio.open(fPath)
#     #print(fcc.meta) # print metadata
#     
#     fcc_hh = fcc.read(1)
#     
#     try: fcc_hv = fcc.read(2)
#     except: fcc_hv = np.nan
#     
#     fcc_hh[fcc_hh == 0] = np.nan
#     try: fcc_hv[fcc_hv == 0] = np.nan
#     except: print('HV not available.')
#     
#     #plotPols(fcc_hh, fcc_hv, splitDate)
#     
#     #printMinMax(fcc_hh, fcc_hv)
#     
#     return fcc_hh, fcc_hv, fcc   
# ######    
# =============================================================================


fp = '/Volumes/ElementsSE/thesisData/toHist/ncdf/Sigma0_HHHV_20190611.nc'

def kmeansFromNetCDF(fPath):
    outFname = os.path.dirname(fPath)+'/'+os.path.split(fp)[-1].split('.')[-2]+'_clusters.csv'
    
    df = readDfFromNetCDF(fPath)
    print(df.head())
    print('Starting kMeans. Output file will be saved in: '+outFname )    
    df, kmeans = kmeansOnHHHV(df,outFname)
    
    return df, kmeans

def readDfFromNetCDF(fPath):
    ds = xr.open_dataset(fPath)
    df = ds.to_dataframe()
    df.reset_index(inplace=True)
    df.replace(0,np.nan,inplace=True)
    return df

def kmeansOnHHHV(df, outFile='/Volumes/ElementsSE/thesisData/toHist/clustering/clusters.csv'):
    #perform kmeans
    kmeans = KMeans(n_clusters=6, random_state=3).fit(df[['Band1', 'Band2']])
    
    # new column in dataframe for location cluster
    df['kmeans_cluster'] = kmeans.labels_
    
    try: df.to_csv(outFile)
    # computing and printing the score of the clustering
    try: print('------Scores of K-Mean Clustering on dataframe ----------\n'+'silhouette:'+str(kmeansSilhouette(df))+
          '\n'+'distortion: '+str(kmeans.inertia_))
    except: print('An exception occurred while calculating the K-Means scores.')
    
    return df, kmeans # returns df with added column from clustering

def kmeansOnHH(df):
    #perform kmeans
    kmeans = KMeans(n_clusters=6, random_state=3).fit(df[['Band1']]) #HH
    
    # new column in dataframe for location cluster
    df['kmeans_cluster'] = kmeans.labels_
    
    # computing and printing the score of the clustering
    print('------Scores of K-Mean Clustering on dataframe ----------\n'+'silhouette:'+str(kmeansSilhouette(df))+
          '\n'+'distortion: '+str(kmeans.inertia_))
    
    return df, kmeans

def kmeansOnHV(df):
    #perform kmeans
    kmeans = KMeans(n_clusters=6, random_state=3).fit(df[['Band2']]) #HV
    
    # new column in dataframe for location cluster
    df['kmeans_cluster'] = kmeans.labels_
    
    # computing and printing the score of the clustering
    print('------Scores of K-Mean Clustering on dataframe ----------\n'+'silhouette:'+str(kmeansSilhouette(df))+
          '\n'+'distortion: '+str(kmeans.inertia_))
    
    return df, kmeans

def kmeansSilhouette(df):
    sampledf = df.sample(n=1000)
    pols = []
    for i in range(len(sampledf['HH'].values)):
        pols.append([sampledf['HH'].values[i], sampledf['HV'].values[i]])
    pwdist = pairwise_distances(pols, metric='manhattan')
    silhouette_avg = silhouette_score(pwdist, sampledf['kmeans_cluster'], metric="precomputed")
    return silhouette_avg

def plotClusters(df, clusterCol='kmeans_cluster'):
    num_colors=len(set(df[clusterCol].values))
    #colors=list(mcolors.CSS4_COLORS.keys())  #found this by searching "python color list"
    #cluster_colors=random.choices(cMap, k=num_colors)
    for i in range(0, num_colors):
        print('Color for cluster '+str(i)+': '+ cMap[i])
    x_=[]
    y_=[]
    c_=[]
    for label, x, y in zip(df[clusterCol].values, df['x'].values, df['y'].values):
        if label==-1:
            continue
        x_.append(x)
        y_.append(y)
        c_.append(cMap[label])
    plt.scatter(x_,y_,s=0.3,c=c_)
    #plt.scatter(-73.974689,40.68265, c='black')
    
