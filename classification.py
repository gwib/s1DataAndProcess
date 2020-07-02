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
import random


# example file
fp = '/Volumes/ElementsSE/thesisData/toHist/ncdf/Sigma0_HHHV_20190611.nc'

# putting it all together
def kmeansFromNetCDF(fPath):
    outFname = os.path.dirname(fPath)+'/'+os.path.split(fp)[-1].split('.')[-2]+'_clusters.csv'
    
    df = readDfFromNetCDF(fPath)
    print(df.head())
    #print(df.shape)
    print('Starting kMeans. ')    
    df, kmeans = kmeansOnHHHV(df,outFname)
    
    return df, kmeans

# reading dataframe from netCDF file
def readDfFromNetCDF(fPath):
    ds = xr.open_dataset(fPath)
    df = ds.to_dataframe()
    df.reset_index(inplace=True)
    df.replace(0,np.nan,inplace=True)
    return df

# K-Means clustering with both polarisations
def kmeansOnHHHV(df, outFile='/Volumes/ElementsSE/thesisData/toHist/clustering/clusters.csv'):
    print(df.shape)
    df.dropna(inplace=True)
    print('NaNs removed.')
    print(df.shape)
    #perform kmeans
    kmeans = KMeans(n_clusters=6, random_state=3).fit(df[['Band1', 'Band2']])
    
    # new column in dataframe for location cluster
    df['kmeans_cluster'] = kmeans.labels_
    
    print ('Cluster Centers: ')
    print (kmeans.cluster_centers_)
    
    try:
        df.to_csv(outFile)
        print('Output file has been saved: '+outFile)
    except: print('CSV file could not be saved.')
    # computing and printing the score of the clustering
    try: print('------Scores of K-Mean Clustering on dataframe ----------\n'+'silhouette:'+str(kmeansSilhouette(df))+
          '\n'+'distortion: '+str(kmeans.inertia_))
    except: print('An exception occurred while calculating the K-Means scores.')
    
    return df, kmeans # returns df with added column from clustering

def kmeansOnHH(df):
    df.dropna(inplace=True)
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


def saveDataframeToNetCDF(df, outFile):
    ds = df.set_index(['x','y']).to_xarray()
    ds.to_netcdf(outFile)

def plotClusters(df, clusterCol='kmeans_cluster'):
    num_colors=6
    #num_colors=len(set(df[clusterCol].values))
    colors=list(mcolors.CSS4_COLORS.keys())  #found this by searching "python color list"
    cluster_colors=random.choices(colors, k=num_colors)
    for i in range(0, num_colors):
        print('Color for cluster '+str(i)+': '+ cluster_colors[i])
    x_=[]
    y_=[]
    c_=[]
    for label, x, y in zip(df[clusterCol].values, df['x'].values, df['y'].values):
        if label==-1:
            continue
        x_.append(x)
        y_.append(y)
        c_.append(cluster_colors[label])
    plt.scatter(x_,y_,s=0.3,c=c_)
    #plt.scatter(-73.974689,40.68265, c='black')