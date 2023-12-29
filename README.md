# Demarcation_analysis

## Title

This repository accompanies the following peer-reviewed publication: 
[del Giorgio O., Baumann M., Hostert P., Kuemmerle T., le Polain de Waroux Y. (date) Title. Journal](Link).

## Project description
[Project description]    

![MainApproachFigure_V2](https://github.com/odelgi/Demarcation_analysis/assets/61065884/e0d2f379-0fa2-406e-b340-1627fc543708)

## Getting Started

#### Software prerequisites
* 64-bit Windows 10 
* [Python](https://www.python.org/downloads/) VERSION 3.1
* [Jupyter Notebook] (https://docs.jupyter.org/en/latest/)
* [ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview) VERSION 3.0.3
* [Google Earth Engine Code Editor](https://code.earthengine.google.com/)

#### Hardware recommendation
* The linear feature detection analysis was run at 10-m resolution for the Gran Chaco ecoregion, which spans 1,076,031 km<sup>2</sup>.
   * Run on a workstation with the following specs:
    * Intel® Core™ i9-9940X X-series Processor (14 physical cores, 19.25M Cache, up to 4.50 GHz) UPDATE
    * 64 GB RAM UPDATE
    * Samsung SSD 970 ECO Plus 500GB UPDATE
   * Linear feature detection - Run time for Gran Chaco = 

* All other analysis components (i.e., steps 3-10 below) were run on a workstation with the following specs:
   *    

#### Input data
* [Sentinel 2 imagery](https://dataspace.copernicus.eu/) - Level-2A
* Gran Chaco-specific data layers:
   * Fields (cropland and pasture) and 'other' land covers (urban areas, wetlands etc.) - [Data available upon request](https://iopscience.iop.org/article/10.1088/1748-9326/ac8b9a) 
   * [Argentine geospatial data repository]() (for road and water masks)
   * [Bolivian geospatial data repository]() (for road and water masks)
   * [Paraguayan roads](https://www.globio.info/what-is-globio) (national data not available)
   * [Paraguyan water bodies](https://www.hydrosheds.org/products/hydrorivers) (national data not available)
   * Smallholder homestead point data - [Data available upon request](https://www.pnas.org/doi/10.1073/pnas.2100436118)

## Workflow

### Overview
The analysis requires that the scripts be run in the following order:
1. [FeatureDetection_Simple.ipynb](https://github.com/odelgi/Demarcation_analysis/blob/main/FeatureDetection_Simple.ipynb) to test linear feature detection parameters .
2. [FeatureDetection_Upscaling.py](https://github.com/odelgi/Demarcation_analysis/blob/main/FeatureDetection_Upscaling.py) to upscale the linear feature detection analysis.
3. [LandTrendr_YOD](https://github.com/odelgi/Demarcation_analysis/blob/main/LandTrendr_YOD) GEE code.editor script to extract the year of detection for pixels within linear feature mask.
4. [PrepDemarcations.py]([link](https://github.com/odelgi/Demarcation_analysis/blob/main/PrepDemarcations.py)) to isolate forest demarcations from all linear features and assign each segment a year of detection.
5. [ClaimingMetrics_GridAggregation.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimingMetrics_GridAggregation.py) to generate claiming metrics from demarcation datase.
6. [file.py](link) Hotspots.
7. [RelatingMetrics.py](https://github.com/odelgi/Demarcation_analysis/blob/main/RelatingMetrics.py) to make claiming metrics and deforestation metrics (Baumann et al. 2022) comparable.
8. [ClaimVsERL_SummaryTables.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimVsERL_SummaryTables.py) to generate summary statistics comparing claiming and deforestation metrics.
9. [file.py](link) Smallholder impact.

### Workflow detailed

## Updates since peer-reviewed article publication
None

## Code developer
* [Olivia del Giorgio](https://github.com/odelgi)

## License

## Acknowledgments



