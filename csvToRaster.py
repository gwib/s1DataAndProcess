# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:38:39 2020

@author: galinavj
"""

import os
import gdal

#dir_with_csvs = r"/home/panda"
#os.chdir(dir_with_csvs)

def find_csv_filenames(path_to_dir, suffix=".csv"):
    filenames = os.listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith(suffix) ]
#csvfiles = find_csv_filenames(dir_with_csvs)
#for fn in csvfiles:
#fn = r"C:\Users\galinavj\OneDrive - NTNU\thesisAnalysis\FCCbatch_clipped\FCC_Sigma0_HHHV_20190412_clipped.tif"
def csvToGrid(fn):
    vrt_fn = fn.replace(".csv", ".vrt")
    #lyr_name = fn.replace('.csv', '')
    out_tif = fn.replace('.csv', '.tiff')
    with open(vrt_fn, 'w') as fn_vrt:
        fn_vrt.write('<OGRVRTDataSource>\n')
        fn_vrt.write('\t<OGRVRTLayer name="%s">\n' % 'cluster')
        fn_vrt.write('\t\t<SrcDataSource>%s</SrcDataSource>\n' % fn)
        fn_vrt.write('\t\t<GeometryType>wkbPoint</GeometryType>\n')
        fn_vrt.write('\t\t<GeometryField encoding="PointFromColumns" x="x" y="y" z="kmeans_cluster"/>\n')
        fn_vrt.write('\t</OGRVRTLayer>\n')
        fn_vrt.write('</OGRVRTDataSource>\n')
    
    output = gdal.Grid(out_tif,vrt_fn)
    # below using your settings - I don't have sample large enough to properly test it, but it is generating file as well  
   #output2 = gdal.Grid('outcome2.tif','name.vrt', algorithm='invdist:power=2.0:smoothing=1.0') 
    return output