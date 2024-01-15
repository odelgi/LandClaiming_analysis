// Code to extract Landsat 5 and 7 imagery (for 5 period) over randomly selected hexagons for the demarcation validation.
// del Giorgio et al.

//========== Required packages ==========

// * Google Earth Engine API

// ========== Required inputs ==========

// USGS Landsat 5, Level 2, Collection 2, Tier 1 (January 1, 1984 - May 5, 2012)
  // * SR_B1: Band 1 - blue
  // * SR_B2: Band 2 - green
  // * SR_B3: Band 3 - red
  // * SR_B4: Band 4 - NIR
  // * SR_B5: Band 5 - SWIR1
  // * SR_B7: Band 7 - SWIR2
  
// * USGS Landsat 7 Level 2, Collection 2, Tier 1 (May 28, 1999 - December 10, 2023)
  // * SR_B1: Band 1 - blue
  // * SR_B2: Band 2 - green
  // * SR_B3: Band 3 - red
  // * SR_B4: Band 4 - NIR
  // * SR_B5: Band 5 - SWIR1
  // * SR_B7: Band 7 - SWIR2
  
// * aoi = Randomly selected 10km2 blocks

// Using L5 between 1986 and 1999. Switching to L7 between 2000 and 2020.
// Level 2 QA_PIXEL band (CFMask) to mask unwanted pixels.

// ========== Load inputs ==========

// --- AOI ---

//load blocks
var geometry = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/HexGrid10km2_100RandomSelected');
var GranChaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/GranChaco');

// ========== Prep functions ==========

function maskL457sr(image) {
  // Bit 0 - Fill
  // Bit 1 - Dilated Cloud
  // Bit 2 - Unused
  // Bit 3 - Cloud
  // Bit 4 - Cloud Shadow
  var qaMask = image.select('QA_PIXEL').bitwiseAnd(parseInt('11111', 2)).eq(0);
  var saturationMask = image.select('QA_RADSAT').eq(0);

  // Apply the scaling factors to the appropriate bands.
  var opticalBands = image.select('SR_B.').multiply(0.0000275).add(-0.2);
  var thermalBand = image.select('ST_B6').multiply(0.00341802).add(149.0);

  // Replace the original bands with the scaled ones and apply the masks.
  return image.addBands(opticalBands, null, true)
      .addBands(thermalBand, null, true)
      .updateMask(qaMask)
      .updateMask(saturationMask);
}

// Define function to get bands of interest from TM
function selectbands(img) {
  return img.select(
        ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4']);
}

// clip collection to aoi
function clp(img) {
  return img.clip(geometry)
}
// ========== Load, filter, and apply prep to collection ==========

// Map functions over data to produce period composites
var composite8694 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
                     .filterDate('1986-01-01', '1994-12-31')
                     .filterBounds(geometry)
                     .map(maskL457sr)
                     .map(selectbands)
                     .map(clp)
                     .median();
print('composite8694',composite8694)

var composite9599 = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
                     .filterDate('1995-01-01', '1999-12-31')
                     .filterBounds(geometry)
                     .map(maskL457sr)
                     .map(selectbands)
                     .map(clp)
                     .median();

// Switch to L7
var composite0007 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
                     .filterDate('2000-01-01', '2007-12-31')
                     .filterBounds(geometry)
                     .map(maskL457sr)
                     .map(selectbands)
                     .map(clp)
                     .median();

var composite0814 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
                     .filterDate('2008-01-01', '2014-12-31')
                     .filterBounds(geometry)
                     .map(maskL457sr)
                     .map(selectbands)
                     .map(clp)
                     .median();

var composite1520 = ee.ImageCollection('LANDSAT/LE07/C02/T1_L2')
                     .filterDate('2015-01-01', '2020-12-31')
                     .filterBounds(geometry)
                     .map(maskL457sr)
                     .map(selectbands)
                     .map(clp)
                     .median();


// Display the results
Map.centerObject(geometry, 11);
Map.setOptions('SATELLITE');
Map.addLayer(composite8694, {bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0, max: 0.3});
Map.addLayer(composite9599, {bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0, max: 0.3});
//Map.addLayer(composite0007, {bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0, max: 0.3});
//Map.addLayer(composite0814, {bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0, max: 0.3});
//Map.addLayer(composite1520, {bands: ['SR_B3', 'SR_B2', 'SR_B1'], min: 0, max: 0.3});

// ========== Export ==========

Export.image.toDrive({
  image: composite8694.clip(geometry), 
  description: 'Landsatcomposite8694', 
  folder: 'DemAnalysis_ValidationL57', 
  fileNamePrefix: 'Landsatcomposite8694',
  scale: 30, 
  crs: 'EPSG:5070',
  region: GranChaco, 
  skipEmptyTiles: true,
  maxPixels: 1e13
});

Export.image.toDrive({
  image: composite9599.clip(geometry), 
  description: 'Landsatcomposite9599', 
  folder: 'DemAnalysis_ValidationL57', 
  fileNamePrefix: 'Landsatcomposite9599',
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13,
  region: GranChaco, 
  skipEmptyTiles: true
});

Export.image.toDrive({
  image: composite0007.clip(geometry), 
  description: 'Landsatcomposite0007', 
  folder: 'DemAnalysis_ValidationL57', 
  fileNamePrefix: 'Landsatcomposite0007',
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13,
  region: GranChaco, 
  skipEmptyTiles: true
});

Export.image.toDrive({
  image: composite0814.clip(geometry), 
  description: 'Landsatcomposite0814', 
  folder: 'DemAnalysis_ValidationL57', 
  fileNamePrefix: 'Landsatcomposite0814',
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13,
  region: GranChaco, 
  skipEmptyTiles: true
});

Export.image.toDrive({
  image: composite1520.clip(geometry), 
  description: 'Landsatcomposite1520', 
  folder: 'DemAnalysis_ValidationL57', 
  fileNamePrefix: 'Landsatcomposite1520',
  scale: 30, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13,
  region: GranChaco, 
  skipEmptyTiles: true
});
