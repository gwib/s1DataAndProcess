#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:30:21 2020

@author: GalinaJonat
"""

# investigating GLIMS

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

glims = pd.read_csv('/Volumes/ElementsSE/thesisData/validation/glims/glimsPolygons_clipped.csv')

print(glims.columns)

print('Number of unique glacier entries in DB: '+ str(len(set(glims.glac_id))))

set(glims.anlys_time) # publication date
#Out[12]: {'2014-12-01T00:00:00', '2018-08-01T00:00:00'}

set(glims.src_date) # image date
#Out[13]: {'2001-08-29T00:00:00', '2016-08-30T00:00:00'}

set(glims.release_dt)
#Out[14]: {'2014-12-01T11:00:00', '2018-08-22T09:00:00'}

glims_short = glims.drop(['local_id', 'glac_stat', 'subm_id', 'rc_id'], axis=1)

#date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')

glims_short['src_date'] = glims_short['src_date'].apply(lambda d: dt.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S'))

glims_short['img_year'] = glims_short['src_date'].apply(lambda x: x.year)

glims_late = glims_short[glims_short.img_year > 2001]

glimsSub = pd.read_csv('/Volumes/ElementsSE/thesisData/validation/glims/glims_subset.csv')

glimsSub_short = glimsSub.drop(['local_id', 'glac_stat', 'subm_id', 'rc_id'], axis=1)


figGlimsHist, axGlimsHist = plt.subplots(dpi=150) 
axGlimsHist.hist(glims.area, bins=10, color='#0098DB')
axGlimsHist.set_ylabel('Glacier Count') #note:changed axis names, just need to rerun
axGlimsHist.set_xlabel(r'Glacier Area in $m^2$')
plt.show()