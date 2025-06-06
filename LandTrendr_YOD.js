//##########################################################################################
//               LANDTRENDR ANALYSIS - DATE OF DEMARCATION APPEARANCE DETECTION
//##########################################################################################

// date: 2023-04-11
// author: Olivia del Giorgio | olivia.delgiorgio@mail.mcgill.ca
// Available on Github (odelgi)

// To run on Google Earth Engine's code editor (https://code.earthengine.google.com/)

// LandTrendr package: Justin Braaten, Zhiqiang Yang, Robert Kennedy
// parameter definitions: https://emapr.github.io/LT-GEE/api.html#getchangemap

//========== Required packages ==========

// * Google Earth Engine API
// * LandTrendr module:
var ltgee = require('users/emaprlab/public:Modules/LandTrendr.js');

// ========== Load inputs ==========

// --- Region ---

//load Chaco boundaries
var chaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/CHACO_AdminBoundaries');
var aoi = geometry; // define area of interest -> set back to chaco if running full script

// load sub-region boundaries for export
var ARG_DRYchaco1 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco1');
var ARG_DRYchaco2 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco2');
var ARG_DRYchaco21 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco21');
var ARG_DRYchaco22 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco22');
var ARG_DRYchaco3 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco3');
var ARG_DRYchaco4 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_DRYchaco4');
var ARG_HUMIDchaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_HUMIDchaco');
var ARG_HUMIDchaco1 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_HUMIDchaco1');
var ARG_HUMIDchaco2 = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/ARG_HUMIDchaco2');
var BOL_chaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/BOL_chaco');
var PRY_HUMIDchaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/PRY_HUMIDchaco');
var PRY_DRYchaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/PRY_DRYchaco');

// --- Demarcation mask ---

//Forest demarcations subdivided by regions for ease of export
var dem_ARGdry1 = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_ARGdry1');
var dem_ARGdry2 = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_ARGdry2');
var dem_ARGdry3 = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_ARGdry3');
var dem_ARGdry4 = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_ARGdry4');
var dem_ARGhumid = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_ARGhumid');
var dem_BOL = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_BOL');
var dem_PRYdry = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_PRYdry');
var dem_PRYhumid = ee.Image('projects/ee-oliviadelgiorgio/assets/dem_PRYhumid');

// Mosaic together to create a single mask:
var dem_total = ee.ImageCollection([dem_ARGdry1, dem_ARGdry2, dem_ARGdry3, dem_ARGdry4, dem_ARGhumid, dem_BOL, dem_PRYdry,dem_PRYhumid]).mosaic();
//print('dem_total',dem_total)

//##########################################################################################
//                                    START INPUTS
//##########################################################################################

// define collection parameters
var startYear = 1990;
var endYear = 2020;
var startDay = '04-20';
var endDay = '07-20';
var aoi = geometry; //set back to chaco if running full analysis
var index = 'TCW'; 

var maskThese = ['cloud', 'shadow', 'snow', 'water'];

// define landtrendr parameters
var runParams = { 
  maxSegments:            6,
  spikeThreshold:         0.9,
  vertexCountOvershoot:   3,
  preventOneYearRecovery: true,
  recoveryThreshold:      0.25,
  pvalThreshold:          0.05,
  bestModelProportion:    0.75,
  minObservationsNeeded:  6
};

// define change parameters
var changeParams = {
  delta:  'loss',
  sort:   'greatest',
  year:   {checked:true, start:1990, end:2020},
  mag:    {checked:false, value:100,  operator:'>'},
  dur:    {checked:false, value:4,    operator:'<'},
  preval: {checked:false, value:300,  operator:'>'},
  mmu:    {checked:false, value:11},
};

//##########################################################################################
//                                    END INPUTS
//##########################################################################################

// add index to changeParams object
changeParams.index = index;

// run landtrendr
var lt = ltgee.runLT(startYear, endYear, startDay, endDay, aoi, index, [], runParams, maskThese);

// get the change map layers
var changeImg = ltgee.getChangeMap(lt, changeParams);

//--------------------------------------------------------------------
//               Perpare and apply demarcation mask
//--------------------------------------------------------------------

// keep only binary values for mask (i.e. exclude NODATA values -> 255)
var mask = dem_total;
//print('mask',mask);

// masks what is demarcation
var changeImg_masked = changeImg.updateMask(mask); 

//--------------------------------------------------------------------
//               Perpare and apply demarcation mask
//--------------------------------------------------------------------

// set visualization dictionaries
var palette = ['#9400D3', '#4B0082', '#0000FF', '#00FF00', '#FFFF00', '#FF7F00', '#FF0000'];
var yodVizParms = {
  min: startYear,
  max: endYear,
  palette: palette
};

var magVizParms = {
  min: 200,
  max: 800,
  palette: palette
};

// display the change attribute map - note that there are other layers - print changeImg to console to see all
Map.setOptions('SATELLITE');
Map.centerObject(geometry, 11);
//Map.addLayer(changeImg.select(['mag']), magVizParms, 'Magnitude of Change');
Map.addLayer(changeImg_masked.select(['yod']), yodVizParms, 'yod TCW masked');

Map.addLayer(mask, magVizParms, 'dem mask');

// export change data to google drive
//var region = chaco.buffer(100000).bounds();
//var exportImg_TCW = changeImg_masked.clip(chaco).unmask(0).short();


Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_DRYchaco1', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_DRYchaco1', 
  region: ARG_DRYchaco1, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_DRYchaco21', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_DRYchaco21', 
  region: ARG_DRYchaco21, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_DRYchaco22', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_DRYchaco22', 
  region: ARG_DRYchaco22, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_DRYchaco3', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_DRYchaco3', 
  region: ARG_DRYchaco3, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_DRYchaco4', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_DRYchaco4', 
  region: ARG_DRYchaco4, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_HUMIDchaco1', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_HUMIDchaco1', 
  region: ARG_HUMIDchaco1, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'ARG_HUMIDchaco2', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'ARG_HUMIDchaco2', 
  region: ARG_HUMIDchaco2, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'BOL_chaco', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'BOL_chaco', 
  region: BOL_chaco, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'PRY_HUMIDchaco', 
  folder: 'lt-gee_TCW_19852020', 
  fileNamePrefix: 'PRY_HUMIDchaco', 
  region: PRY_HUMIDchaco, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});

Export.image.toDrive({
  image: exportImg_TCW, 
  description: 'PRY_DRYchaco', 
  folder: 'lt-gee_TCW_19902020', 
  fileNamePrefix: 'PRY_DRYchaco', 
  region: PRY_DRYchaco, 
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13
});
