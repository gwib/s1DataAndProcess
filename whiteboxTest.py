#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:36:57 2020

@author: GalinaJonat
"""

from whitebox.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()
wbt.work_dir = '/Volumes/ElementsSE/thesisData/toHist/mskClipped/'

wbt.average_overlay('FCC_Sigma0_HHHV_20200418_clipped_msk.tif;FCC_Sigma0_HHHV_20200313_clipped_msk.tif',
                    output='test.tif')