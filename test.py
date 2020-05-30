import rsgislib
from rsgislib import imageutils
from osgeo import gdal
import numpy
import glob
import sys
from sklearn.cluster import MiniBatchKMeans

# Search current directory for KEA rasters
InputImages = glob.glob('/Volumes/ElementsSE/thesisData/sigma0/WinsvoldGRD_Sigma0_Subset_Orb_TN_Cal__S1B_IW_GRDH_1SDH_20190412T101559_20190412T101624_015772_01D9A6_29DC.data/Sigma0_HH_db.img')

# Define the number of spectral classes
SpectralClasses = 6

# Define format and datatype of output raster
gdalformat = 'GTiff'
gdaldatatype = gdal.GDT_Byte

# Define the classifier
clf = MiniBatchKMeans(n_clusters=SpectralClasses, init='k-means++', max_iter=10, batch_size=10000, verbose=0, compute_labels=True, random_state=None, tol=0.0, max_no_improvement=100, init_size=2000, n_init=10, reassignment_ratio=0.05)

# Terminate the script if the returned list is empty
if not InputImages:
  sys.exit("Error: No input images provided.")

for Raster in sorted(InputImages):
    OutImage = Raster.replace('.img','_Kmeans.img')

    print("Reading " + Raster)
    Image = gdal.Open(Raster, gdal.GA_ReadOnly)

    # Set up empty list to hold data
    TestData = []

    # Read data from each band
    for band in range(Image.RasterCount):
        band += 1

        B = Image.GetRasterBand(band)

        Array = B.ReadAsArray()

        # Get shape of array
        Shape = numpy.ma.shape(Array)

        # Flatten to 1D array
        Array = Array.flatten()

        TestData.append(Array)

        del Array

    TestData = numpy.array(TestData, dtype=numpy.dtype('float32')) # Convert to float to prevent sklearn error/warning message 
    TestData = numpy.transpose(TestData)

    print("Performing K-means classification...")
    clf.fit(TestData, y=None)
    predictedClass = clf.predict(TestData)

    del TestData

    predictedClass = predictedClass + 1 #Add 1 to exclude zeros in output raster
    predictedClass = numpy.reshape(predictedClass, Shape) # Reshape the numpy array to match the original image

    # Create an output raster the same size as the input image
    driver = gdal.GetDriverByName(gdalformat)
    metadata = driver.GetMetadata()
    output = driver.Create(OutImage, Image.RasterXSize, Image.RasterYSize, 1, gdaldatatype)

    # Create projection info for the output raster
    output.SetProjection(Image.GetProjectionRef())
    output.SetGeoTransform(Image.GetGeoTransform()) 

    # Write classification to band 1
    output_band = output.GetRasterBand(1)
    output_band.WriteArray(predictedClass)

    # Close datasets
    output_band = None
    output = None
    Image = None
    del predictedClass

    # Build image overviews
    imageutils.popImageStats(OutImage, True, 0, True)
    print("Done." + '\n')

print("All images processed.")