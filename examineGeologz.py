#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 20:18:48 2020

@author: GalinaJonat
"""

import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from colours import colorDict
from sklearn.utils import shuffle
import squarify

geolFile = '/Volumes/ElementsSE/thesisData/Datasets/geologicalMap/diskoGeology.csv'

geolDisko = pd.read_csv(geolFile)

gm_count = Counter(list(geolDisko.GM_LABEL))

geol_group = {}
# volcanic rocks
geol_group[1] = ['Vph','MNN','MR','MRA','Vpb','a','gn','deltT1','NAt']#,'ms','MS'] #volcanic rocks
geol_group[2] = ['ICE'] # ice
geol_group[3] = ['LAK'] # lakes
geol_group[4] = ['NAK'] # marine sandstone
geol_group[5] = ['NAS'] # non-marine sandstone
geol_group[6] = ['Q10'] #rock slides
#geol_group[7] = ['NAt'] # fossils
geol_group[8] = ['Q7'] # glaciofluvial and marine deposits
geol_group[9] = ['Qundif', 'NU', 'ms', 'MS']

geolNames = {}
geolNames[1] = f'Volcanic \n Rocks'
geolNames[2] = 'Ice'
geolNames[3] = 'Lake'
geolNames[4] = f'Marine \n Sandstone'
geolNames[5] = f'Non-marine \n Sandstone'
geolNames[6] = f'Rock Slides'
#geolNames[7] = 'Fossils'
geolNames[8] = f'Glaciofluvial \n and Marine \n Deposits'
geolNames[9] = f'Un-\ndifferentiated\nDeposits'


geolNamesPlot = {}
geolNamesPlot[1] = f'Volcanic Rocks'
geolNamesPlot[2] = 'Ice'
geolNamesPlot[3] = 'Lake'
geolNamesPlot[4] = f'Marine Sandstone'
geolNamesPlot[5] = f'Non-marine Sandstone'
geolNamesPlot[6] = f'Rock Slides'
#geolNames[7] = 'Fossils'
geolNamesPlot[8] = f'Glaciofluvial and Marine Deposits'
geolNamesPlot[9] = f'Undifferentiated Deposits'


geolColours = [colorDict['darkBlue'],colorDict['azure'],colorDict['darkGreen'],
               colorDict['darkOrange'], colorDict['darkRed'], colorDict['darkYellow'],
               colorDict['black85'], colorDict['black75']
               ]

def groupGeol():
    geolDiskoGroup = geolDisko.copy()
    geolDiskoGroup['geol_group'] = geolDiskoGroup['GM_LABEL'].apply(lambda x: strInGroup(x))
    return geolDiskoGroup
    
def strInGroup(inStr):
    for g in list(geol_group.keys()):
        if (inStr in geol_group[g]):
            return g
        else: continue
    return -1

geo_group = groupGeol()
aggr_func_geol = {'SHAPE_Area': 'sum'} # snow depth

geoTypesDisko = geo_group.groupby(geo_group['geol_group']).aggregate(aggr_func_geol)

totalArea = sum(list(geoTypesDisko.SHAPE_Area))

geoTypesDisko['area_perc'] = geoTypesDisko.SHAPE_Area.apply(lambda x: x/totalArea * 100)

def plotGeology():
    xax = []
    for i in geoTypesDisko.index:
        xax.append(geolNamesPlot[i])
    print(xax)    
    
    fig, ax = plt.subplots()
    ax.bar(xax, geoTypesDisko.area_perc, color=colorDict['darkYellow'])
    ax.set_ylabel('Area coverage for geology type in  $\%$', fontsize=14)
    ax.set_xticks(list(geoTypesDisko.index),xax)#, rotation=45, fontsize=8)
    fig.set_dpi(200)
    fig.subplots_adjust(left=0.2)
    fig.show()

def plotGeoPie():
    fig, ax = plt.subplots(dpi=200,subplot_kw=dict(aspect="equal"))
    
    # Data to plot
    labels = []
    for i in geoTypesDisko.index:
        labels.append(geolNamesPlot[i])
    
    
    geoTypePerc = list(geoTypesDisko.area_perc)
    
    
    print(len(geoTypePerc))
    #X, y = shuffle(labels,geoTypePerc,random_state=33)
    p = np.array([0,6,3,7,2,1,5,4])
    p = p.astype(int)
    
    geoPerc_ordered = []
    label_ordered = []
    geoCol_ordered = []
    for i in p:
        geoPerc_ordered.append(geoTypePerc[i])
        label_ordered.append(labels[i])
        geoCol_ordered.append(geolColours[i])
        
        
    # Plot
    wedges, texts, autotexts = ax.pie(geoPerc_ordered, labels=label_ordered, colors=geoCol_ordered,
    autopct='%1.1f%%', shadow=False, startangle=110)
    
    plt.setp(autotexts,size=10)

    return labels, geoTypePerc

def plotGeoTree():
    labels = []
    for i in geoTypesDisko.index:
        labels.append(geolNamesPlot[i])
    
    fig, ax = plt.subplots(dpi=200,subplot_kw=dict(aspect="equal"))
    geoTypePerc = list(geoTypesDisko.area_perc)
    
    squarify.plot(sizes=geoTypePerc, label=labels,color=geolColours)#,alpha=.4)
    plt.axis('off')
    plt.show()
    
    p = np.array([0,6,3,7,2,1,5,4])
    p = p.astype(int)
    
    geoPerc_ordered = []
    label_ordered = []
    geoCol_ordered = []
    for i in p:
        geoPerc_ordered.append(geoTypePerc[i])
        label_ordered.append(labels[i])
        geoCol_ordered.append(geolColours[i])
        
    fig2, ax2 = plt.subplots(dpi=200,subplot_kw=dict(aspect="equal"))
        
    ax2.squarify.plot(sizes=geoPerc_ordered, label=label_ordered,color=geoCol_ordered)#,alpha=.4)
    ax2.axis('off')
    plt.show()