#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 09:44:43 2020

@author: GalinaJonat
"""
import rasterio as rio
import numpy as np

glims = rio.open('/Volumes/ElementsSE/thesisData/Datasets/GlacierOutline/glimsNodataAndGlac_12600.tif')
glims_arr = glims.read(1)