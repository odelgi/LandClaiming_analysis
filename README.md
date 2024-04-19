# Demarcation_analysis

## An approach to map land claiming in agricultural commodity frontiers

This repository accompanies the following peer-reviewed publication: 
[del Giorgio O., Baumann M., Kuemmerle T., le Polain de Waroux Y. (2024) Revealing land control dynamics in emerging agricultural frontiers!. Submitted to: PNAS](Link).

## Project description
The continued expansion of agricultural commodity production into the world’s tropical and subtropical forests represents one of the greatest threats to Earth system functioning and adds to the harms affecting the world’s most vulnerable. With corporate and governmental accountability still lacking in many regions, monitoring these expanding frontiers of resource appropriation is essential. Specifically, detecting where land is being staked out for commodity production offers the possibility of a better understanding of the early phases of frontier development and allows for a more accurate and timely targeting of interventions and enforcement, prior to the occurrence of large-scale deforestation. Yet, for many commodity frontiers, information on land deals, agricultural rents, and deforestation permits is unavailable, not uncommonly due to the concealment of official registries and the illegal nature of land acquisitions.
The growing availability of high-resolution satellite imagery as well as increased data handling capabilities has now opened the door to the detection of proxies for land processes which ground data is often unavailable for. We made use of these to develop a remote-sensing approach to map land claiming activity occurring in forested areas prospected for agricultural commodity production. 
Our approach offers a template for the mapping of land-control indicators across large geographic extents. The focus on image morphology, rather than purely on spectral signal, makes the method modulable to differently shaped features and to higher or lower resolution input imagery. It is thus transferable to different global contexts where the specific land control change indicator will necessarily differ. 
Additionally, for the Gran Chaco, the approach provides a rapid and dependable way to continue monitoring land claiming in the region going forward. 
   
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

* All other analysis components (i.e., steps 3-13 below) were run on a workstation with the following specs:
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
   * Smallholder homestead (i.e. puesto) point data - [Data available upon request](https://www.pnas.org/doi/10.1073/pnas.2100436118)

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
9. [ClaimingMetrics_GridAggregation.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimingMetrics_GridAggregation.py) to generate claiming metrics from demarcation data.
10. [ClaimingPatterns.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimingPatterns.py) to assign aggregate pixels to the claiming pattern typology.
11. [PatternClusters.py](https://github.com/odelgi/Demarcation_analysis/blob/main/PatternClusters.py) to produce clusters from claiming patterns.
12. [RelatingMetrics.py](https://github.com/odelgi/Demarcation_analysis/blob/main/RelatingMetrics.py) to make claiming metrics and deforestation metrics (Baumann et al. 2022) comparable.
13. [ClaimVsERL_SummaryTables.py](https://github.com/odelgi/Demarcation_analysis/blob/main/ClaimVsERL_SummaryTables.py) to generate summary statistics comparing claiming and deforestation metrics.
14. [DisappearedPuestosChoropleth.py](https://github.com/odelgi/Demarcation_analysis/blob/main/DisappearedPuestosChoropleth.py) to compare claiming metrics with smallholder puesto disappearance (data from Levers et al. 2021).

### Detailed workflow

1. Linear feature detection
![DemarcationDetection_ApproachFigure](https://github.com/odelgi/Demarcation_analysis/assets/61065884/54554c50-4430-4b7f-aa06-f98410e4f3a3)

2. Isolating forest demarcations and assigning each segment a year of appearance
![Dem_PrepUPDATED](https://github.com/odelgi/Demarcation_analysis/assets/61065884/bcd289b1-f428-4bc0-8cbc-cd7c412b8f45)

3. Genarate reference demarcations for validation
<img width="1158" alt="Validation" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/5e0229ba-cb67-4546-b20c-901fc67060b4">

4. Linear correspondence analysis
<img width="1122" alt="LinearCorrespondenceUPDATE" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/c604038c-45b2-4933-9b33-311f928aaeb8">

5. Generate claiming metrics
<img width="896" alt="MetricGridAggregation_DensCorrected" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/034a860c-336a-46e3-86b9-512bf41e9ef0">

6. Assign aggregate pixels to claiming pattern typology
<img width="705" alt="ClaimingHotspotsModelUPDATE" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/8ce96581-109a-4870-9a38-cfdbe7c1791c">

7. Determine claim pattern clustering using a density-based analysis
<img width="522" alt="PatternClusters" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/5c036226-0e4a-4682-a677-b82dec876e0e">

8. Relate claiming and deforestation metrics
![RelatingMetrics_MODEL](https://github.com/odelgi/Demarcation_analysis/assets/61065884/d1237ccc-367d-407a-854e-3226f6419042)

9. Generate summary statistics comparing claiming and deforestation metrics
<img width="1089" alt="ClaimVsERL_summarytables" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/71a6b02e-ef1e-4340-a492-f821750955f3">

10. Generate hexagonal grid over which to compare the claiming metrics and the proportion of smallholder puestos disappeared by 2018
<img width="784" alt="DisappearedPuestosChoropleth" src="https://github.com/odelgi/Demarcation_analysis/assets/61065884/59f9094c-e522-4c5b-9337-fd19fde344bf">

### Updates since peer-reviewed article publication
None

## Code developers
* [Olivia del Giorgio](https://github.com/odelgi)
* Linear feature detection upscaling [Matthias Baumann](https://github.com/matthias-baumann)

### Acknowledgments
We thank S. Schulz, C. Dammann, Tim Elrick, Ruilan Shi and J. Vacirca for their administrative support.


