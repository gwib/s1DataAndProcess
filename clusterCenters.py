# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:18:19 2020

@author: galinavj
"""

import pandas as pd

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
    df['Date'] = df['Date'].astype(str)
    return df

clusterHH_df = readDfFromFile(clusterC_HH_f)
clusterHV_df = readDfFromFile(clusterC_HV_f)
clusterHHHV_df = readDfFromFile(clusterC_HHHV_f)




def clustersInCols(df,pol='HH'):
    col_Names = ['Date','Cluster_1', 'Cluster_2','Cluster_3', 'Cluster_4', 'Cluster_5', 'Cluster_6']
    colNames_pol = []
    for c in col_Names:
        if c=='Date':
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