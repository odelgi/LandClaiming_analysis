"""
-*- Code to produce clusters from claiming patterns -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""
import arcpy
from arcpy.ia import *

def PatternClusters():  # PatternClusters

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")
    arcpy.CheckOutExtension("3D")

    HexGrid_points = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Input.gdb\\Chaco_HexGrid_points"
    Consolidating1500 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Consolidating1500")
    Emerging1500 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Emerging1500")
    Maintained1500 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Maintained1500")

    # Process: Raster Calculator (3) (Raster Calculator) (ia)
    PatternMerge1500 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\PatternMerge1500"
    Raster_Calculator_3_ = PatternMerge1500
    PatternMerge1500 =  Consolidating1500 +  Emerging1500 + Maintained1500
    PatternMerge1500.save(Raster_Calculator_3_)


    # Process: Reclassify (3) (Reclassify) (sa)
    _3_pattern_merge = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\PatternMerge1500Reclass"
    Reclassify_3_ = _3_pattern_merge
    _3_pattern_merge = arcpy.sa.Reclassify(in_raster=PatternMerge1500, reclass_field="Value", remap="0 NODATA;1 1;2 1", missing_values="DATA")
    _3_pattern_merge.save(Reclassify_3_)


    # Process: Extract Multi Values to Points (3) (Extract Multi Values to Points) (sa)
    points_for_clustering = arcpy.sa.ExtractMultiValuesToPoints(in_point_features=HexGrid_points, in_rasters=[[_3_pattern_merge, "3Merged1500"], [Maintained1500, "Maintained1500"], [Emerging1500, "Emerging1500"], [Consolidating1500, "Consolidating1500"]], bilinear_interpolate_values="NONE")
    .save(Extract_Multi_Values_to_Points_3_)


    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    points_select_1_, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=points_for_clustering, selection_type="NEW_SELECTION", where_clause="Emerging1500 = 1", invert_where_clause="")

    # Process: Select Layer By Attribute (2) (Select Layer By Attribute) (management)
    points_select_2_, Count_2_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=points_for_clustering, selection_type="NEW_SELECTION", where_clause="Consolidating1500 = 1", invert_where_clause="")

    # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
    points_select_3_, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=points_for_clustering, selection_type="NEW_SELECTION", where_clause="F3Merged1500 = 1", invert_where_clause="")

    # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
    points_select_4_, Count_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=points_for_clustering, selection_type="NEW_SELECTION", where_clause="Maintained1500 = 1", invert_where_clause="")

    # Process: Export Features (Export Features) (conversion)
    points_emerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\Points_Emerging1500"
    if points_select_1_:
        arcpy.conversion.ExportFeatures(in_features=points_for_clustering, out_features=points_emerging, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,Chaco_HexGrid_points,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,Chaco_HexGrid_points,ORIG_FID,-1,-1;F3Merged1500 \"F3Merged1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,F3Merged1500,-1,-1;Maintained1500 \"Maintained1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Maintained1500,-1,-1;Emerging1500 \"Emerging1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Emerging1500,-1,-1;Consolidating1500 \"Consolidating1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Consolidating1500,-1,-1", sort_field=[])

    # Process: Density-based Clustering (Density-based Clustering) (stats)
    clusters_emergence = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Consolidating1500_Clust.gdb\\Points_Emerging1500_DBC"
    if points_select_1_:
        arcpy.stats.DensityBasedClustering(in_features=points_emerging, output_features=clusters_emergence, cluster_method="DBSCAN", min_features_cluster=100, search_distance="30 Kilometers", cluster_sensitivity=None, time_field="", search_time_interval="")

    # Process: Export Features (2) (Export Features) (conversion)
    points_consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\Points_Consolidating1500"
    if points_select_2_:
        arcpy.conversion.ExportFeatures(in_features=points_for_clustering, out_features=points_consolidating, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,Chaco_HexGrid_points,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,Chaco_HexGrid_points,ORIG_FID,-1,-1;F3Merged1500 \"F3Merged1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,F3Merged1500,-1,-1;Maintained1500 \"Maintained1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Maintained1500,-1,-1;Emerging1500 \"Emerging1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Emerging1500,-1,-1;Consolidating1500 \"Consolidating1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Consolidating1500,-1,-1", sort_field=[])

    # Process: Density-based Clustering (2) (Density-based Clustering) (stats)
    clusters_consolidation = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Consolidating1500_Clust.gdb\\Points_Consolidating1500_DBC"
    if points_select_2_:
        arcpy.stats.DensityBasedClustering(in_features=points_consolidating, output_features=clusters_consolidation, cluster_method="DBSCAN", min_features_cluster=100, search_distance="30 Kilometers", cluster_sensitivity=None, time_field="", search_time_interval="")

    # Process: Export Features (3) (Export Features) (conversion)
    points_merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\Points_3Merged1500"
    if points_select_3_:
        arcpy.conversion.ExportFeatures(in_features=points_for_clustering, out_features=points_merged, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,Chaco_HexGrid_points,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,Chaco_HexGrid_points,ORIG_FID,-1,-1;F3Merged1500 \"F3Merged1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,F3Merged1500,-1,-1;Maintained1500 \"Maintained1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Maintained1500,-1,-1;Emerging1500 \"Emerging1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Emerging1500,-1,-1;Consolidating1500 \"Consolidating1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Consolidating1500,-1,-1", sort_field=[])

    # Process: Density-based Clustering (3) (Density-based Clustering) (stats)
    clusters_merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Consolidating1500_Clust.gdb\\Points_3Merged1500_DBC"
    if points_select_3_:
        arcpy.stats.DensityBasedClustering(in_features=points_merged, output_features=clusters_merged, cluster_method="DBSCAN", min_features_cluster=100, search_distance="30 Kilometers", cluster_sensitivity=None, time_field="", search_time_interval="")

    # Process: Export Features (4) (Export Features) (conversion)
    points_maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Clusters_Filt1500.gdb\\Points_Maintained1500"
    if points_select_4_:
        arcpy.conversion.ExportFeatures(in_features=points_for_clustering, out_features=points_maintained, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,Chaco_HexGrid_points,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,Chaco_HexGrid_points,ORIG_FID,-1,-1;F3Merged1500 \"F3Merged1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,F3Merged1500,-1,-1;Maintained1500 \"Maintained1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Maintained1500,-1,-1;Emerging1500 \"Emerging1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Emerging1500,-1,-1;Consolidating1500 \"Consolidating1500\" true true false 2 Short 0 0,First,#,Chaco_HexGrid_points,Consolidating1500,-1,-1", sort_field=[])

    # Process: Density-based Clustering (4) (Density-based Clustering) (stats)
    clusters_maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\PatternClustering\\Consolidating1500_Clust.gdb\\Points_Maintained1500_DBC"
    if points_select_4_:
        arcpy.stats.DensityBasedClustering(in_features=points_maintained, output_features=clusters_maintained, cluster_method="DBSCAN", min_features_cluster=100, search_distance="30 Kilometers", cluster_sensitivity=None, time_field="", search_time_interval="")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\PatternClustering\Consolidating1500_Clust.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\PatternClustering\Consolidating1500_Clust.gdb"):
        PatternClusters()
