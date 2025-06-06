"""
-*- Code to make claiming metrics and deforestation metrics (Baumann et al. 2022) comparable -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3
2023-12-19 15:02:19

"""
import arcpy

def RelatingMetrics():  # Relating Metrics

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    GranChaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\LandCover_InputMasks.gdb\\GranChaco"
    Activeness_aggr_4x4 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\Activeness_aggr_4x4")
    Density_weighted = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_weighted")
    Density_Weighted_NaturalClasses = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_Weighted_NaturalClasses")
    Density_Unweighted_NaturalClasses = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_Unweighted_NaturalClasses")
    Density_unweighted = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Density.gdb\\Density_unweighted")
    PeakPeriod_classified = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\PeakPeriod_classified")
    PeakPeriod_unclassified = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\PeakPeriod_unclassified")
    RecentActivity_2Classes = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_2Classes")
    RecentActivity_FrontierClasses = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\ClaimTiming.gdb\\RecentActivity_FrontierClasses")
    Speed_NaturalClasses = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\Speed_NaturalClasses")
    Speed_unclassified = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\BasicMetrics\\Speed.gdb\\Speed_unclassified")
    HexGrid_ERLfootprint_Chaco_3_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint_Chaco"
    points_ERLfootprint = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint"
    Activeness_aggr_4x4_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\Activeness_aggr_4x4")
    CropTransitionPasture_aggr_4x4 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\CropTransitionPasture_aggr_4x4")
    FastMediumSlow_aggr_10x10 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\FastMediumSlow_aggr_10x10")
    HighMediumLow_Woodland = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\HighMediumLow_Woodland")
    OnsetYR_aggr_4x4 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\OnsetYR_aggr_4x4")
    ProgLeapf_aggr_4x4 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\ProgLeapf_aggr_4x4")
    Dem_BasicMetricsJoined = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined"
    HexGrid_10km2_points_3_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points"
    HexGrid_ERLmetrics = "HexGrid_ERLmetrics"
    ProgLeapf_aggr_4x4_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\ProgLeapf_aggr_4x4")
    OnsetYR_aggr_4x4_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\OnsetYR_aggr_4x4")
    HighMediumLow_Woodland_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\HighMediumLow_Woodland")
    FastMediumSlow_aggr_10x10_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\FastMediumSlow_aggr_10x10")
    CropTransitionPasture_aggr_4x4_3_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Inputs\\Baumann2022_Metrics.gdb\\CropTransitionPasture_aggr_4x4")

    # Process: Generate Tessellation (Generate Tessellation) (management)
    HexGrid_10km2 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2"
    arcpy.management.GenerateTessellation(Output_Feature_Class=HexGrid_10km2, Extent="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="HEXAGON", Size="10 SquareKilometers", Spatial_Reference="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Clip (Clip) (analysis)
    HexGrid_10km2_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco"
    arcpy.analysis.Clip(in_features=HexGrid_10km2, clip_features=GranChaco, out_feature_class=HexGrid_10km2_Chaco, cluster_tolerance="")

    # Process: Generate Tessellation (2) (Generate Tessellation) (management)
    HexGrid_ERLfootprint_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint"
    arcpy.management.GenerateTessellation(Output_Feature_Class=HexGrid_ERLfootprint_2_, Extent="-67.6921933706275 -33.8012113011605 -55.7085496100605 -17.5589172785737 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="HEXAGON", Size="1.5 SquareKilometers", Spatial_Reference="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Clip (2) (Clip) (analysis)
    HexGrid_ERLfootprint_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint_Chaco"
    arcpy.analysis.Clip(in_features=HexGrid_ERLfootprint_2_, clip_features=GranChaco, out_feature_class=HexGrid_ERLfootprint_Chaco, cluster_tolerance="")

    # Process: Grid To Point (2) (Feature To Point) (management)
    points_ERLmetrics = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint"
    arcpy.management.FeatureToPoint(in_features=HexGrid_ERLfootprint_Chaco, out_feature_class=points_ERLmetrics, point_location="CENTROID")

    # Process: Reclassify (2) (Reclassify) (sa)
    frontier_footprint = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\ERL_FrontierFootprint_raster"
    Reclassify_2_ = frontier_footprint
    frontier_footprint = arcpy.sa.Reclassify(in_raster=Activeness_aggr_4x4, reclass_field="Value", remap="0 NODATA;1 1;2 1;3 1", missing_values="DATA")
    frontier_footprint.save(Reclassify_2_)

    # Process: Extract Values to Points (Extract Values to Points) (sa)
    points_ERLfootprintExtracted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprintExtracted"
    arcpy.sa.ExtractValuesToPoints(in_point_features=points_ERLmetrics, in_raster=frontier_footprint, out_point_features=points_ERLfootprintExtracted, interpolate_values="NONE", add_attributes="VALUE_ONLY")

    # Process: Spatial Join (2) (Spatial Join) (analysis)
    HexGrid_ERLfootprint = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint"
    arcpy.analysis.SpatialJoin(target_features=HexGrid_10km2_Chaco, join_features=points_ERLfootprintExtracted, out_feature_class=HexGrid_ERLfootprint, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,GRID_ID,0,12;Shape_length \"Shape_length\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,Shape_length,-1,-1;Shape_area \"Shape_area\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,Shape_area,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Grid To Point (Feature To Point) (management)
    HexGrid_points = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points"
    arcpy.management.FeatureToPoint(in_features=HexGrid_10km2_Chaco, out_feature_class=HexGrid_points, point_location="CENTROID")

    # Process: Reclassify (Reclassify) (sa)
    Reclass_Speed = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Reclass_Speed"
    Reclassify = Reclass_Speed
    Reclass_Speed = arcpy.sa.Reclassify(in_raster=Speed_NaturalClasses, reclass_field="Value", remap="1 3;2 2;3 1", missing_values="DATA")
    Reclass_Speed.save(Reclassify)

    # Process: Extract Multi Values to Points (Extract Multi Values to Points) (sa)
    HexGrid_10km2_points = arcpy.sa.ExtractMultiValuesToPoints(in_point_features=HexGrid_points, in_rasters=[[Density_weighted, "DensityWeighted_1"], [Density_Weighted_NaturalClasses, "DensityWeighted_NaturalClasses_1"], [Density_Unweighted_NaturalClasses, "DensityUnweighted_NaturalClasses_1"], [Density_unweighted, "DensityUnweighted_1"], [PeakPeriod_classified, "PeakPeriod_Classified_1"], [PeakPeriod_unclassified, "PeakPeriod_Unclassified_1"], [RecentActivity_2Classes, "RecentActivity_2Classes_1"], [RecentActivity_FrontierClasses, "RecentActivity_FrontierClasses_1"], [Reclass_Speed, "Speed_3Classes_1"], [Speed_unclassified, "Speed_Unclassified_1"]], bilinear_interpolate_values="NONE")
    .save(Extract_Multi_Values_to_Points)

    # Process: Spatial Join (3) (Spatial Join) (analysis)
    Dem_BasicMetricsJoined_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\MetricsAnalysis_manual\\Footprint\\Density_FieldsMasked.gdb\\Dem_BasicMetricsJoined"
    arcpy.analysis.SpatialJoin(target_features=HexGrid_10km2_Chaco, join_features=HexGrid_10km2_points, out_feature_class=Dem_BasicMetricsJoined_2_, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,GRID_ID,0,12;Shape_length \"Shape_length\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,Shape_length,-1,-1;Shape_area \"Shape_area\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_Chaco,Shape_area,-1,-1;GRID_ID_1 \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,GRID_ID,0,12;Shape_length_1 \"Shape_length\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,Shape_length,-1,-1;Shape_area_1 \"Shape_area\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,Shape_area,-1,-1;ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ORIG_FID,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Extract Multi Values to Points (2) (Extract Multi Values to Points) (sa)
    Updated_point_features = arcpy.sa.ExtractMultiValuesToPoints(in_point_features=points_ERLfootprint, in_rasters=[[Activeness_aggr_4x4_3_, "Activeness_aggr_4x4_1"], [CropTransitionPasture_aggr_4x4, "CropTransitionPasture_aggr_4x4_1"], [FastMediumSlow_aggr_10x10, "FastMediumSlow_aggr_10x10_1"], [HighMediumLow_Woodland, "HighMediumLow_Woodland_1"], [OnsetYR_aggr_4x4, "OnsetYR_aggr_4x4_1"], [ProgLeapf_aggr_4x4, "ProgLeapf_aggr_4x4_1"]], bilinear_interpolate_values="NONE")
    .save(Extract_Multi_Values_to_Points_2_)

    # Process: Spatial Join (Spatial Join) (analysis)
    HexGridSMALL_ERLmetricsExtracted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\HexGridSMALL_ERLmetricsExtracted"
    arcpy.analysis.SpatialJoin(target_features=HexGrid_ERLfootprint_Chaco_3_, join_features=Updated_point_features, out_feature_class=HexGridSMALL_ERLmetricsExtracted, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint_Chaco,GRID_ID,0,12;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint_Chaco,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\HexGrid_ERLfootprint_Chaco,Shape_Area,-1,-1;GRID_ID_1 \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,ORIG_FID,-1,-1;Activeness_aggr_4x4 \"Activeness_aggr_4x4\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,Activeness_aggr_4x4,-1,-1;CropTransitionPasture_aggr_4x4 \"CropTransitionPasture_aggr_4x4\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,CropTransitionPasture_aggr_4x4,-1,-1;FastMediumSlow_aggr_10x10 \"FastMediumSlow_aggr_10x10\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,FastMediumSlow_aggr_10x10,-1,-1;HighMediumLow_Woodland \"HighMediumLow_Woodland\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,HighMediumLow_Woodland,-1,-1;OnsetYR_aggr_4x4 \"OnsetYR_aggr_4x4\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,OnsetYR_aggr_4x4,-1,-1;ProgLeapf_aggr_4x4 \"ProgLeapf_aggr_4x4\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_FrontierFootprint.gdb\\points_ERLfootprint,ProgLeapf_aggr_4x4,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Polygon to Raster (Polygon to Raster) (conversion)
    HexGrid_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\HexGrid__raster"
    arcpy.conversion.PolygonToRaster(in_features=HexGrid_ERLmetrics, value_field="OBJECTID", out_rasterdataset=HexGrid_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="D:\\GIS_Chapter1\\Demarcation_analysis\\MetricsAnalysis_model\\BasicMetrics\\Density.gdb\\dem_footprint_raster", build_rat="BUILD")

    # Process: Zonal Statistics (6) (Zonal Statistics) (ia)
    ZonalStats_ProgMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_ProgMAX"
    Zonal_Statistics_6_ = ZonalStats_ProgMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_ProgMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="VALUE", in_value_raster=ProgLeapf_aggr_4x4_3_, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_ProgMAX.save(Zonal_Statistics_6_)

    # Process: Zonal Statistics (5) (Zonal Statistics) (ia)
    ZonalStats_OnsetMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_OnsetMAX"
    Zonal_Statistics_5_ = ZonalStats_OnsetMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_OnsetMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="VALUE", in_value_raster=OnsetYR_aggr_4x4_3_, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_OnsetMAX.save(Zonal_Statistics_5_)

    # Process: Zonal Statistics (4) (Zonal Statistics) (ia)
    ZonalStats_WoodlandMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_WoodlandMAX"
    Zonal_Statistics_4_ = ZonalStats_WoodlandMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_WoodlandMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="VALUE", in_value_raster=HighMediumLow_Woodland_3_, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_WoodlandMAX.save(Zonal_Statistics_4_)

    # Process: Zonal Statistics (3) (Zonal Statistics) (ia)
    ZonalStats_SpeedMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_SpeedMAX"
    Zonal_Statistics_3_ = ZonalStats_SpeedMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_SpeedMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="Value", in_value_raster=FastMediumSlow_aggr_10x10_3_, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_SpeedMAX.save(Zonal_Statistics_3_)

    # Process: Zonal Statistics (2) (Zonal Statistics) (ia)
    ZonalStats_TransitionMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_TransitionMAX"
    Zonal_Statistics_2_ = ZonalStats_TransitionMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_TransitionMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="VALUE", in_value_raster=CropTransitionPasture_aggr_4x4_3_, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_TransitionMAX.save(Zonal_Statistics_2_)

    # Process: Zonal Statistics (Zonal Statistics) (ia)
    ZonalStats_ActivenessMAX = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\ZonalStats_ActivenessMAX"
    Zonal_Statistics = ZonalStats_ActivenessMAX
    with arcpy.EnvManager(cellSize="HexGrid__raster"):
        ZonalStats_ActivenessMAX = arcpy.ia.ZonalStatistics(in_zone_data=HexGrid_raster, zone_field="VALUE", in_value_raster=Activeness_aggr_4x4, statistics_type="MAXIMUM", ignore_nodata="DATA", process_as_multidimensional="CURRENT_SLICE", percentile_value=90, percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
        ZonalStats_ActivenessMAX.save(Zonal_Statistics)

    # Process: Extract Multi Values to Points (3) (Extract Multi Values to Points) (sa)
    HexGrid_10km2_points_2_ = arcpy.sa.ExtractMultiValuesToPoints(in_point_features=HexGrid_10km2_points_3_, in_rasters=[[ZonalStats_ProgMAX, "ERLmetric_ProgLeap_1"], [ZonalStats_OnsetMAX, "ERLmetric_Onset_1"], [ZonalStats_WoodlandMAX, "ERLmetric_Woodland_1"], [ZonalStats_SpeedMAX, "ERLmetric_Speed_1"], [ZonalStats_TransitionMAX, "ERLmetric_Transition_1"], [ZonalStats_ActivenessMAX, "ERLmetric_Activeness_1"]], bilinear_interpolate_values="NONE")
    .save(Extract_Multi_Values_to_Points_3_)

    # Process: Spatial Join (4) (Spatial Join) (analysis)
    DemERLmetrics_JOINED = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\ERL_MetricsComparison\\ERL_MetricsInHexGrid.gdb\\DemERLmetrics_JOINED"
    arcpy.analysis.SpatialJoin(target_features=Dem_BasicMetricsJoined, join_features=HexGrid_10km2_points_2_, out_feature_class=DemERLmetrics_JOINED, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="Join_Count \"Join_Count\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,TARGET_FID,-1,-1;GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,GRID_ID,0,12,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,ORIG_FID,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ORIG_FID,-1,-1;DensityWeighted \"DensityWeighted\" true true false 4 Float 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,DensityWeighted,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,DensityWeighted,-1,-1;DensityWeighted_NaturalClasses \"DensityWeighted_NaturalClasses\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,DensityWeighted_NaturalClasses,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,DensityWeighted_NaturalClasses,-1,-1;DensityUnweighted_NaturalClasses \"DensityUnweighted_NaturalClasses\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,DensityUnweighted_NaturalClasses,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,DensityUnweighted_NaturalClasses,-1,-1;DensityUnweighted \"DensityUnweighted\" true true false 4 Float 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,DensityUnweighted,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,DensityUnweighted,-1,-1;PeakPeriod_Classified \"PeakPeriod_Classified\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,PeakPeriod_Classified,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,PeakPeriod_Classified,-1,-1;PeakPeriod_Unclassified \"PeakPeriod_Unclassified\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,PeakPeriod_Unclassified,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,PeakPeriod_Unclassified,-1,-1;RecentActivity_2Classes \"RecentActivity_2Classes\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,RecentActivity_2Classes,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,RecentActivity_2Classes,-1,-1;RecentActivity_FrontierClasses \"RecentActivity_FrontierClasses\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,RecentActivity_FrontierClasses,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,RecentActivity_FrontierClasses,-1,-1;Speed_3Classes \"Speed_3Classes\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,Speed_3Classes,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,Speed_3Classes,-1,-1;Speed_Unclassified \"Speed_Unclassified\" true true false 4 Float 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,Speed_Unclassified,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,Speed_Unclassified,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\Dem_MetricsInHexGrid.gdb\\Dem_BasicMetricsJoined,Shape_Area,-1,-1;ERLmetric_ProgLeap_1 \"ERLmetric_ProgLeap_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_ProgLeap_1,-1,-1;ERLmetric_Onset_1 \"ERLmetric_Onset_1\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_Onset_1,-1,-1;ERLmetric_Woodland_1 \"ERLmetric_Woodland_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_Woodland_1,-1,-1;ERLmetric_Speed_1 \"ERLmetric_Speed_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_Speed_1,-1,-1;ERLmetric_Transition_1 \"ERLmetric_Transition_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_Transition_1,-1,-1;ERLmetric_Activeness_1 \"ERLmetric_Activeness_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\RelatingMetrics\\Dem_Metrics\\HexGrid.gdb\\HexGrid_10km2_points,ERLmetric_Activeness_1,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Hotspots_UPDATE.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Hotspots_UPDATE.gdb"):
        RelatingMetrics()
