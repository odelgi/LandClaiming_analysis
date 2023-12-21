
### -*- Demarcation detection -*-

# Olivia del Giorgio
# Version: 2023
# Script accessible on GitHub: Demarcation_analysis, odelgi

# Description: Code to detect linear features in the Gran Chaco ecoregion. 

# ##################################################### SET-UP ##################################################### #

# Load libraries
from osgeo import ogr, osr, gdal
from osgeo import gdalconst
from osgeo.gdalconst import *
import cv2
import astropy.units as u
import time
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# %matplotlib inline

import scipy.ndimage
import skimage
from skimage.exposure import rescale_intensity
from sklearn.ensemble import RandomForestClassifier
from skimage import measure, util
from skimage import morphology
from skimage.morphology import (erosion, dilation, opening, closing, binary_closing,
                                white_tophat,black_tophat, square, disk,remove_small_holes)
from skimage.filters import sato
from skimage.filters.rank import enhance_contrast
from skimage.util import img_as_ubyte
from skimage.measure import label, regionprops, regionprops_table
from skimage.segmentation import clear_border

from skimage.segmentation import random_walker
from tqdm import tqdm
from joblib import Parallel, delayed
import warnings
import gc

# ##################################################### WORKER FUNCTION ##################################################### #

def WorkerFunction(job):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    # Create the memory driver to generate the output-files
    drvMemR = gdal.GetDriverByName('MEM')
    drvMemV = ogr.GetDriverByName('Memory')
    # Extract the information from the job
    tileID = job['id']
    outFolder_DETECTED = job['outputDETECTED']

    # Helper-functions
    def LoadTile(tileID):
        rootPath = "A:/_BioGeo/giorgioo/Analysis_linearFeatures/"
        tile = gdal.Open(rootPath + "_NewData/S2/Full_Year/" + str(tileID) + 	"_Sentinel-2_2020_FullYear.tif", GA_ReadOnly)
        # Load image properties
        print("Loading tileID ", str(tileID))
        print("---------------------------------")
        gt = tile.GetGeoTransform() #affine transformation
        pr = tile.GetProjection() #coordinate system (projection)
        cols = tile.RasterXSize # number of columns of the raster
        rows = tile.RasterYSize # number of rows
        bands = tile.RasterCount
        return tile

    def CopyRasterToDisk(array, cols, rows, topright, topleft, gt, pr, type, outName):
        outRas = drvMemR.Create('', cols, rows, topright, topleft, type)
        outRas.SetProjection(pr)
        outRas.SetGeoTransform(gt)
        # Calcualte the new geotransform (because we only use a subset)
        ul_x = gt[0] + topright*gt[1]
        ul_y = gt[3] + topleft*gt[5]
        out_gt = [ul_x, gt[1], gt[2], ul_y, gt[4], gt[5]]
        outRas.SetGeoTransform(out_gt)
        outRas.GetRasterBand(1).WriteArray(array, 0, 0)
        outRas = None

# Function to detect linear features (using 1000x1000 pixel moving window)

def DetectFeatures(col, row, topright, topleft):
    # Define root path
    rootPath = "A:/_BioGeo/giorgioo/Analysis_linearFeatures/"

    ####################### FUNCTIONS #######################

    # Sato filter function
    def Sato(arr):
        sato_filt = sato(arr, sigmas=range(3, 5, 20), black_ridges=False, mode='reflect', cval=0)
        return sato_filt

    # Stretch array functions
    def Stretch_02_90(arr):
        x = arr
        x[np.isnan(x)] = 0
        p02, p90 = np.percentile(x, (2, 90))
        out = rescale_intensity(x, in_range=(p02, p90), out_range=(0,1))
        return out

    def Stretch_02_98(arr):
        x = arr
        x[np.isnan(x)] = 0
        p02, p98 = np.percentile(x, (2, 98))
        out = rescale_intensity(x, in_range=(p02, p98), out_range=(0,1))
        return out

    # Hugh line transformation function
    def HughLines(arr):
        u8 = arr.astype(np.uint8)
        line_image = np.copy(arr) * 0  # creating a blank to draw lines on
        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(u8, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(1,0,0),5)
        line_eroded = erosion(line_image, footprint=square(3), out=None) # erosion
        return(line_eroded)

    ### Morphological cleaning

    # 1. Function to remove small regions
    def RemoveSmall(arr,area):
        label_binary = label(arr) # label image regions
        regions = regionprops(label_binary) # get regions
        table = regionprops_table(label_binary,properties=('label', 'area'),)
        condition = (table['area'] > area) # condition of inclusion
        # zero out labels not meeting condition
        input_labels = table['label']
        output_labels = input_labels * condition
        filt_label_binary = util.map_array(label_binary, input_labels, output_labels)
        # Create small-filtered binary array
        removed = np.where(filt_label_binary > 0, 1, 0)
        return removed

    # 2. Function to remove floating blobs
    def RemoveFloatingBlobs(arr,major_axis):
        label_binary = label(arr) # label image regions
        regions = regionprops(label_binary) # get regions
        table = regionprops_table(label_binary,properties=('label','axis_major_length'),)
        condition = (table['axis_major_length'] < major_axis)
        # zero out labels not meeting condition
        input_labels = table['label']
        output_labels = input_labels * condition
        filt_label_binary = util.map_array(label_binary, input_labels, output_labels)
        # Create blob array
        more_blobs = np.where(filt_label_binary > 0, 1, 0)
        # remove blobs
        noblobs = arr - more_blobs
        return noblobs

    # 3. Function to remove short regions
    def RemoveShort(arr,length):
        label_binary = label(arr) # label image regions
        regions = regionprops(label_binary) # get regions
        table = regionprops_table(label_binary,properties=('label', 'axis_major_length'),)
        condition = (table['axis_major_length'] > length) # condition of inclusion
        # zero out labels not meeting condition
        input_labels = table['label']
        output_labels = input_labels * condition
        filt_label_binary = util.map_array(label_binary, input_labels, output_labels)
        # Create small-filtered binary array
        long = np.where(filt_label_binary > 0, 1, 0)
        return long

    ####################### PROCESSING #######################

    # Assign array dimensions
    pixc = cols # HOLD CONSTANT
    pixr = rows # HOLD CONSTANT
    topr = topright # MOVING WINDOW - STEP HORIZONTALLY BY 1000
    topl = topleft # MOVING WINDOW - STEP VERTICALLY BY 1000

    # Select bands
    Gp10 = tile.GetRasterBand(7).ReadAsArray(topr, topl, pixc, pixr) # ReadAsArray(0, 0, cols, rows)
    Rp10 = tile.GetRasterBand(11).ReadAsArray(topr, topl, pixc, pixr)
    NIRmean = tile.GetRasterBand(13).ReadAsArray(topr, topl, pixc, pixr)
    NIRp10 = tile.GetRasterBand(15).ReadAsArray(topr, topl, pixc, pixr)
    BmeanC = tile.GetRasterBand(17).ReadAsArray(topr, topl, pixc, pixr)
    GmeanC = tile.GetRasterBand(18).ReadAsArray(topr, topl, pixc, pixr)
    RmeanC = tile.GetRasterBand(19).ReadAsArray(topr, topl, pixc, pixr)
    BmeanDIS = tile.GetRasterBand(21).ReadAsArray(topr, topl, pixc, pixr)
    GmeanDIS = tile.GetRasterBand(22).ReadAsArray(topr, topl, pixc, pixr)
    RmeanDIS = tile.GetRasterBand(23).ReadAsArray(topr, topl, pixc, pixr)

    # Rescale
    out1 = Stretch_02_90(Gp10)
    out2 = Stretch_02_90(Rp10)
    out3 = Stretch_02_90(RmeanDIS)
    out4 = Stretch_02_98(GmeanDIS)
    out5 = Stretch_02_98(BmeanDIS)

    # Apply Sato filter
    out1_SATO = Sato(out1)
    out2_SATO = Sato(out2)
    out3_SATO = Sato(out3)
    out4_SATO = Sato(out4)
    out5_SATO = Sato(out5)

    ####################### FEATURE DETECTION #######################

    #### 1. Detect baseline ####
    out3_SATOthresh = np.where(out3_SATO >= 0.07, 1, 0) # Threshold sato output

    # Hough line transformation:
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 350  # angular resolution in radians of the Hough grid
    threshold = 100  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 3  # maximum gap in pixels between connectable line segments
    line_image = np.copy(out3_SATOthresh) * 0  # creating a blank to draw lines on
    line_MAJOR = HughLines(out3_SATOthresh)

    #### 2. Refine detection with Random Forest ####

    # Array configuration for RF:

    # y processing
    MAJ = line_MAJOR # Hugh lines output as training set
    maj_y = MAJ.reshape(pixr*pixc) # flatten array
    lf_y = maj_y[maj_y==1] # select all demarcations
    other_y = np.zeros_like(lf_y) # select all non-demarcations
    # x processing
    x_arr = np.dstack([out1_SATO, out2_SATO, out3_SATO, out4_SATO, out5_SATO]) # create stacked array 	with all texture inputs
    test = x_arr.reshape(pixr*pixc, x_arr.shape[2]) # flatten 3d array into 2d
    xx_lf = test[maj_y==1] # select all pixels that are demarcations
    xx_oth_all = test[maj_y==0] # select all pixels that are not demarcations
    xx_oth_indices = np.random.choice(xx_oth_all.shape[0], size=other_y.shape[0], replace=False) # 	get indices for same number of non-demarcation pixels as y
    xx_oth = xx_oth_all[xx_oth_indices,:] # select non-demarcation pixels using indice
    y_arr_tr = np.concatenate([lf_y, other_y]) # y_train -> target values (demarcations)
    x_arr_tr = np.concatenate([xx_lf, xx_oth], axis=0) # X_train -> input sample values (texture)

    # Create RF classifier model:
    model = RandomForestClassifier(n_estimators=100, #number of trees in the forest. The larger the 	better, but also the longer it will take to compute.
                                   max_features='sqrt', # Size of the random subsets of features to 	consider when splitting a node.
                                                        # The lower the greater the reduction of 	variance, but also the greater the increase in bias.
                                                        # Empirically good default values are 		max_features=1.0 or equivalently max_features=None (always considering all features instead 	of a random subset) for regression problems,
                                                        # and max_features="sqrt" (using a random 	subset of size sqrt(n_features)) for classification task (where n_features is the number of 	features in the data).
                                   criterion='gini', # The function to measure the quality of a split
                                   max_depth=None, # Use max_depth to control the size of the tree to 	prevent overfitting
                                   min_samples_split=2, # Use min_samples_split or min_samples_leaf 	to ensure that multiple samples inform every decision in the tree, by controlling which 	splits will be considered.
                                                        # A very small number will usually mean the 	tree will overfit,
                                                        # whereas a large number will prevent the 	tree from learning the data.
                                                        # Try min_samples_leaf=5 as an initial value.
                                   min_samples_leaf=1,
                                   min_weight_fraction_leaf=0.0, # f the samples are weighted, it 	will be easier to optimize the tree structure using weight-based pre-pruning criterion such 	as min_weight_fraction_leaf, which ensure that leaf nodes contain at least a fraction of the 	overall sum of the sample weights.
                                   max_leaf_nodes=None, min_impurity_decrease=0.0,
                                   bootstrap=True, oob_score=False, # Parameter cross-validation
                                   n_jobs=None, # Parallel construction of the trees and the parallel 	computation of the predictions
                                                # If n_jobs=k then computations are partitioned into 	k jobs, and run on k cores of the machine.
                                                # If n_jobs=-1 then all cores available on the 		machine are used.
                                   random_state=None, # Controls both the randomness of the 		bootstrapping of the samples used when building trees
                                                      # (if bootstrap=True) and the sampling of the 	features to consider when looking for the best split
                                                      # at each node (if max_features < n_features)
                                   verbose=0, # Controls the verbosity when fitting and predicting
                                   warm_start=False,
                                   class_weight=None, # Balance your dataset before training to 	prevent the tree from being biased toward the classes that are dominant
                                                      # In the form {class_label: weight}. If not 	given, all classes are supposed to have weight one.
                                   ccp_alpha=0.0,
                                   max_samples=None # Sub-sample size is controlled with the 		max_samples parameter if bootstrap=True (default), otherwise the whole dataset is used to 	build each tree
                                  )
    model.fit(x_arr_tr, y_arr_tr) # train model
    pred = model.predict_proba(test) # apply trained model to test data
    # Extract probability scores
    prob1 = pred[:, 1]
    prob0 = pred[:, 0]
    # Re-shape into 2d arrays
    prob1_2d = prob1.reshape(pixr,pixc)
    prob0_2d = prob0.reshape(pixr,pixc)
    # Threshold according to select probability
    RF_out = np.where(prob1_2d > 0.5, 1, 0) # np.where(condition[, x, y])  condition : When True, 	yield x, otherwise yield y.

    #### 3. Processing RF output ####

    # Morphological processing
    closed = closing(RF_out, footprint=square(2), out=None)
    RF_sr = RemoveSmall(closed,40) # remove according to area threshold
    RF_sr = erosion(RF_sr, footprint=square(3), out=None)
    RF_sr = RemoveSmall(RF_sr,50)
    RF_sr = RemoveFloatingBlobs(RF_sr,35) # remove according to major axis threshold
    filled = remove_small_holes(RF_sr, area_threshold=50, connectivity=0, in_place=False, out=None)
    filled = closing(filled, footprint=square(2), out=None)

    # Hough line transformation
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 350  # angular resolution in radians of the Hough grid
    threshold = 45  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20  # minimum number of pixels making up a line
    max_line_gap = 4  # maximum gap in pixels between connectable line segments
    line_eroded = HughLines(filled)

    # Obtain coded output (Morphological processing round 2)
    ALL_clean = RemoveSmall(line_eroded,150) # remove according to area threshold
    ALL_clean = closing(ALL_clean, footprint=square(3), out=None)
    MAJOR = remove_small_holes(ALL_clean, area_threshold=40, connectivity=0, in_place=False, 		out=None)
    MAJOR_clean = RemoveShort(MAJOR,50) # remove according to length threshold
    CODED = MAJOR_clean + ALL_clean
    return CODED

"""## Parallel processing"""

# ####################################### PROTECT MAIN LOOP FOR PARALLEL PROCESSING ########################### #
if __name__ == '__main__':
# ####################################### SET TIME-COUNT ###################################################### #
        starttime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        print("--------------------------------------------------------")
        print("Starting process, time: " + starttime)
        print("")
# ####################################### FILES AND FOLDER-PATHS ############################################## #
        # General folder path, tileID
        workFolder = "A:/_BioGeo/giorgioo/Analysis_linearFeatures/"
        tileFolder = "A:/_BioGeo/giorgioo/Analysis_linearFeatures/_NewData/S2/Full_Year/"
        outputFolder = "A:/_BioGeo/giorgioo/Analysis_linearFeatures/Output/"
        nr_cores = 4
        output_TILE = bt.baumiFM.CreateFolder(outputFolder + "window" + str("{:02d}".format(tileID)) + "/")

# ####################################### START PROCESSING #################################################### #

# (1) INSTANTIATE A JOB-LIST AND POPULATE IT
        jobList = [] # Make a list of strings and send to the parallelization function
        # Populate joblist
        tilesLYR = tiles.GetLayer()
        tilesFEAT = tilesLYR.GetNextFeature()
        while tilesFEAT:
            # Get the tiles ID, instantiate job via dictionary
            tileID = tilesFEAT.GetField("Id")
            Chaco_YN = tilesFEAT.GetField("Chaco")
            if Chaco_YN == 1:
                job = {'id': tileID, 'outputBurned': output_BA, 'outputSize': output_BA_size}
                jobList.append(job)
                tilesFEAT = tilesLYR.GetNextFeature()

# (2) KICK OFF THE JOBLIST TO THE CLUSTER ALTERNATIVELY RUN IT SEQUENTIALLY
        Parallel(n_jobs = nr_cores)(delayed(WorkerFunction)(i) for i in tqdm(jobList))
        #for job in jobList:
            if job['id'] in []:
                WorkerFunction(job)
                print("")

#### TO INCLUDE IN LOOP ONCE CORE IS ASSIGNED:

#### 1. Load tile ####
    tile = LoadTile(tileID)

#### 2. Process tile using moving window (2nd embedded loop) ####
    # Create output array the size of the tile and

    # Create array/moving window loop
    cols = 1000
    rows = 1000
    topright = i # topright = Step window horizontally
    topleft = j # topleft = Step window vertically
    # Detection
    output = DetectFeatures(cols,rows,topright,topleft)
    # Write out each window output to the master tile output
    #...


#### 3. Write out final file to disk
CopyRasterToDisk(outRas, cols, rows, topright, topleft, gt, pr, type, outName)


# ##################################### END TIME-COUNT AND PRINT TIME STATS#################################### #
print("")
endtime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("start: " + starttime)
print("end: " + endtime)
print("")