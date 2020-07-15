# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:18:19 2020

@author: galinavj
"""

import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from colours import colorDict


#windows
inFolder = "C:/Users/galinavj/OneDrive - NTNU/thesisAnalysis/clustersFromMsk/clusterCSV/"
#os
inFolder = "/Volumes/ElementsSE/thesisData/toHist/mskClipped/clusterAftermath/clusterCSV/"

clusterC_HH_f = inFolder+"ClusterCentersKMeans-HH.csv"
clusterC_HV_f = inFolder+"ClusterCentersKMeans-HV.csv"
clusterC_HHHV_f = inFolder+"ClusterCentersKMeans-HHHV.csv"

## FUNCTIONS
def readDfFromFile(fp):
    df = pd.read_csv(fp)
    try: df['Date'] = df['Date'].astype(str)
    except:
        df = pd.read_csv(fp,delimiter=';')
        df['Date'] = df['Date'].astype(str)
    return df

clusterHH_df = readDfFromFile(clusterC_HH_f)
clusterHV_df = readDfFromFile(clusterC_HV_f)
clusterHHHV_df = readDfFromFile(clusterC_HHHV_f)




def clustersInCols(df,pol='HH'):
    col_Names = ['Date_1','Cluster_1', 'Cluster_2','Cluster_3', 'Cluster_4', 'Cluster_5', 'Cluster_6']
    colNames_pol = []
    for c in col_Names:
        if c=='Date_1':
            colNames_pol.append(c)
        elif 'Cluster' in  c:
            colNames_pol.append(c+pol)
            
    #newDf = pd.DataFrame(columns=col_Names)
    l2 = []
    for d in set(list(df.Date)):
        l=[d]
        for c in [1,2,3,4,5,6]:
            l.append(df.loc[((df["Date"] == d) & (df.Cluster == c))][pol].iloc[0])
        l2.append(l)
    newDf = pd.DataFrame(l2, columns=colNames_pol)
    newDf['Date'] = newDf.Date_1.apply(lambda x: dt.datetime.strptime(x.split()[0], '%Y%m%d'))
        #df.loc[df_len] = l
        #l_df = pd.DataFrame([l], columns=newDf.columns)
        #print(l_df)
        #print(type(l_Series))
        #newDf.append(l_df)#, ignore_index=True)
    return newDf

hhbyClusters = clustersInCols(clusterHH_df,'HH')
hvbyClusters = clustersInCols(clusterHV_df,'HV')


hhhvbyClusters_hh = clustersInCols(clusterHHHV_df,'HH')
hhhvbyClusters_hv = clustersInCols(clusterHHHV_df, 'HV')

hhhvbyClusters = pd.merge(hhhvbyClusters_hv, hhhvbyClusters_hh, on='Date')

def plotPolPrCluster(dfpol, pol):
    fig = plt.figure(dpi=200)
    ax = fig.subplots(1)
    
    # Set the axis lables
    #ax.set_xlabel('Date',fontsize=14)
    ax.set_ylabel(r'Mean $\sigma_0$ in $dB$',fontsize=14)
    
    dfpol.sort_values(by=['Date_1'],inplace=True)
    
    
    # X axis is day numbers from 1 to 15
    dates = list(dfpol['Date'])
    #dates.sort()
    #print(dates)
    xaxis = dates
    print(xaxis)
    cols = list(dfpol.columns)
    clusterNames = [k for k in cols if 'Cluster' in k]
    
    clusterCols = {}
    clusterCols[1] = colorDict['darkBlue']
    clusterCols[2] = colorDict['darkAzure']
    clusterCols[3] = colorDict['darkGreen']
    clusterCols[4] = colorDict['darkOrange']
    clusterCols[5] = colorDict['darkRed']
    clusterCols[6] = colorDict['darkYellow']
     
    # Draw a grid for the graph
    ax.grid(color=colorDict['black15'])
    # Line style for each cluster
    lineStyle_clusters={"linestyle":"-", "linewidth":2}#, "markeredgewidth":1}#, "elinewidth":0.8, "capsize":1}

    
    clusterCenter = {}
    line={}
    for c in clusterNames:
        clusterCenter = list(dfpol[c])
        cluster_num = int(''.join(filter(str.isdigit,c)))
        
        line[c] = ax.scatter(xaxis,clusterCenter,**lineStyle_clusters,color=clusterCols[cluster_num],label = 'Cluster '+str(cluster_num))

    
    # Draw a legend bar
    plt.legend(loc='upper right')
    
    
    
    ax.set_xlabel('Date')
    ax.set_ylabel(r'Backscatter [$\sigma_0$ ('+pol+')] = dB')
    fig.autofmt_xdate(bottom=0.2)
    #fig.subplots_adjust(bottom=0.24)
    # Customize the tickes on the graph
    #plt.xticks(xaxis,rotation=45)           
    #plt.xlabel('Date',fontsize=14)    
    #plt.yticks(np.arange(20, 47, 2))
    
    # Customize the legend font and handle length
    #params = {'legend.fontsize': 12,
    #          'legend.handlelength': 2}
    #fig.set_rcParams.update(params)
    fig.autofmt_xdate(bottom=0.2)
    fig.subplots_adjust(bottom=0.24)

    
    fig.show()