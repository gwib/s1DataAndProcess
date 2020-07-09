#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 12:14:32 2020

@author: GalinaJonat
"""

import rasterio as rio
from rasterio.plot import show
from sklearn import cluster
import matplotlib.pyplot as plt
import numpy as np
from colours import cMap


# Open the image 
test_raster = rio.open("/Volumes/ElementsSE/thesisData/toHist/noData/FCC_Sigma0_HHHV_20190611_clipped_nodata.tif")
print(test_raster.meta)

# Read, enhance and show the image
rast_arr = test_raster.read(1) # read the opened image
vmin, vmax = np.nanpercentile(rast_arr, (5,95))  # 5-95% contrast stretch# show the enhanced image
plt.figure(figsize=[20,20])
show(rast_arr, cmap='gray', vmin=vmin, vmax=vmax)
plt.show()

# create an empty array with same dimension and data type
imgxyb = np.empty((test_raster.height, test_raster.width, test_raster.count), test_raster.meta['dtype'])# loop through the raster's bands to fill the empty array
for band in range(imgxyb.shape[2]):
    imgxyb[:,:,band] = test_raster.read(band+1)
    
# convert to 1d array
img1d=imgxyb[:,:,:3].reshape((imgxyb.shape[0]*imgxyb.shape[1],imgxyb.shape[2]))    

cl = cluster.KMeans(n_clusters=6, random_state=3) # create an object of the classifier
param = cl.fit(img1d) # train it
img_cl = cl.labels_ # get the labels of the classes
img_cl = img_cl.reshape(imgxyb[:,:,0].shape) # reshape labels to a 3d array (one band only)

# Create a custom color map to represent our different 4 classes
#cmap = mc.LinearSegmentedColormap.from_list("", ["black","red","green","yellow"])# Show the resulting array and save it as jpg image
plt.figure(figsize=[20,20])
plt.imshow(img_cl, cmap=cMap)
plt.axis('off')
#plt.savefig("elhas_clustered.jpg", bbox_inches='tight')
plt.show()