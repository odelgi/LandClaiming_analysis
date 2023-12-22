"""
-*- Code to generate claiming metrics from demarcation datase -*-

del Giorgio et al. 
ArcGIS Pro version X
2023-12-19 15:01:23

5 metrics produced:
    1. Claiming density (unweighted)
    2. Claiming density (weighted)
    3. Peak claiming period
    4. Last claiming activity
    5. Claiming speed

"""
import arcpy
from arcpy.sa import *

def MetricsGridAggregation():  # Model to generate claiming metrics from stats on 10x10km grid (aggregation)

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    Demarcations = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\DemFINAL_Input.gdb\\dem_YOD1985_final"
    Fields_Polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\Fields_Polygon"
    LC_Other_Polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\LC_Other_polygon"
    Input_true_raster_or_constant_value = 0
    TotalCellsMask = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\TotalCellsMask"
    ZonalStats_demSUM = arcpy.Raster("ZonalStats_demSUM")
    Gran_Chaco_Limit = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\GranChaco"
    Gran_Chaco_Limit_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\GranChaco"
    ZonalStats_masksSUM_CORRECTED = arcpy.Raster("ZonalStats_masksSUM_CORRECTED")
    ZonalStats_totalSUM = arcpy.Raster("ZonalStats_totalSUM")

    # Process: Generate Tessellation (Generate Tessellation) (management)
    GenerateTessellation = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\GenerateTessellation"
    arcpy.management.GenerateTessellation(Output_Feature_Class=GenerateTessellation, Extent="-67.6921933706275 -33.8012113011605 -55.7671398818405 -17.6139385997885 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="SQUARE", Size="100 SquareKilometers", Spatial_Reference="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Copy Features (Copy Features) (management)
    Grid_density_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Grid_density"
    arcpy.management.CopyFeatures(in_features=GenerateTessellation, out_feature_class=Grid_density_, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

    # Process: Polyline to Raster - Density (Polyline to Raster) (conversion)
    dem_footprint_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\dem_footprint_raster"
    arcpy.conversion.PolylineToRaster(in_features=Demarcations, value_field="DEM", out_rasterdataset=dem_footprint_raster, cell_assignment="MAXIMUM_LENGTH", priority_field="NONE", cellsize="D:\\GIS_Chapter1\\Demarcation_analysis\\PrepDemarcations_model\\Model_inputs\\GEE_LandTrendr_YOD.gdb\\MOSAIC_TCW_yod1985", build_rat="BUILD")

    # Process: Zonal Statistics - Sum (Dem) (Zonal Statistics) (sa)
    dem_SUM = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ZonalStats_demSUM"
    Zonal_Statistics_Sum_Dem_ = dem_SUM
    dem_SUM = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=dem_footprint_raster, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    dem_SUM.save(Zonal_Statistics_Sum_Dem_)

    # Process: Merge (Merge) (management)
    merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\Fields_Other_Merge"
    arcpy.management.Merge(inputs=[Fields_Polygon, LC_Other_Polygon], output=merged, field_mappings="Id \"Id\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,Id,-1,-1;gridcode \"gridcode\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,gridcode,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Area,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Polygon to Raster - Mask (Polygon to Raster) (conversion)
    mask_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\TotalMask_raster"
    with arcpy.EnvManager(cellSize=dem_footprint_raster, extent=dem_footprint_raster, snapRaster=dem_footprint_raster):
        arcpy.conversion.PolygonToRaster(in_features=merged, value_field="gridcode", out_rasterdataset=mask_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=dem_footprint_raster, build_rat="BUILD")

    # Process: Zonal Statistics - Sum (Mask) (Zonal Statistics) (sa)
    with_null = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\ZonalStats_maskSUM"
    Zonal_Statistics_Sum_Mask_ = with_null
    with_null = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=mask_raster, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    with_null.save(Zonal_Statistics_Sum_Mask_)

    # Process: Is Null (Is Null) (sa)
    null_identified = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\ZonalStats_maskSUM_IsNull"
    Is_Null = null_identified
    null_identified = arcpy.sa.IsNull(in_raster=with_null)
    null_identified.save(Is_Null)

    # Process: Con (Con) (sa)
    mask_SUM_CORRECTED = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\ZonalStats_masksSUM_CORRECTED"
    Con = mask_SUM_CORRECTED
    mask_SUM_CORRECTED = arcpy.sa.Con(in_conditional_raster=null_identified, in_true_raster_or_constant=Input_true_raster_or_constant_value, in_false_raster_or_constant=with_null, where_clause="Value = 1")
    mask_SUM_CORRECTED.save(Con)

    # Process: Polygon to Raster - Total (Polygon to Raster) (conversion)
    total_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\TotalCells_raster"
    with arcpy.EnvManager(extent=dem_footprint_raster, snapRaster=dem_footprint_raster):
        arcpy.conversion.PolygonToRaster(in_features=TotalCellsMask, value_field="OBJECTID", out_rasterdataset=total_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=dem_footprint_raster, build_rat="BUILD")

    # Process: Zonal Statistics - Sum (Total) (Zonal Statistics) (sa)
    total_SUM = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\ZonalStats_totalSUM"
    Zonal_Statistics_Sum_Total_ = total_SUM
    total_SUM = arcpy.sa.ZonalStatistics(in_zone_data=Grid_density_, zone_field="GRID_ID", in_value_raster=total_raster, statistics_type="SUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    total_SUM.save(Zonal_Statistics_Sum_Total_)

    # Process: Clip Unweighted Density (Clip Raster) (management)
    density_uneweighted_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_unweighted"
    arcpy.management.Clip(in_raster=ZonalStats_demSUM, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=density_uneweighted_, in_template_dataset=Gran_Chaco_Limit, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    density_uneweighted_ = arcpy.Raster(density_uneweighted_)

    # Process: Reclassify Density - Natural Breaks (Reclassify) (sa)
    density_unweighted_natural_classes = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_Unweighted_NaturalClasses"
    Reclassify_Density_Natural_Breaks = density_unweighted_natural_classes
    density_unweighted_natural_classes = arcpy.sa.Reclassify(in_raster=density_uneweighted_, reclass_field="VALUE", remap="1 876.921569 1;876.921569 1807.588235 2;1807.588235 2847.745098 3;2847.745098 4106.882353 4;4106.882353 5749.235294 5;5749.235294 13961 6", missing_values="DATA")
    density_unweighted_natural_classes.save(Reclassify_Density_Natural_Breaks)

    # Process: Copy Grid (Copy Features) (management)
    Grid_dynamics_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\Grid"
    arcpy.management.CopyFeatures(in_features=GenerateTessellation, out_feature_class=Grid_dynamics_, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

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
    peak_period_classified_ = arcpy.sa.Reclassify(in_raster=peak_period_unclassified_, reclass_field="VALUE", remap="1986 1994.999900 1;1995 1999.999900 2;2000 2007.999900 3;2008 2014.999900 4;2015 2020 5", missing_values="DATA")
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

    # Process: Reclassify - Recent Activity (FC) (Reclassify) (sa)
    recent_activity_frontier_classes_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_FrontierClasses"
    Reclassify_Recent_Activity_FC_ = recent_activity_frontier_classes_
    recent_activity_frontier_classes_ = arcpy.sa.Reclassify(in_raster=recent_activity_unclassified_, reclass_field="Value", remap="1986 1994.999900 1;1995 1999.999900 2;2000 2007.999900 3;2008 2014.999900 4;2015 2022 5", missing_values="DATA")
    recent_activity_frontier_classes_.save(Reclassify_Recent_Activity_FC_)

    # Process: Reclassify - Recent Activity (2C) (Reclassify) (sa)
    recent_activity_2_classes_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_2Classes"
    Reclassify_Recent_Activity_2C_ = recent_activity_2_classes_
    recent_activity_2_classes_ = arcpy.sa.Reclassify(in_raster=recent_activity_unclassified_, reclass_field="VALUE", remap="1986 2017.999900 1;2018 2022 2", missing_values="DATA")
    recent_activity_2_classes_.save(Reclassify_Recent_Activity_2C_)

    # Process: Zonal Statistics - Majority (Mask) (Zonal Statistics) (sa)
    mask_field_other_aggregate_10km = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\MetricsGrid.gdb\\FieldOtherMask_Agg10km"
    Zonal_Statistics_Majority_Mask_ = mask_field_other_aggregate_10km
    mask_field_other_aggregate_10km = arcpy.sa.ZonalStatistics(in_zone_data=GenerateTessellation, zone_field="GRID_ID", in_value_raster=mask_raster, statistics_type="MAJORITY", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    mask_field_other_aggregate_10km.save(Zonal_Statistics_Majority_Mask_)

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

    # Process: Reclassify - Speed (Reclassify) (sa)
    Speed_natural_classes_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\Speed_NaturalClasses"
    Reclassify_Speed = Speed_natural_classes_
    Speed_natural_classes_ = arcpy.sa.Reclassify(in_raster=speed_unclassified_, reclass_field="VALUE", remap="0 4.153488 1;4.153489 6.131339 2;6.131340 14 3", missing_values="DATA")
    Speed_natural_classes_.save(Reclassify_Speed)

    # Process: Raster Calculator (Raster Calculator) (sa)
    density_weighted_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\ZonalStats_demSUM_weighted"
    Raster_Calculator = density_weighted_
    density_weighted_ = ZonalStats_demSUM *(1+(ZonalStats_masksSUM_CORRECTED / ZonalStats_totalSUM))
    density_weighted_.save(Raster_Calculator)

    # Process: Clip Weighted Density (Clip Raster) (management)
    density_Weighted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_weighted"
    arcpy.management.Clip(in_raster=density_weighted_, rectangle="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585", out_raster=density_Weighted, in_template_dataset=Gran_Chaco_Limit, nodata_value="2147483647", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    density_Weighted = arcpy.Raster(density_Weighted)

    # Process: Reclassify Density - Natural Breaks (2) (Reclassify) (sa)
    density_unweighted_natural_classes_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_Weighted_NaturalClasses"
    Reclassify_Density_Natural_Breaks_2_ = density_unweighted_natural_classes_2_
    density_unweighted_natural_classes_2_ = arcpy.sa.Reclassify(in_raster=density_Weighted, reclass_field="VALUE", remap="1.394332 1190.549346 1;1190.549346 2323.077931 2;2323.077931 3568.859375 3;3568.859375 5041.146535 4;5041.146535 7249.577275 5;7249.577275 14441.133789 6", missing_values="DATA")
    density_unweighted_natural_classes_2_.save(Reclassify_Density_Natural_Breaks_2_)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Hotspots_UPDATE.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Hotspots_UPDATE.gdb"):
        MetricsGridAggregation()
