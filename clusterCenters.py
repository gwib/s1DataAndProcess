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

def plotPolPrCluster(dfHH,dfHV):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    
    # Set the axis lables
    #ax.set_xlabel('Date',fontsize=14)
    ax.set_ylabel(r'Mean $\sigma_0$ in $dB$',fontsize=14)
    
    # X axis is day numbers from 1 to 15
    dates = list(hhMeanDict.keys())
    dates.sort()
    #print(dates)
    xaxis = dates
    
    # Y values
    HHc_y = []
    HVc_y = []
    #HHsd = []
    #HVsd = []
    for d in dates:
        HHmean_y.append(hhMeanDict[d])
        HVmean_y.append(hvMeanDict[d])
        #HHsd.append(hhSdDict[d])
        #HVsd.append(hvSdDict[d])
    
    # Line color for error bar
    color_HH = colorDict['orange'] # orange
    color_HV = colorDict['green'] # green
    
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
    plt.xticks(xaxis,rotation=45)           
    plt.xlabel('Date',fontsize=14)    
    #plt.yticks(np.arange(20, 47, 2))
    
    # Customize the legend font and handle length
    params = {'legend.fontsize': 12,
              'legend.handlelength': 2}
    plt.rcParams.update(params)

    
    # Draw a grid for the graph
    
    
    #ax.set_title('Mean Backscatter of glaciarised areas', fontsize=16)
    
    plt.show()