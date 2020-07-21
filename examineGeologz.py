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
        xax.append(geolNames[i])
        
    plt.bar(geoTypesDisko.index, geoTypesDisko.area_perc, color=colorDict['darkYellow'])
    
    
    
    plt.xticks(list(geoTypesDisko.index),xax, rotation=45, fontsize=8)
    plt.tick_params('x',length=5)
    plt.ylabel('Area coverage in $\%$', fontsize=14)
    plt.show()


