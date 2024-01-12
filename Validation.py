"""
-*- Code used to produce the demarcation reference dataset for validation -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3
2024-01-12 10:40:23

"""
import arcpy

def Validation():  # Validation

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\GeoAnalytics Desktop Tools.tbx")
    Hex_Grid_10km2 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks.gdb\\HexGrid_10km2_masked"
    Fields = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Masks.gdb\\Fields_Polygon_Chaco"
    LC_Other = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Masks.gdb\\LC_Other_polygon_Chaco"
    Blocks_gdb = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks.gdb"
    S2_image_2 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_2020_S2\\DemAnalysis_ValidationS2\\S2collection_median-0000018944-0000018944.tif")
    hexgrid_SELECTION = "HexGrid10km2__100RandomSelect"
    S2_image_1 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_2020_S2\\DemAnalysis_ValidationS2\\S2collection_median-0000000000-0000037888.tif")
    S2C_mosaics = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_2020_S2\\S2C_mosaics.gdb"
    LS_image_1 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_86_2020_L57\\DemAnalysis_ValidationL57\\DemAnalysis_ValidationL57\\Landsatcomposite0007-0000000000-0000000000.tif")
    LS_image_2 = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_86_2020_L57\\DemAnalysis_ValidationL57\\DemAnalysis_ValidationL57\\Landsatcomposite0007-0000000000-0000000000.tif")
    LC_mosaics = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_86_2020_L57\\LC_mosaics.gdb"
    demarcation_manual_reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Dem_Validation.gdb\\Demarcations_ManualRef"

    # Process: Select Layer By Attribute (Select Layer By Attribute) (management)
    select_all_polygons, Count = arcpy.management.SelectLayerByAttribute(in_layer_or_view=Hex_Grid_10km2, selection_type="NEW_SELECTION", where_clause="Shape_Area IS NOT NULL", invert_where_clause="")

    # Process: Merge (Merge) (management)
    mask = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Masks.gdb\\Masks_merged"
    arcpy.management.Merge(inputs=[Fields, LC_Other], output=mask, field_mappings="Id \"Id\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,Id,-1,-1;gridcode \"gridcode\" true true false 4 Long 0 0,First,#,Fields_Polygon_Chaco,gridcode,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,Fields_Polygon_Chaco,Shape_Area,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Select Layer By Location (Select Layer By Location) (management)
    centroids_not_in_mask, output_layer_name, Count_2_ = arcpy.management.SelectLayerByLocation(in_layer=[select_all_polygons], overlap_type="HAVE_THEIR_CENTER_IN", select_features=mask, search_distance="", selection_type="REMOVE_FROM_SELECTION", invert_spatial_relationship="NOT_INVERT")

    # Process: Export Features (Export Features) (conversion)
    masked_hexagons = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks.gdb\\HexGrid_10km2__MASKED"
    arcpy.conversion.ExportFeatures(in_features=centroids_not_in_mask, out_features=masked_hexagons, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,HexGrid_10km2_masked_Layer,GRID_ID,0,12;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,HexGrid_10km2_masked_Layer,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,HexGrid_10km2_masked_Layer,Shape_Area,-1,-1", sort_field=[])

    # Process: Add Field (Add Field) (management)
    create_mask_label = arcpy.management.AddField(in_table=masked_hexagons, field_name="Merge", field_type="LONG", field_precision=None, field_scale=None, field_length=None, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")[0]

    # Process: Calculate Field (Calculate Field) (management)
    assign_labels = arcpy.management.CalculateField(in_table=create_mask_label, field="Merge", expression="1", expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Dissolve (Dissolve) (management)
    dissolve_masked_hexagons = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks.gdb\\MASKED_Dissolved"
    arcpy.management.Dissolve(in_features=assign_labels, out_feature_class=dissolve_masked_hexagons, dissolve_field=["Merge"], statistics_fields=[], multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES", concatenation_separator="")

    # Process: Create Random Points (Create Random Points) (management)
    random_points = arcpy.management.CreateRandomPoints(out_path=Blocks_gdb, out_name="RandomPoints", constraining_feature_class=dissolve_masked_hexagons, constraining_extent="0 0 250 250", number_of_points_or_field=100, minimum_allowed_distance="25 Kilometers", create_multipoint_output="POINT", multipoint_size=0)[0]

    # Process: Ranomly Select 100 Hexagons (Select Layer By Location) (management)
    hex_grid_SELECTION, output_layer_names, Count_3_ = arcpy.management.SelectLayerByLocation(in_layer=[assign_labels], overlap_type="INTERSECT", select_features=random_points, search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")

    # Process: Clip Raster (4) (Clip Raster) (management)
    clip_S2_image_2 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_2020_S2\\S2C_clipped.gdb\\S2collection_median_Clip"
    arcpy.management.Clip(in_raster=S2_image_2, rectangle="4144801.25754005 -4376285.57864499 6032860.36810455 -2784472.74056485", out_raster=clip_S2_image_2, in_template_dataset=hexgrid_SELECTION, nodata_value="3.4e+38", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    clip_S2_image_2 = arcpy.Raster(clip_S2_image_2)

    # Process: Clip Raster (3) (Clip Raster) (management)
    clip_S2_image_1 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_2020_S2\\S2C_clipped.gdb\\S2collection_median_Clip"
    arcpy.management.Clip(in_raster=S2_image_1, rectangle="4144801.25754005 -4376285.57864499 6032860.36810455 -2784472.74056485", out_raster=clip_S2_image_1, in_template_dataset=hexgrid_SELECTION, nodata_value="3.4e+38", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    clip_S2_image_1 = arcpy.Raster(clip_S2_image_1)

    # Process: Mosaic To New Raster (Mosaic To New Raster) (management)
    S2C_2020_Mosaic = arcpy.management.MosaicToNewRaster(input_rasters=[clip_S2_image_2, clip_S2_image_1], output_location=S2C_mosaics, raster_dataset_name_with_extension="S2C_clip", coordinate_system_for_the_raster="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", pixel_type="32_BIT_UNSIGNED", cellsize=None, number_of_bands=3, mosaic_method="MEAN", mosaic_colormap_mode="FIRST")[0]
    S2C_2020_Mosaic = arcpy.Raster(S2C_2020_Mosaic)

    # Process: Clip Raster (2) (Clip Raster) (management)
    clip_LS_image_1 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_86_2020_L57\\LC_clipped.gdb\\Clip_Landsatcomposite0007"
    arcpy.management.Clip(in_raster=LS_image_1, rectangle="4144801.25754005 -4376285.57864499 6032860.36810455 -2784472.74056485", out_raster=clip_LS_image_1, in_template_dataset=hexgrid_SELECTION, nodata_value="1.79e+308", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    clip_LS_image_1 = arcpy.Raster(clip_LS_image_1)

    # Process: Clip Raster (1) (Clip Raster) (management)
    clip_LS_image_2 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Blocks_Imagery\\Blocks_86_2020_L57\\LC_clipped.gdb\\Clip_Landsatcomposite0007"
    arcpy.management.Clip(in_raster=LS_image_2, rectangle="4144801.25754005 -4376285.57864499 6032860.36810455 -2784472.74056485", out_raster=clip_LS_image_2, in_template_dataset=hexgrid_SELECTION, nodata_value="1.79e+308", clipping_geometry="ClippingGeometry", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    clip_LS_image_2 = arcpy.Raster(clip_LS_image_2)

    # Process: Mosaic To New Raster (2) (Mosaic To New Raster) (management)
    LC_Period_1_mosaic = arcpy.management.MosaicToNewRaster(input_rasters=[clip_LS_image_1, clip_LS_image_2], output_location=LC_mosaics, raster_dataset_name_with_extension="LC8694_mosaic", coordinate_system_for_the_raster="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", pixel_type="64_BIT", cellsize=None, number_of_bands=4, mosaic_method="MEAN", mosaic_colormap_mode="FIRST")[0]
    LC_Period_1_mosaic = arcpy.Raster(LC_Period_1_mosaic)

    # Process: Clip Layer (Clip Layer) (gapro)
    clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Dem_Validation.gdb\\Demarcations_ManualRef_Clip"
    arcpy.gapro.ClipLayer(input_layer=demarcation_manual_reference, clip_layer=hexgrid_SELECTION, out_feature_class=clipped)

    # Process: Split Line At Vertices (Split Line At Vertices) (management)
    demarcations_manual_reference_coded = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Dem_Validation.gdb\\Demarcations_ManualRef_Coding"
    arcpy.management.SplitLine(in_features=clipped, out_feature_class=demarcations_manual_reference_coded)

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LinearCorrespondence.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LinearCorrespondence.gdb"):
        Validation()
