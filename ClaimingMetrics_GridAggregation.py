"""
-*- Code to generate claiming metrics from demarcation dataset -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

5 metrics produced:
    1. Claiming density (uncorrected)
    2. Claiming density (corrected)
    3. Peak claiming period
    4. Last claiming activity
    5. Claiming speed

"""

import arcpy
from arcpy.sa import *

def MetricsGridAggregation():  # Metrics Grid Aggregation

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    Grid = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics\\BasicMetrics_1500Filt\\MetricsGrid.gdb\\Grid"
    Demarcations = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Dem_FINAL.gdb\\dem_YOD1985_FILTERED1500"
    Gran_Chaco_Limit_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\GranChaco"
    GranChaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\GranChaco"
    Fields_Polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\Fields_Polygon_Chaco"
    LC_Other_Polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\LC_Other_polygon_Chaco"
    TotalCellsMask = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\TotalCellsMask"

    # Process: Generate Tessellation (Generate Tessellation) (management)
    GenerateTessellation = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\GenerateTessellation"
    with arcpy.EnvManager(extent="-61.003634125 -19.913289462 -60.280541677 -19.325354588 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]", outputCoordinateSystem="PROJCS["WGS_1984_UTM_Zone_18S",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",-75.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]"):
        arcpy.management.GenerateTessellation(Output_Feature_Class=GenerateTessellation, Extent="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="SQUARE", Size="100 SquareKilometers", Spatial_Reference="PROJCS[\"WGS_1984_UTM_Zone_18S\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",10000000.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]];-5120900 1900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision")

    # Process: Copy Grid (Copy Features) (management)
    Grid_dynamics_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\Grid"
    arcpy.management.CopyFeatures(in_features=Grid, out_feature_class=Grid_dynamics_, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Polyline to Raster - Timing (Polyline to Raster) (conversion)
    dem_claim_timing_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\dem_YOD"
    arcpy.conversion.PolylineToRaster(in_features=Demarcations, value_field="Z_Mean", out_rasterdataset=dem_claim_timing_raster, cell_assignment="MAXIMUM_LENGTH", priority_field="NONE", cellsize="D:\\GIS_Chapter1\\Demarcation_analysis\\MetricsAnalysis_manual\\Inputs\\LandCover_InputMasks.gdb\\MOSAIC_TCW_yod1985", build_rat="BUILD")

    # Process: Zonal Statistics - Majority (Peak) (Zonal Statistics) (sa)
    yod_MAJORITY = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\ZonalStats_yodMAJORITY"
    Zonal_Statistics_Majority_Peak_ = yod_MAJORITY
    yod_MAJORITY = arcpy.sa.ZonalStatistics(in_zone_data=Grid_dynamics_, zone_field="GRID_ID", in_value_raster=dem_claim_timing_raster, statistics_type="MAJORITY", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    yod_MAJORITY.save(Zonal_Statistics_Majority_Peak_)


    # Process: Clip Peak (Clip Raster) (management)
    peak_period_unclassified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\PeakPeriod_unclassified"
    arcpy.management.Clip(in_raster=yod_MAJORITY, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=peak_period_unclassified_, in_template_dataset=Gran_Chaco_Limit_2_, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    peak_period_unclassified_ = arcpy.Raster(peak_period_unclassified_)

    # Process: Reclassify - Peak Period (Reclassify) (sa)
    peak_period_classified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\PeakPeriod_classified"
    Reclassify_Peak_Period = peak_period_classified_
    peak_period_classified_ = arcpy.sa.Reclassify(in_raster=peak_period_unclassified_, reclass_field="Value", remap="1986 1994.999900 1;1995 1999.999900 2;2000 2007.999900 3;2008 2014.999900 4;2015 2020 5", missing_values="DATA")
    peak_period_classified_.save(Reclassify_Peak_Period)


    # Process: Zonal Statistics - Maximum (Recent) (Zonal Statistics) (sa)
    yod_MAXIMUM = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\ZonalStats_yodMAXIMUM"
    Zonal_Statistics_Maximum_Recent_ = yod_MAXIMUM
    yod_MAXIMUM = arcpy.sa.ZonalStatistics(in_zone_data=Grid_dynamics_, zone_field="GRID_ID", in_value_raster=dem_claim_timing_raster, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    yod_MAXIMUM.save(Zonal_Statistics_Maximum_Recent_)


    # Process: Clip Recent (Clip Raster) (management)
    recent_activity_unclassified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_unclassified"
    arcpy.management.Clip(in_raster=yod_MAXIMUM, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=recent_activity_unclassified_, in_template_dataset=Gran_Chaco_Limit_2_, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    recent_activity_unclassified_ = arcpy.Raster(recent_activity_unclassified_)

    # Process: Reclassify - Recent Activity (2C) (Reclassify) (sa)
    recent_activity_2_classes_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_2Classes"
    Reclassify_Recent_Activity_2C_ = recent_activity_2_classes_
    recent_activity_2_classes_ = arcpy.sa.Reclassify(in_raster=recent_activity_unclassified_, reclass_field="Value", remap="1986 2017.999900 1;2018 2022 2", missing_values="DATA")
    recent_activity_2_classes_.save(Reclassify_Recent_Activity_2C_)


    # Process: Copy Features (Copy Features) (management)
    Grid_density_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Grid_density"
    arcpy.management.CopyFeatures(in_features=Grid, out_feature_class=Grid_density_, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Polyline to Raster - Density (Polyline to Raster) (conversion)
    dem_footprint_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\dem_footprint_raster"
    arcpy.conversion.PolylineToRaster(in_features=Demarcations, value_field="DEM", out_rasterdataset=dem_footprint_raster, cell_assignment="MAXIMUM_LENGTH", priority_field="NONE", cellsize="D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Inputs\\LandCover_InputMasks.gdb\\MOSAIC_TCW_yod1985", build_rat="BUILD")

    # Process: Zonal Statistics - Sum (Dem) (Zonal Statistics) (sa)
    dem_SUM = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ZonalStats_demSUM"
    Zonal_Statistics_Sum_Dem_ = dem_SUM
    dem_SUM = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=dem_footprint_raster, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    dem_SUM.save(Zonal_Statistics_Sum_Dem_)


    # Process: Clip Unweighted Density (Clip Raster) (management)
    density_uneweighted_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_unweighted"
    arcpy.management.Clip(in_raster=dem_SUM, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=density_uneweighted_, in_template_dataset=GranChaco, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    density_uneweighted_ = arcpy.Raster(density_uneweighted_)

    # Process: Polyline to Raster - Speed (Polyline to Raster) (conversion)
    dem_speed_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\dem_YOD"
    arcpy.conversion.PolylineToRaster(in_features=Demarcations, value_field="Z_Mean", out_rasterdataset=dem_speed_raster, cell_assignment="MAXIMUM_LENGTH", priority_field="NONE", cellsize="D:\\GIS_Chapter1\\Demarcation_analysis\\MetricsAnalysis_manual\\Inputs\\LandCover_InputMasks.gdb\\MOSAIC_TCW_yod1985", build_rat="BUILD")

    # Process: Zonal Statistics - Standard Deviation (Speed) (Zonal Statistics) (sa)
    yod_STANDARD_DEV = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\ZonalStats_yodStandDev"
    Zonal_Statistics_Standard_Deviation_Speed_ = yod_STANDARD_DEV
    yod_STANDARD_DEV = arcpy.sa.ZonalStatistics(in_zone_data=Grid_dynamics_, zone_field="GRID_ID", in_value_raster=dem_speed_raster, statistics_type="STD", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    yod_STANDARD_DEV.save(Zonal_Statistics_Standard_Deviation_Speed_)


    # Process: Clip Speed (Clip Raster) (management)
    speed_unclassified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\Speed_unclassified"
    arcpy.management.Clip(in_raster=yod_STANDARD_DEV, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=speed_unclassified_, in_template_dataset=Gran_Chaco_Limit_2_, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    speed_unclassified_ = arcpy.Raster(speed_unclassified_)

    # Process: Merge (Merge) (management)
    merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\Fields_Other_Merge"
    arcpy.management.Merge(inputs=[Fields_Polygon, LC_Other_Polygon], output=merged, field_mappings="Id \"Id\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,Id,-1,-1;gridcode \"gridcode\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,gridcode,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Area,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Polygon to Raster - Mask (Polygon to Raster) (conversion)
    mask_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\TotalMask_raster"
    with arcpy.EnvManager(cellSize=dem_footprint_raster, extent=dem_footprint_raster, snapRaster=dem_footprint_raster):
        arcpy.conversion.PolygonToRaster(in_features=merged, value_field="gridcode", out_rasterdataset=mask_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=dem_footprint_raster, build_rat="BUILD")

    # Process: Reclassify (Reclassify) (sa)
    ForestMask = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ForestMask"
    Reclassify = ForestMask
    ForestMask = arcpy.sa.Reclassify(in_raster=mask_raster, reclass_field="VALUE", remap="0 1;1 NODATA;NODATA 1", missing_values="DATA")
    ForestMask.save(Reclassify)


    # Process: Clip Raster (2) (Clip Raster) (management)
    ForestMask_Clip = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ForestMask_Clip"
    arcpy.management.Clip(in_raster=ForestMask, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=ForestMask_Clip, in_template_dataset=GranChaco, nodata_value="", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    ForestMask_Clip = arcpy.Raster(ForestMask_Clip)

    # Process: Zonal Statistics (2) (Zonal Statistics) (sa)
    ZonalStats_ForestSum = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ZonalStats_ForestSum"
    Zonal_Statistics_2_ = ZonalStats_ForestSum
    ZonalStats_ForestSum = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=ForestMask_Clip, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    ZonalStats_ForestSum.save(Zonal_Statistics_2_)


    # Process: Polygon to Raster - Total (Polygon to Raster) (conversion)
    total_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\TotalCells_raster"
    with arcpy.EnvManager(extent=dem_footprint_raster, snapRaster=dem_footprint_raster):
        arcpy.conversion.PolygonToRaster(in_features=TotalCellsMask, value_field="OBJECTID", out_rasterdataset=total_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=dem_footprint_raster, build_rat="BUILD")

    # Process: Zonal Statistics (Zonal Statistics) (sa)
    ZonalStats_totalSum = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ZonalStats_totalSum"
    Zonal_Statistics = ZonalStats_totalSum
    ZonalStats_totalSum = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=total_raster, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    ZonalStats_totalSum.save(Zonal_Statistics)


    # Process: Raster Calculator (2) (Raster Calculator) (sa)
    ProportionForest = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ProportionForest"
    Raster_Calculator_2_ = ProportionForest
    ProportionForest = ZonalStats_ForestSum /  ZonalStats_totalSum
    ProportionForest.save(Raster_Calculator_2_)


    # Process: Raster Calculator (3) (Raster Calculator) (sa)
    DensityCorrected = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\DensityCorrected"
    Raster_Calculator_3_ = DensityCorrected
    DensityCorrected = dem_SUM /  ProportionForest
    DensityCorrected.save(Raster_Calculator_3_)


    # Process: Clip Raster (Clip Raster) (management)
    DensityCorrected_Clip = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\DensityCorrected_Clip"
    arcpy.management.Clip(in_raster=DensityCorrected, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=DensityCorrected_Clip, in_template_dataset=GranChaco, nodata_value="3.4e+38", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    DensityCorrected_Clip = arcpy.Raster(DensityCorrected_Clip)

    # Process: Set Null (Set Null) (sa)
    DensityCorrected_Thresholded = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\DensityCorrected_Thresholded"
    Set_Null = DensityCorrected_Thresholded
    DensityCorrected_Thresholded = arcpy.sa.SetNull(in_conditional_raster=DensityCorrected_Clip, in_false_raster_or_constant=DensityCorrected_Clip, where_clause="VALUE > 15000")
    DensityCorrected_Thresholded.save(Set_Null)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Metrics\Metrics_1500Filt.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Metrics\Metrics_1500Filt.gdb"):
        MetricsGridAggregation()
