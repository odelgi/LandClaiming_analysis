//========== Required packages ==========

// * Google Earth Engine API

// ========== Required inputs ==========

// * Sentinel-2 MSI: MultiSpectral Instrument, Level-2A 

// * geometry = Randomly selected 10km2 blocks

// ========== Parameters ==========

/**
 * Function to mask clouds using the Sentinel-2 QA band
 * @param {ee.Image} image Sentinel-2 image
 * @return {ee.Image} cloud masked Sentinel-2 image
 */
 
function maskS2clouds(image) {
  var qa = image.select('QA60');

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));

  return image.updateMask(mask).divide(10000);
}

// Define function to get bands of interest from TM
function selectbands(img) {
  return img.select(
        ['B2', 'B3', 'B4']);
}

// clip collection to aoi
function clp(img) {
  return img.clip(geometry)
}
// ========== Load inputs ==========

//load blocks
var geometrty = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/HexGrid10km2_100RandomSelected');
var GranChaco = ee.FeatureCollection('projects/ee-oliviadelgiorgio/assets/GranChaco');

// ========== Load and filter image collection ==========

var S2collection_median = ee.ImageCollection('COPERNICUS/S2_SR')
                  .filterDate('2020-01-01', '2020-12-31')
                  // Pre-filter to get less cloudy granules.
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
                  .map(maskS2clouds)
                  .filterBounds(geometry)
                  .map(selectbands)
                  .map(clp)
                  .median();

var visualization = {
  min: 0.0,
  max: 0.3,
  bands: ['B4', 'B3', 'B2'],
};

Map.centerObject(geometry, 11);
Map.setOptions('SATELLITE');
Map.addLayer(S2collection_median, visualization, 'RGB');

// ========== Export ==========

Export.image.toDrive({
//  image: S2collection_median.clip(geometry2).toFloat(), 
  image: S2collection_median.clip(geometry),
  description: 'S2collection_median', 
  folder: 'DemAnalysis_ValidationS2', 
  fileNamePrefix: 'S2collection_median',
  scale: 10, 
  crs: 'EPSG:5070', 
  maxPixels: 1e13,
  region: geometry, 
  skipEmptyTiles: true
});

