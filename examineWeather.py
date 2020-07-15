# -*- coding: utf-8 -*-

"""
Created on Fri Jul  3 10:26:33 2020

@author: galinavj
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from colours import colorDict
import datetime as dt

### HELPER FUNCTIONS
def nanForNeg(x):
    if x < 0:
        return np.nan
    else: return x

# Windows
#prcpFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
#snwDepthFile = "m:\\Documents\\thesis\\data\\weather\\View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
#metFile = "m:\\Documents\\thesis\\data\\weather\\View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"

# Home
prcpFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/View_ClimateBasis_Disko_Data_Precipitation_Precipitation__60min_sample_mm270520201658405828.csv"
snwDepthFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/View_ClimateBasis_Disko_Data_Snow_depth_Snow_depth__60min_average_m270520201657165978.csv"
tempFile = "/Volumes/Transcend1/IIKT/Thesis/Datasets/weather/qeqertarsuaq-heliport-daily-20192020.csv"
metFile = "/Volumes/ElementsSE/thesisData/weather/View_GeoBasis_Disko_Data_Meteorology_AWS2Meteorology030720201034510908.csv"


prcp = pd.read_csv(prcpFile, delimiter="\t", encoding="unicode_escape")
snowDepth = pd.read_csv(snwDepthFile, delimiter="\t", encoding="unicode_escape")
temp = pd.read_csv(tempFile, delimiter=";")#, encoding="unicode_escape")

temp['Date'] = temp.DateTime.apply(lambda x: dt.datetime.strptime(x.split()[0], '%Y-%m-%d'))
# snow depth
snowDepth['Date'] = snowDepth[snowDepth.columns[0]]
snowDepth['Datetime'] = snowDepth['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
snowDepth_new = snowDepth[['Datetime', 'SD (m)']].copy()
aggregation_functions_snowDepth = {'SD (m)': 'mean'} # snow depth

snowDepthDaily = snowDepth_new.groupby(snowDepth_new['Datetime']).aggregate(aggregation_functions_snowDepth)

snowDepthDaily['SnwDepth_avg'] = snowDepthDaily['SD (m)'].apply(lambda x: nanForNeg(x))

# Precipitation
prcp['Date'] = prcp[prcp.columns[0]]
prcp['Datetime'] = prcp['Date'].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
prcp_new = prcp[['Datetime', 'PRE (mm)']].copy()
aggr_func_prcp = {'PRE (mm)': 'sum'}
# total precipitation per day
prcpDaily = prcp_new.groupby(prcp_new['Datetime']).aggregate(aggr_func_prcp)
# remove precipitation < 0
prcpDaily['prcp'] = prcpDaily['PRE (mm)'].apply(lambda x: nanForNeg(x))

prcpDaily1920 = prcpDaily.loc[prcpDaily.index >= dt.datetime(2019, 4, 12)]
snowDepthDaily1920 = snowDepthDaily.loc[snowDepthDaily.index >= dt.datetime(2019, 4, 12)]
temp = temp.loc[temp.Date >= dt.datetime(2019, 4, 12)]

def plotSnwPrcp():
    dates = list(prcpDaily.index)
    # subplot with shared x-axis
    fig=plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    ax1.bar(prcpDaily1920.index, prcpDaily1920.prcp, color=colorDict['darkblue'])
    ax2.plot(snowDepthDaily1920.index, snowDepthDaily1920.SnwDepth_avg)
        
    #ax1.set_title('Precipitation')
    #ax2.set_title('Snow Depth')
    
    ax1.set_ylabel(r'Precipitation in $mm$')
    ax2.set_ylabel(r'Snow depth in $m$')
    

    ax1.grid(color='lightgrey', linestyle='-')
    ax1.set_facecolor('w')
    ax2.grid(color='lightgrey', linestyle='-')
    ax2.set_facecolor('w')    
    #fig.suptitle('Histogram for polarisation on '+splitDate, fontsize=14)
    
    ax1.get_shared_x_axes().join(ax1, ax2)
    # Customize the tickes on the graph
    #plt.xticks(dates,rotation=45, fontsize=10)               
    #plt.yticks(np.arange(20, 47, 2))
    #ax2.set_xticklabels(list(prcpDaily1920.index))
    ax2.autoscale() ## call autoscale if needed
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
    plt.show()


def subplotsSnwPrcp():
    dates = snowDepthDaily1920.index
    fig2, axs2 = plt.subplots(2, sharex=True)
    axs2[0].plot(dates, snowDepthDaily1920.SnwDepth_avg)
    axs2[1].plot(dates, prcpDaily1920.prcp)
    axs2[2].plot()
    
    axs2[0].set_ylabel('Average daily snow depth [m]', fontsize=8)
    axs2[1].set_ylabel('Daily precipitation [mm]', fontsize=8)
    axs2[1].set_xlabel('Date', fontsize=8)
#plt.plot(list(snowDepthDaily.index), list(snowDepthDaily['SnwDepth_avg']))
#plt.savefig('/Volumes/Transcend1/IIKT/thesis/report/plots/snowDepth.png')

def pltSnwPrcp():
    fig, ax1 = plt.subplots()
    
    color=colorDict['blue']
    ax1.set_xlabel('Date')
    ax1.set_ylabel(r'Snow depth in $m$', color=color)
    ax1.plot(snowDepthDaily1920.index, snowDepthDaily1920.SnwDepth_avg, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    #ax1.grid(color=colorDict['black15'], linestyle='-')
    ax1.set_facecolor('w')
    color='#000000'
    ax2 = ax1.twinx()
    ax2.set_ylabel(r'Precipitation in $mm$', color=color)
    ax2.bar(prcpDaily1920.index, prcpDaily1920.prcp, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    #ax2.grid(color=colorDict['black45'])
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
    fig.tight_layout()
    fig.set_dpi(200)
    plt.show()
    

def plotTemp():
     #fig, ax = plt.subplots()
     fig = plt.figure(dpi=200)
     ax = fig.subplots(1)
     d = temp.Date
     ax.plot(d,temp.Middel, linewidth=1)
     ax.plot(d,temp.Laveste, '--', linewidth=0.3)
     ax.plot(d, temp.Højeste, '--', linewidth=0.3)
     #ax.set_xticks(ax.get_xticks()[::10])
      #ax.xticks.set_tick_params()
     #ax.set_title('Temperatures at Qeqertarsuaq Heliport')
     ax.set_xlabel('Date')
     ax.set_ylabel(r'Temperature in $°C$')
     fig.autofmt_xdate(bottom=0.2)
     fig.subplots_adjust(bottom=0.24)
     fig.show()

def plotPrcp():
     #fig, ax = plt.subplots()
     fig = plt.figure(dpi=200)
     ax = fig.subplots(1)
     d = temp.Date
     ax.plot(d,temp.Middel, linewidth=1)
     ax.plot(d,temp.Laveste, '--', linewidth=0.3)
     ax.plot(d, temp.Højeste, '--', linewidth=0.3)
     #ax.set_xticks(ax.get_xticks()[::10])
      #ax.xticks.set_tick_params()
     #ax.set_title('Temperatures at Qeqertarsuaq Heliport')
     ax.set_xlabel('Date')
     ax.set_ylabel(r'Temperature in $°C$')
     fig.autofmt_xdate(bottom=0.2)
     fig.subplots_adjust(bottom=0.24)
     fig.show()