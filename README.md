# Demarcation_analysis

## An approach to map land claiming in agricultural commodity frontiers

This repository accompanies the following peer-reviewed publication: 
[del Giorgio O., Baumann M., Hostert P., Kuemmerle T., le Polain de Waroux Y. (date) Title. Journal](Link).

## Project description
[Project description]    
#### Approach summary
![MainApproachFigure_V2](https://github.com/odelgi/Demarcation_analysis/assets/61065884/e0d2f379-0fa2-406e-b340-1627fc543708)
## Getting Started

#### Software prerequisites
* 64-bit Windows 10 
* [Python](https://www.python.org/downloads/) VERSION 3.1
* [Jupyter Notebook](https://docs.jupyter.org/en/latest/)
* [ESRI ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview) VERSION 3.0.3 (including the Spatial Analyst lisence extension)
* [Google Earth Engine Code Editor](https://code.earthengine.google.com/)

#### Hardware recommendation
* The linear feature detection analysis was run at 10-m resolution for the Gran Chaco ecoregion, which spans 1,076,031 km<sup>2</sup>.
   * Run on a workstation with the following specs:
    * Intel® Core™ i9-9940X X-series Processor (14 physical cores, 19.25M Cache, up to 4.50 GHz) UPDATE
    * 64 GB RAM UPDATE
    * Samsung SSD 970 ECO Plus 500GB UPDATE
   * Linear feature detection - Run time for Gran Chaco = 

* All other analysis components (i.e., steps 3-11 below) were run on a workstation with the following specs:
   * Windows 10 Pro (Version 22H2) - 64 bit (OS build 19045.3930)
   * Intel® Core™ i7-10700 CPU @ 2.90GHz
   * 32 GB RAM

#### Input data
* [Sentinel 2 imagery](https://dataspace.copernicus.eu/) - Level-2A
* Gran Chaco-specific data layers:
   * Fields (cropland and pasture) and 'other' land covers (urban areas, wetlands etc.) - [Data available upon request](https://iopscience.iop.org/article/10.1088/1748-9326/ac8b9a) 
   * [Argentine geospatial data repository](https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/CapasSIG) (for road and water masks)
   * [Bolivian geospatial data repository](https://geo.gob.bo/) (for road and water masks)
   * [Paraguayan roads](https://www.globio.info/what-is-globio) (national data not available)
   * [Paraguyan water bodies](https://www.hydrosheds.org/products/hydrorivers) (national data not available)
   * Smallholder homestead point data - [Data available upon request](https://www.pnas.org/doi/10.1073/pnas.2100436118)

## Workflow

### Overview
The analysis requires that the scripts be run in the following order:
1. [FeatureDetection_Simple.ipynb](https://github.com/odelgi/Demarcation_analysis/blob/main/FeatureDetection_Simple.ipynb) to test linear feature detection parameters .
2. [FeatureDetection_Upscaling.py](https://github.com/odelgi/Demarcation_analysis/blob/main/FeatureDetection_Upscaling.py) to upscale the linear feature detection analysis.
3. [LandTrendr_YOD](https://github.com/odelgi/Demarcation_analysis/blob/main/LandTrendr_YOD) GEE code.editor script to extract the year of detection for pixels within linear feature mask.
4. [PrepDemarcations.py](https://github.com/odelgi/Demarcation_analysis/blob/main/PrepDemarcations.py) to isolate forest demarcations from all linear features and assign each segment a year of detection.
5. [Validation.py](https://github.com/odelgi/Demarcation_analysis/blob/main/Validation.py) to produce the demarcation reference dataset for validation.
6. [Landsat_GEEValidation.js](https://github.com/odelgi/Demarcation_analysis/blob/main/Landsat_GEEValidation.js) to extract Landsat imagery over randomly selected hexagons for the demarcation validation.
7. [S2_GEEValidation.js](https://github.com/odelgi/Demarcation_analysis/blob/main/S2_GEEValidation.js) to extract Sentinel 2 imagery over randomly selected hexagons for the demarcation validation.
8. [LinearCorrespondenceAnalysis.py](https://github.com/odelgi/Demarcation_analysis/blob/main/LinearCorrespondenceAnalysis.py) to calculate the linear correspondence between the extracted and reference demarcations.
9. [ClaimingMetrics_GridAggregation.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimingMetrics_GridAggregation.py) to generate claiming metrics from demarcation datase.
10. [ClaimingPatterns.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimingPatterns.py) to assign aggregate pixels to the claiming pattern typology.
11. [RelatingMetrics.py](https://github.com/odelgi/Demarcation_analysis/blob/main/RelatingMetrics.py) to make claiming metrics and deforestation metrics (Baumann et al. 2022) comparable.
12. [ClaimVsERL_SummaryTables.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimVsERL_SummaryTables.py) to generate summary statistics comparing claiming and deforestation metrics.
13. [file.py](link) Smallholder impact.

### Detailed workflow

1. Linear feature detection
![DemarcationDetection_ApproachFigure](https://github.com/odelgi/Demarcation_analysis/assets/61065884/54554c50-4430-4b7f-aa06-f98410e4f3a3)

2. Isolating forest demarcations and assigning each segment a year of appearance
![DemPrep_MODEL](https://github.com/odelgi/Demarcation_analysis/assets/61065884/1ad6f999-3424-499e-b060-d37a0cb0f8fc)

3. Genarate reference demarcations for validation
<img width="1158" alt="Validation" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/5e0229ba-cb67-4546-b20c-901fc67060b4">

4. Linear correspondence analysis
<img width="781" alt="LCA" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/a77dc8a4-1673-4cf6-a11f-1c36c85ecabf">

5. Generate claiming metrics
![MetricGridAggregation_MODEL](https://github.com/odelgi/Demarcation_analysis/assets/61065884/658f1848-4592-4650-81fd-69785b8bc7bb)

6. Assign aggregate pixels to claiming pattern typology
<img width="629" alt="ClaimingPatternModel" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/d5038358-b9af-4013-bf5c-1dcc4a777787">

8. Relate claiming and deforestation metrics
![RelatingMetrics_MODEL](https://github.com/odelgi/Demarcation_analysis/assets/61065884/d1237ccc-367d-407a-854e-3226f6419042)

9. Generate summary statistics comparing claiming and deforestation metrics
![ClaimVsERL summarytables](https://github.com/odelgi/Demarcation_analysis/assets/61065884/cbd56473-2516-46e4-931a-4a40a5a76a51)

10. Assess smallholder impact


### Updates since peer-reviewed article publication
None

## Code developers
* [Olivia del Giorgio](https://github.com/odelgi)
* Linear feature detection upscaling [Matthias Baumann](https://github.com/matthias-baumann)

### Acknowledgments
We thank S. Schulz and C. Dammann and J. Vacirca for their administrative support.


