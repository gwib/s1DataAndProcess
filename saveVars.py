#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 09:43:53 2020

@author: GalinaJonat
"""

import pickle

# obj0, obj1, obj2 are created here...
fn = '/Users/GalinaJonat/Documents/IIKT/Thesis/analysis/dict.pkl'
# Saving the objects:
def saveObj(pklFile=fn, *argv):
    with open(pklFile, 'wb') as f:
        pickle.dump([*argv], f)

# Getting back the objects:
def readHHHVdicts(fp=fn):
    with open(fp, 'rb') as f:
        mHH, sHH, mHV, sHV = pickle.load(f)
    return mHH, sHH, mHV, sHV