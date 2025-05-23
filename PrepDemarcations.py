"""
-*- Code to isolate forest demarcations from all linear features and assign each segment a year of detection  -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3
2023-12-19 15:01:23

"""
import arcpy

def PrepDemModel():  # Prep Demarcations Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("Foundation")
    arcpy.CheckOutExtension("Defense")
    arcpy.CheckOutExtension("ImageAnalyst")

    Land_Cover_Dataset = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\LandCover_Inputs.gdb\\LandCover_2020")
    Demarcations = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\Demarcations_INPUT.gdb\\DemacationsAll_2020")
    Input_False_Constant = 1
    Chaco_road_network = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\LandCover_Inputs.gdb\\Chaco_RedVialTOTAL"
    BOL_rivers_Chaco_water_bodies = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\LandCover_Inputs.gdb\\WaterPolys_Chaco_TOTAL"
    PRY_rivers = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\LandCover_Inputs.gdb\\HydroRIVERS_Pr_ord2"
    ARG_rivers = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\LandCover_Inputs.gdb\\perennial_ArgChaco"
    Input_False_Constant_2_ = 1
    LandTrendr_Output = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_inputs\\GEE_LandTrendr_YOD.gdb\\MOSAIC_TCW_yod1985")
    Dem_yod1995_final = "Dem_yod1995_final"
    dem_YOD1985_finalProj = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj"

    # Process: Focal Statistics (Focal Statistics) (ia)
    focalized_land_cover = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\FocalSt_LC"
    Focal_Statistics = focalized_land_cover
    focalized_land_cover = arcpy.ia.FocalStatistics(in_raster=Land_Cover_Dataset, neighborhood="Rectangle 15 15 CELL", statistics_type="MAJORITY", ignore_nodata="DATA", percentile_value=90)
    focalized_land_cover.save(Focal_Statistics)

    # Process: Expand Pasture + Cropland (Expand) (sa)
    pasture_cropland_grown = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\Expand_LC"
    Expand_Pasture_Cropland = pasture_cropland_grown
    pasture_cropland_grown = arcpy.sa.Expand(in_raster=focalized_land_cover, number_cells=2, zone_values=[3, 4], expand_method="MORPHOLOGICAL")
    pasture_cropland_grown.save(Expand_Pasture_Cropland)

    # Process: Reclassify Fields (Reclassify) (3d)
    fields = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\Reclass_ExpandLC"
    arcpy.ddd.Reclassify(in_raster=pasture_cropland_grown, reclass_field="VALUE", remap="1 NODATA;2 NODATA;3 1;4 1;5 NODATA;20 NODATA;21 NODATA;22 NODATA;23 NODATA", out_raster=fields, missing_values="DATA")
    fields = arcpy.Raster(fields)

    # Process: Fields Raster to Polygon (Raster to Polygon) (conversion)
    fields_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_outputs\\LandCover_Masks.gdb\\Fields_Polygon"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=fields, out_polygon_features=fields_polygon, simplify="NO_SIMPLIFY", raster_field="", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Region Group (Region Group) (sa)
    demarcations_grouped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\DemGrouped"
    Region_Group = demarcations_grouped
    demarcations_grouped = arcpy.sa.RegionGroup(in_raster=Demarcations, number_neighbors="FOUR", zone_connectivity="WITHIN", add_link="ADD_LINK", excluded_value=0)
    demarcations_grouped.save(Region_Group)


    # Process: Set Null By Region Area - 300 (Set Null) (sa)
    nibble_mask_all = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\nibble_mask300"
    Set_Null_By_Region_Area_300 = nibble_mask_all
    nibble_mask_all = arcpy.sa.SetNull(in_conditional_raster=demarcations_grouped, in_false_raster_or_constant=Input_False_Constant, where_clause="Count < 300")
    nibble_mask_all.save(Set_Null_By_Region_Area_300)


    # Process: Nibble Small (Nibble) (sa)
    small_removed = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\nibble_output300"
    Nibble_Small = small_removed
    small_removed = arcpy.sa.Nibble(in_raster=Demarcations, in_mask_raster=nibble_mask_all, nibble_values="DATA_ONLY", nibble_nodata="PRESERVE_NODATA", in_zone_raster="")
    small_removed.save(Nibble_Small)


    # Process: Reclassify Demarcations (Reclassify) (sa)
    demarcations_reclassified = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\dem_reclassALL"
    Reclassify_Demarcations = demarcations_reclassified
    demarcations_reclassified = arcpy.sa.Reclassify(in_raster=small_removed, reclass_field="VALUE", remap="0 NODATA;1 1;2 1", missing_values="DATA")
    demarcations_reclassified.save(Reclassify_Demarcations)


    # Process: Demarcation Raster to Polygon (Raster to Polygon) (conversion)
    demarcation_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\Dem_polygonALL"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=demarcations_reclassified, out_polygon_features=demarcation_polygon, simplify="NO_SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Polygon To Centerline (Polygon To Centerline) (topographic)
    demarcation_centreline = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\dem_centreline_all"
    arcpy.topographic.PolygonToCenterline(in_features=demarcation_polygon, out_feature_class=demarcation_centreline, connecting_features=[])

    # Process: Buffer Road Network (Buffer) (analysis)
    road_network_buffered = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\Chaco_RedVialTotal_Buff100"
    arcpy.analysis.Buffer(in_features=Chaco_road_network, out_feature_class=road_network_buffered, buffer_distance_or_field="100 Meters", line_side="FULL", line_end_type="FLAT", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

    # Process: Road Polygon to Raster (Polygon to Raster) (conversion)
    road_network_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\road_buffered"
    arcpy.conversion.PolygonToRaster(in_features=road_network_buffered, value_field="OBJECTID", out_rasterdataset=road_network_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize=demarcations_reclassified, build_rat="BUILD")

    # Process: Invert Road Raster (Reclassify) (3d)
    road_network_inverted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\vial_inverted"
    arcpy.ddd.Reclassify(in_raster=road_network_raster, reclass_field="VALUE", remap="1 NODATA;NODATA 1", out_raster=road_network_inverted, missing_values="DATA")
    road_network_inverted = arcpy.Raster(road_network_inverted)

    # Process: NOTroad Raster to Polygon (Raster to Polygon) (conversion)
    NOTroad_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\NOTVial_polygon"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=road_network_inverted, out_polygon_features=NOTroad_polygon, simplify="NO_SIMPLIFY", raster_field="", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Clip - Clean Roads (Clip) (analysis)
    dem_roads_masked = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\dem_RoadsMasked_All"
    arcpy.analysis.Clip(in_features=demarcation_centreline, clip_features=NOTroad_polygon, out_feature_class=dem_roads_masked, cluster_tolerance="")

    # Process: Buffer BOL Rivers + Chaco Water Bodies (Buffer) (analysis)
    BOL_rivers_Chaco_water_buffered = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\WaterPolys_buffer400"
    arcpy.analysis.Buffer(in_features=BOL_rivers_Chaco_water_bodies, out_feature_class=BOL_rivers_Chaco_water_buffered, buffer_distance_or_field="400 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

    # Process: Buffer PRY Rivers (Buffer) (analysis)
    PRY_rivers_buffered = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\RiversPryORD2_buffer600"
    arcpy.analysis.Buffer(in_features=PRY_rivers, out_feature_class=PRY_rivers_buffered, buffer_distance_or_field="600 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

    # Process: Buffer ARG Rivers (Buffer) (analysis)
    ARG_rivers_buffered = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\perennialArg_Buffer100"
    arcpy.analysis.Buffer(in_features=ARG_rivers, out_feature_class=ARG_rivers_buffered, buffer_distance_or_field="100 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="ALL", dissolve_field=[], method="PLANAR")

    # Process: Merge All Water (Merge) (management)
    water_merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\water_merged"
    arcpy.management.Merge(inputs=[BOL_rivers_Chaco_water_buffered, PRY_rivers_buffered, ARG_rivers_buffered], output=water_merged, field_mappings="Water \"Water\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\WaterPolys_buffer400,Water,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\WaterPolys_buffer400,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\WaterPolys_buffer400,Shape_Area,-1,-1;BUFF_DIST \"BUFF_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\WaterPolys_buffer400,BUFF_DIST,-1,-1;ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Masking_Dem.gdb\\WaterPolys_buffer400,ORIG_FID,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Water Polygon to Raster (Polygon to Raster) (conversion)
    water_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\water_raster"
    arcpy.conversion.PolygonToRaster(in_features=water_merged, value_field="OBJECTID", out_rasterdataset=water_raster, cell_assignment="CELL_CENTER", priority_field="NONE", cellsize="", build_rat="BUILD")

    # Process: Reclassify - Invert Water (Reclassify) (3d)
    water_inverted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\Reclass_water"
    arcpy.ddd.Reclassify(in_raster=water_raster, reclass_field="VALUE", remap="1 NODATA;2 NODATA;3 NODATA;NODATA 1", out_raster=water_inverted, missing_values="DATA")
    water_inverted = arcpy.Raster(water_inverted)

    # Process: NOTwater Raster to Polygon (Raster to Polygon) (conversion)
    NOTwater_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\NOTwater_poly"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=water_inverted, out_polygon_features=NOTwater_polygon, simplify="NO_SIMPLIFY", raster_field="", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Clip - Clean Water (Clip) (analysis)
    dem_roads_water_masked = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWaterMasked_All"
    arcpy.analysis.Clip(in_features=dem_roads_masked, clip_features=NOTwater_polygon, out_feature_class=dem_roads_water_masked, cluster_tolerance="")

    # Process: Reclassify - Isolate Other LC (Reclassify) (3d)
    LC_other = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\MaskingDem_LandCover.gdb\\LC_Other"
    arcpy.ddd.Reclassify(in_raster=Land_Cover_Dataset, reclass_field="Value", remap="1 NODATA;2 NODATA;3 NODATA;4 NODATA;5 1;20 NODATA;21 NODATA;22 NODATA;23 NODATA", out_raster=LC_other, missing_values="DATA")
    LC_other = arcpy.Raster(LC_other)

    # Process: Other LC Raster to Polygon (Raster to Polygon) (conversion)
    LC_other_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\MaskingDem_LandCover.gdb\\LC_Other_polygon"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=LC_other, out_polygon_features=LC_other_polygon, simplify="NO_SIMPLIFY", raster_field="", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Clip Other (Clip) (analysis)
    dem_overlaying_other_LC = "D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\MaskingDem_LandCover.gdb\\Dem_other"
    arcpy.analysis.Clip(in_features=dem_roads_water_masked, clip_features=LC_other_polygon, out_feature_class=dem_overlaying_other_LC, cluster_tolerance="")

    # Process: Pairwise Erase - Clean Other LC (Pairwise Erase) (analysis)
    dem_roads_water_other_masked = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWaterOther_MaskedAll"
    arcpy.analysis.PairwiseErase(in_features=dem_roads_water_masked, erase_features=dem_overlaying_other_LC, out_feature_class=dem_roads_water_other_masked, cluster_tolerance="")

    # Process: Reclassify - Invert Fields (Reclassify) (3d)
    fields_inverted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\Raster_NOTfield"
    arcpy.ddd.Reclassify(in_raster=fields, reclass_field="VALUE", remap="1 NODATA;NODATA 1", out_raster=fields_inverted, missing_values="DATA")
    fields_inverted = arcpy.Raster(fields_inverted)

    # Process: NOTfields Raster to Polygon (Raster to Polygon) (conversion)
    NOTfields_polygon = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\b_Prep_Masks.gdb\\NOTfield_polygon"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=fields_inverted, out_polygon_features=NOTfields_polygon, simplify="NO_SIMPLIFY", raster_field="", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Clip - Clean Fields (Clip) (analysis)
    demarcations_fully_masked = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWaterOtherFields_MaskedAll"
    arcpy.analysis.Clip(in_features=dem_roads_water_other_masked, clip_features=NOTfields_polygon, out_feature_class=demarcations_fully_masked, cluster_tolerance="")

    # Process: Copy Raster (Copy) (management)
    demarcations_fully_masked_copy = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\d_Final_Clean.gdb\\Dem_RoadsWaterOtherFields_MaskedAll_copy"
    arcpy.management.Copy(in_data=demarcations_fully_masked, out_data=demarcations_fully_masked_copy, data_type="", associated_data=[])

    # Process: Trim Line - Removed Dangles (Trim Line) (edit)
    demarcations_trimmed = arcpy.edit.TrimLine(in_features=demarcations_fully_masked_copy, dangle_length="250 Meters", delete_shorts="DELETE_SHORT")[0]

    # Process: Recalculate Feature Class Extent (Recalculate Feature Class Extent) (management)
    updated_demarcations = arcpy.management.RecalculateFeatureClassExtent(in_features=demarcations_trimmed, store_extent=False)[0]

    # Process: Repair Geometry (Repair Geometry) (management)
    repaired_demarcations = arcpy.management.RepairGeometry(in_features=updated_demarcations, delete_null="DELETE_NULL", validation_method="ESRI")[0]

    # Process: Add Field (Add Field) (management)
    Updated_Input_Table = arcpy.management.AddField(in_table=repaired_demarcations, field_name="DEM", field_type="LONG", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

    # Process: Calculate Field (Calculate Field) (management)
    Updated_Input_Table_2_ = arcpy.management.CalculateField(in_table=Updated_Input_Table, field="DEM", expression="1", expression_type="PYTHON3", code_block="", field_type="LONG", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Feature to Raster (Feature to Raster) (conversion)
    DemPrepLT_raster = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\e_Prep_LandTrendrInput.gdb\\DemPrepLT_raster"
    if Updated_Input_Table_2_:
        arcpy.conversion.FeatureToRaster(in_features=repaired_demarcations, field="", out_raster=DemPrepLT_raster, cell_size="D:\\GIS_Chapter1\\Demarcation_analysis\\PrepDemarcations_model\\Model_inputs\\Demarcations_INPUT.gdb\\DemacationsAll_2020")
        DemPrepLT_raster = arcpy.Raster(DemPrepLT_raster)

    # Process: Expand raster (Expand) (sa)
    expanded_DEM = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\e_Prep_LandTrendrInput.gdb\\Expand_DEM2"
    Expand_raster = expanded_DEM
    if Updated_Input_Table_2_:
        expanded_DEM = arcpy.sa.Expand(in_raster=DemPrepLT_raster, number_cells=2, zone_values=[1], expand_method="MORPHOLOGICAL")
        expanded_DEM.save(Expand_raster)


    # Process: Simplify All Lines (Simplify Line) (cartography)
    demarcations_simplified = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\g_Prep_Long.gdb\\dem_simplified"
    point_features_collapsed = arcpy.cartography.SimplifyLine(in_features=repaired_demarcations, out_feature_class=demarcations_simplified, algorithm="POINT_REMOVE", tolerance="30 Meters", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="KEEP_COLLAPSED_POINTS", error_checking_option="CHECK", in_barriers=[])[0]

    # Process: Set Null By Region Area - 1300 (Set Null) (sa)
    nibble_mask_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\nibble_mask1300"
    Set_Null_By_Region_Area_1300 = nibble_mask_large
    nibble_mask_large = arcpy.sa.SetNull(in_conditional_raster=demarcations_grouped, in_false_raster_or_constant=Input_False_Constant_2_, where_clause="COUNT < 1300")
    nibble_mask_large.save(Set_Null_By_Region_Area_1300)


    # Process: Nibble Medium (Nibble) (sa)
    medium_removed = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\Nibble_output1300"
    Nibble_Medium = medium_removed
    medium_removed = arcpy.sa.Nibble(in_raster=Demarcations, in_mask_raster=nibble_mask_large, nibble_values="DATA_ONLY", nibble_nodata="PRESERVE_NODATA", in_zone_raster="")
    medium_removed.save(Nibble_Medium)


    # Process: Reclassify Demarcations - Large (Reclassify) (sa)
    demarcations_reclassified_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\Dem_reclassLARGE"
    Reclassify_Demarcations_Large = demarcations_reclassified_large
    demarcations_reclassified_large = arcpy.sa.Reclassify(in_raster=medium_removed, reclass_field="VALUE", remap="0 NODATA;1 1;2 1", missing_values="DATA")
    demarcations_reclassified_large.save(Reclassify_Demarcations_Large)


    # Process: Demarcation Raster to Polygon - Large (Raster to Polygon) (conversion)
    demarcation_polygon_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\Dem_polygonLARGE"
    with arcpy.EnvManager(outputMFlag="Disabled", outputZFlag="Disabled"):
        arcpy.conversion.RasterToPolygon(in_raster=demarcations_reclassified_large, out_polygon_features=demarcation_polygon_large, simplify="NO_SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature=None)

    # Process: Polygon To Centerline - Large (Polygon To Centerline) (topographic)
    demarcation_centreline_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\a_Filter_Demarcations.gdb\\dem_centreline_large"
    arcpy.topographic.PolygonToCenterline(in_features=demarcation_polygon_large, out_feature_class=demarcation_centreline_large, connecting_features=[])

    # Process: Clip - Clean Roads (2) (Clip) (analysis)
    dem_roads_masked_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsMasked_Large"
    arcpy.analysis.Clip(in_features=demarcation_centreline_large, clip_features=NOTroad_polygon, out_feature_class=dem_roads_masked_large, cluster_tolerance="")

    # Process: Clip - Clean Water (2) (Clip) (analysis)
    dem_roads_water_masked_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWater_MaskedLarge"
    arcpy.analysis.Clip(in_features=dem_roads_masked_large, clip_features=NOTwater_polygon, out_feature_class=dem_roads_water_masked_large, cluster_tolerance="")

    # Process: Pairwise Erase - Clean Other LC (2) (Pairwise Erase) (analysis)
    dem_roads_water_other_masked_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWaterOther_MaskedLarge"
    arcpy.analysis.PairwiseErase(in_features=dem_roads_water_masked_large, erase_features=dem_overlaying_other_LC, out_feature_class=dem_roads_water_other_masked_large, cluster_tolerance="")

    # Process: Clip - Clean Fields (2) (Clip) (analysis)
    demarcations_fully_masked_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\c_Mask_Demarcations.gdb\\Dem_RoadsWaterOtherFields_MaskedLarge"
    arcpy.analysis.Clip(in_features=dem_roads_water_other_masked_large, clip_features=NOTfields_polygon, out_feature_class=demarcations_fully_masked_large, cluster_tolerance="")

    # Process: Copy Raster (2) (Copy) (management)
    demarcations_fully_masked_large_copy = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\d_Final_Clean.gdb\\Dem_RoadsWaterOtherFields_MaskedLarge_copy"
    arcpy.management.Copy(in_data=demarcations_fully_masked_large, out_data=demarcations_fully_masked_large_copy, data_type="", associated_data=[])

    # Process: Trim Line - Removed Dangles (2) (Trim Line) (edit)
    demarcations_large_trimmed = arcpy.edit.TrimLine(in_features=demarcations_fully_masked_large_copy, dangle_length="250 Meters", delete_shorts="DELETE_SHORT")[0]

    # Process: Recalculate Feature Class Extent (2) (Recalculate Feature Class Extent) (management)
    updated_demarcations_large = arcpy.management.RecalculateFeatureClassExtent(in_features=demarcations_large_trimmed, store_extent=False)[0]

    # Process: Repair Geometry (2) (Repair Geometry) (management)
    repaired_demarcations_large = arcpy.management.RepairGeometry(in_features=updated_demarcations_large, delete_null="DELETE_NULL", validation_method="ESRI")[0]

    # Process: Simplify Large Lines (Simplify Line) (cartography)
    demarcations_simplified_large = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\f_Prep_Large.gdb\\dem_simplified_large"
    point_features_collapsed_2_ = arcpy.cartography.SimplifyLine(in_features=repaired_demarcations_large, out_feature_class=demarcations_simplified_large, algorithm="POINT_REMOVE", tolerance="30 Meters", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="KEEP_COLLAPSED_POINTS", error_checking_option="CHECK", in_barriers=[])[0]

    # Process: Split Line At Vertices (Split Line At Vertices) (management)
    demarcations_split = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\g_Prep_Long.gdb\\dem_split"
    arcpy.management.SplitLine(in_features=demarcations_simplified, out_feature_class=demarcations_split)

    # Process: Copy (3) (Copy) (management)
    all_demarcations = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD"
    arcpy.management.Copy(in_data=demarcations_split, out_data=all_demarcations, data_type="", associated_data=[])

    # Process: Reclassify zero to NODATA (Reclassify) (3d)
    Reclass_change = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\MOSAIC_TCW_yod_reclass"
    arcpy.ddd.Reclassify(in_raster=LandTrendr_Output, reclass_field="Value", remap="0 NODATA;1985 1985;1986 1986;1987 1987;1988 1988;1989 1989;1990 1990;1991 1991;1992 1992;1993 1993;1994 1994;1995 1995;1996 1996;1997 1997;1998 1998;1999 1999;2000 2000;2001 2001;2002 2002;2003 2003;2004 2004;2005 2005;2006 2006;2007 2007;2008 2008;2009 2009;2010 2010;2011 2011;2012 2012;2013 2013;2014 2014;2015 2015;2016 2016;2017 2017;2018 2018;2019 2019;2020 2020;2021 2021;2022 2022", out_raster=Reclass_change, missing_values="NODATA")
    Reclass_change = arcpy.Raster(Reclass_change)

    # Process: Add Surface Information (Add Surface Information) (3d)
    demarcations_with_min_YOD = arcpy.ddd.AddSurfaceInformation(in_feature_class=all_demarcations, in_surface=Reclass_change, out_property=["Z_MIN", "Z_MAX", "Z_MEAN"], method="BILINEAR", sample_distance=60, z_factor=1, pyramid_level_resolution=0, noise_filtering="")[0]

    # Process: Round (Calculate Field) (management)
    rounded = arcpy.management.CalculateField(in_table=demarcations_with_min_YOD, field="Z_Min", expression="round(!Z_Min!)", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Copy (2) (Copy) (management)
    demarcations_split_all_copy = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\g_Prep_Long.gdb\\dem_YOD"
    arcpy.management.Copy(in_data=demarcations_split, out_data=demarcations_split_all_copy, data_type="", associated_data=[])

    # Process: Remove Short Lines (1000) (Remove Small Lines) (topographic)
    demarcations_long = arcpy.topographic.RemoveSmallLines(in_features=demarcations_split_all_copy, minimum_length="1000 Meters", maximum_angle=25, in_intersecting_features=[], recursive="RECURSIVE", split_input_lines="NO_SPLIT")[0]

    # Process: Merge Long and Large (Merge) (management)
    long_and_large_merged = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\h_Prep_PrimaryDem.gdb\\longLarge_merged"
    arcpy.management.Merge(inputs=[demarcations_long, demarcations_simplified_large], output=long_and_large_merged, field_mappings="ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Dem_YOD.gdb\\dem_YOD,ORIG_FID,-1,-1;ORIG_SEQ \"ORIG_SEQ\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Analysis\\Dem_YOD.gdb\\dem_YOD,ORIG_SEQ,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Add Code Field (Add Field) (management)
    long_and_large_merged_code_added = arcpy.management.AddField(in_table=long_and_large_merged, field_name="DEM_CODE", field_type="SHORT", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

    # Process: Calculate Code (Calculate Field) (management)
    primary_demarcations = arcpy.management.CalculateField(in_table=long_and_large_merged_code_added, field="DEM_CODE", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Spatial Join Large (Spatial Join) (analysis)
    joined_with_primary = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\j_Finalize.gdb\\dem_YOD_final"
    arcpy.analysis.SpatialJoin(target_features=rounded, join_features=primary_demarcations, out_feature_class=joined_with_primary, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD,ORIG_FID,-1,-1;ORIG_SEQ \"ORIG_SEQ\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD,ORIG_SEQ,-1,-1;Z_Min \"Z_Min\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD,Z_Min,-1,-1;Z_Max \"Z_Max\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD,Z_Max,-1,-1;Z_Mean \"Z_Mean\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\i_Add_YOD.gdb\\dem_YOD,Z_Mean,-1,-1;ORIG_FID \"ORIG_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\h_Prep_PrimaryDem.gdb\\longLarge_merged,ORIG_FID,-1,-1;ORIG_SEQ \"ORIG_SEQ\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\h_Prep_PrimaryDem.gdb\\longLarge_merged,ORIG_SEQ,-1,-1;DEM_CODE \"DEM_CODE\" true true false 0 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Model_intermediaries\\h_Prep_PrimaryDem.gdb\\longLarge_merged,DEM_CODE,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Delete Field (Delete Field) (management)
    almost_final = arcpy.management.DeleteField(in_table=joined_with_primary, drop_field=["Join_Count", "TARGET_FID", "ORIG_SEQ"], method="DELETE_FIELDS")[0]

    # Process: Final code (Calculate Field) (management)
    DEMCARCATIONS_FINAL = arcpy.management.CalculateField(in_table=almost_final, field="DEM_CODE", expression="changenull(!DEM_CODE!)", expression_type="PYTHON3", code_block="""def changenull(x):
    if x == None:
        return 2
    else:
        return 1""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Copy (Copy) (management)
    dem_YOD1985_fina_copied = "D:\\GIS_Chapter1\\Demarcation_analysis\\PrepDemarcations.gdb\\dem_YOD1985_finalcopy"
    arcpy.management.Copy(in_data=DEMCARCATIONS_FINAL, out_data=dem_YOD1985_fina_copied, data_type="", associated_data=[])

    # Process: Alter Field (Alter Field) (management)
    Min1995_renamed = arcpy.management.AlterField(in_table=Dem_yod1995_final, field="Z_Min", new_field_name="Z_Min1995", new_field_alias="Z_Min1995", field_type="LONG", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (Join Field) (management)
    _85_and_95_joined = arcpy.management.JoinField(in_data=dem_YOD1985_fina_copied, in_field="OBJECTID", join_table=Min1995_renamed, join_field="OBJECTID", fields=["Z_Min1995"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Calculate Field (2) (Calculate Field) (management)
    dem_YOD1985_final_4_ = arcpy.management.CalculateField(in_table=_85_and_95_joined, field="Z_Mean", expression="changeMAX(!Z_Mean!, !Z_Mean!, !Z_Min1995!)", expression_type="PYTHON3", code_block="""def changeMAX(x, mean, min1995):
    if x < 1986:
        return min1995
    else:
        return mean""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Round (2) (Calculate Field) (management)
    rounded_2_ = arcpy.management.CalculateField(in_table=dem_YOD1985_final_4_, field="Z_Max", expression="round(!Z_Max!)", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Round (3) (Calculate Field) (management)
    rounded_3_ = arcpy.management.CalculateField(in_table=rounded_2_, field="Z_Mean", expression="round(!Z_Mean!)", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Buffer (Buffer) (analysis)
    dem_test_Buffer100 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_Buffer100"
    arcpy.analysis.Buffer(in_features=dem_YOD1985_finalProj, out_feature_class=dem_test_Buffer100, buffer_distance_or_field="100 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Dissolve (Dissolve) (management)
    dem_test_Buffer100_Dissolve = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_Buffer100_Dissolve"
    arcpy.management.Dissolve(in_features=dem_test_Buffer100, out_feature_class=dem_test_Buffer100_Dissolve, dissolve_field=[], statistics_fields=[], multi_part="SINGLE_PART", unsplit_lines="DISSOLVE_LINES", concatenation_separator="")

    # Process: Add Field (2) (Add Field) (management)
    dem_test_Buffer100_Dissolve_2_ = arcpy.management.AddField(in_table=dem_test_Buffer100_Dissolve, field_name="ID", field_type="LONG", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

    # Process: Calculate Field (3) (Calculate Field) (management)
    dem_test_Buffer100_Dissolve_3_ = arcpy.management.CalculateField(in_table=dem_test_Buffer100_Dissolve_2_, field="ID", expression="!OBJECTID!", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Spatial Join (Spatial Join) (analysis)
    dem_test_SpatialJoin = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_SpatialJoin"
    arcpy.analysis.SpatialJoin(target_features=dem_YOD1985_finalProj, join_features=dem_test_Buffer100_Dissolve_3_, out_feature_class=dem_test_SpatialJoin, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="FID \"FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,FID,-1,-1;DEM \"DEM\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,DEM,-1,-1;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,ORIG_FID,-1,-1;Z_Min \"Z_Min\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,Z_Min,-1,-1;Z_Max \"Z_Max\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,Z_Max,-1,-1;Z_Mean \"Z_Mean\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,Z_Mean,-1,-1;DEM_CODE \"DEM_CODE\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,DEM_CODE,-1,-1;Z_Min1995 \"Z_Min1995\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,Z_Min1995,-1,-1;SHAPE_Length \"SHAPE_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_finalProj,SHAPE_Length,-1,-1;ID \"ID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_Buffer100_Dissolve,ID,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Dissolve (2) (Dissolve) (management)
    dem_test_Unsplit = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_Unsplit"
    arcpy.management.Dissolve(in_features=dem_test_SpatialJoin, out_feature_class=dem_test_Unsplit, dissolve_field=["ID"], statistics_fields=[["DEM", "SUM"]], multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES", concatenation_separator="")

    # Process: Copy (4) (Copy) (management)
    dem_test_Unsplit_copy = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_Unsplit_copy"
    arcpy.management.Copy(in_data=dem_test_Unsplit, out_data=dem_test_Unsplit_copy, data_type="FeatureClass", associated_data=[])

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    dem_test_Unsplit_Layer, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=dem_test_Unsplit, selection_type="NEW_SELECTION", where_clause="SHAPE_Length < 1200", invert_where_clause="")

    # Process: Delete Features (Delete Features) (management)
    if dem_test_Unsplit_Layer:
        dem_test_Unsplit_4_ = arcpy.management.DeleteFeatures(in_features=dem_test_Unsplit)[0]

    # Process: Select Layer By Location (Select Layer By Location) (management)
    if dem_test_Unsplit_Layer:
        dem_test_2_, Output_Layer_Names, Count_2_ = arcpy.management.SelectLayerByLocation(in_layer=[dem_YOD1985_finalProj], overlap_type="INTERSECT", select_features=dem_test_Unsplit_4_, search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

    # Process: Export Features (Export Features) (conversion)
    dem_test_filtered = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_test_filtered"
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        arcpy.conversion.ExportFeatures(in_features=dem_test_2_, out_features=dem_test_filtered, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="FID \"FID\" true true false 4 Long 0 0,First,#,dem_YOD1985_finalProj_Layer,FID,-1,-1;DEM \"DEM\" true true false 4 Long 0 0,First,#,dem_YOD1985_finalProj_Layer,DEM,-1,-1;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,dem_YOD1985_finalProj_Layer,ORIG_FID,-1,-1;Z_Min \"Z_Min\" true true false 8 Double 0 0,First,#,dem_YOD1985_finalProj_Layer,Z_Min,-1,-1;Z_Max \"Z_Max\" true true false 8 Double 0 0,First,#,dem_YOD1985_finalProj_Layer,Z_Max,-1,-1;Z_Mean \"Z_Mean\" true true false 8 Double 0 0,First,#,dem_YOD1985_finalProj_Layer,Z_Mean,-1,-1;DEM_CODE \"DEM_CODE\" true true false 2 Short 0 0,First,#,dem_YOD1985_finalProj_Layer,DEM_CODE,-1,-1;Z_Min1995 \"Z_Min1995\" true true false 8 Double 0 0,First,#,dem_YOD1985_finalProj_Layer,Z_Min1995,-1,-1;SHAPE_Length \"SHAPE_Length\" false true true 8 Double 0 0,First,#,dem_YOD1985_finalProj_Layer,SHAPE_Length,-1,-1", sort_field=[])

    # Process: Calculate Field (4) (Calculate Field) (management)
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        dem_test_filtered_2_ = arcpy.management.CalculateField(in_table=dem_test_filtered, field="Z_Mean", expression="calc(!Z_Mean!)", expression_type="PYTHON3", code_block="""def calc(X1): 
    if X1 >= 2020:
        return 2020
    else:
        return X1""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Field (5) (Calculate Field) (management)
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        dem_test_filtered_3_ = arcpy.management.CalculateField(in_table=dem_test_filtered_2_, field="Z_Min", expression="calc(!Z_Min!)", expression_type="PYTHON3", code_block="""def calc(X1): 
    if X1 >= 2020:
        return 2020
    else:
        return X1""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate Field (6) (Calculate Field) (management)
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        dem_test_filtered_4_ = arcpy.management.CalculateField(in_table=dem_test_filtered_3_, field="Z_Max", expression="calc(!Z_Max!)", expression_type="PYTHON3", code_block="""def calc(X1): 
    if X1 >= 2020:
        return 2020
    else:
        return X1""", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Delete Field (2) (Delete Field) (management)
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        dem_test_filtered_5_ = arcpy.management.DeleteField(in_table=dem_test_filtered_4_, drop_field=["Z_Min1995"], method="DELETE_FIELDS")[0]

    # Process: Copy (5) (Copy) (management)
    dem_YOD1985_FILTERED = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\DemCleaning\\Dem_CLEANED.gdb\\dem_YOD1985_FILTERED"
    if Output_Layer_Names and dem_test_Unsplit_Layer:
        arcpy.management.Copy(in_data=dem_test_filtered_5_, out_data=dem_YOD1985_FILTERED, data_type="", associated_data=[])

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\DemCleaning\Dem_CLEANTest.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\DemCleaning\Dem_CLEANTest.gdb"):
        PrepDemModel()
