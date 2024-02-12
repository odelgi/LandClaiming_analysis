"""
-*- Code used to calculate the linear correspondence between the extracted and reference demarcations -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""
import arcpy

def LCA2():  # LinearCorrespondenceUPDATE

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\GeoAnalytics Desktop Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")
    Demarcations_extracted_automatically = "dem_YOD1985_FILTERED1500"
    HexGrid_random_selection = "HexGrid10km2__100RandomSelect"
    Sub_Regions = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\MergeSubRegions"
    Gran_Chaco = "GranChaco"
    Demarcations_manual_reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Dem_Validation.gdb\\DemManualRef_Project"

    # Process: Clip Layer (Clip Layer) (gapro)
    dem1500Extracted_clipHex = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500Extracted_clipHex"
    arcpy.gapro.ClipLayer(input_layer=Demarcations_extracted_automatically, clip_layer=HexGrid_random_selection, out_feature_class=dem1500Extracted_clipHex)

    # Process: Spatial Join (3) (Spatial Join) (analysis)
    dem1500_extract = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract"
    arcpy.analysis.SpatialJoin(target_features=dem1500Extracted_clipHex, join_features=Sub_Regions, out_feature_class=dem1500_extract, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Spatial Join (4) (Spatial Join) (analysis)
    extracted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500extract_REGIONS"
    arcpy.analysis.SpatialJoin(target_features=dem1500_extract, join_features=Gran_Chaco, out_feature_class=extracted, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="Join_Count \"Join_Count\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,TARGET_FID,-1,-1;OBJECTID \"OBJECTID\" true false false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,OBJECTID,-1,-1;FID \"FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,FID,-1,-1;DEM \"DEM\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,DEM,-1,-1;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,ORIG_FID,-1,-1;Z_Min \"Z_Min\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,Z_Min,-1,-1;Z_Max \"Z_Max\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,Z_Max,-1,-1;Z_Mean \"Z_Mean\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,Z_Mean,-1,-1;DEM_CODE \"DEM_CODE\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,DEM_CODE,-1,-1;Z_Min1995 \"Z_Min1995\" true true false 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,Z_Min1995,-1,-1;iso3 \"iso3\" true true false 254 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\dem1500_extract,iso3,0,254;OBJECTID_1 \"OBJECTID\" true true false 4 Long 0 0,First,#,GranChaco,OBJECTID,-1,-1;AREA \"AREA\" true true false 8 Double 0 0,First,#,GranChaco,AREA,-1,-1;PERIMETER \"PERIMETER\" true true false 8 Double 0 0,First,#,GranChaco,PERIMETER,-1,-1;Name \"ECO_NAME\" true true false 99 Text 0 0,First,#,GranChaco,Name,0,99;REALM \"REALM\" true true false 3 Text 0 0,First,#,GranChaco,REALM,0,3;BIOME \"BIOME\" true true false 8 Double 0 0,First,#,GranChaco,BIOME,-1,-1;ECO_NUM \"ECO_NUM\" true true false 8 Double 0 0,First,#,GranChaco,ECO_NUM,-1,-1;ECO_ID \"ECO_ID\" true true false 8 Double 0 0,First,#,GranChaco,ECO_ID,-1,-1;ECO_SYM \"ECO_SYM\" true true false 8 Double 0 0,First,#,GranChaco,ECO_SYM,-1,-1;GBL_STAT \"GBL_STAT\" true true false 8 Double 0 0,First,#,GranChaco,GBL_STAT,-1,-1;G200_REGIO \"G200_REGIO\" true true false 99 Text 0 0,First,#,GranChaco,G200_REGIO,0,99;G200_NUM \"G200_NUM\" true true false 8 Double 0 0,First,#,GranChaco,G200_NUM,-1,-1;G200_BIOME \"G200_BIOME\" true true false 8 Double 0 0,First,#,GranChaco,G200_BIOME,-1,-1;G200_STAT \"G200_STAT\" true true false 8 Double 0 0,First,#,GranChaco,G200_STAT,-1,-1;Shape_Leng \"Shape_Leng\" true true false 8 Double 0 0,First,#,GranChaco,Shape_Leng,-1,-1;area_km2 \"area_km2\" true true false 4 Long 0 0,First,#,GranChaco,area_km2,-1,-1;eco_code \"eco_code\" true true false 50 Text 0 0,First,#,GranChaco,eco_code,0,50;PER_area \"PER_area\" true true false 8 Double 0 0,First,#,GranChaco,PER_area,-1,-1;PER_area_1 \"PER_area_1\" true true false 8 Double 0 0,First,#,GranChaco,PER_area_1,-1,-1;PER_area_2 \"PER_area_2\" true true false 8 Double 0 0,First,#,GranChaco,PER_area_2,-1,-1;Chaco \"Chaco\" true true false 2 Short 0 0,First,#,GranChaco,Chaco,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,GranChaco,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,GranChaco,Shape_Area,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Summary Statistics (3) (Summary Statistics) (analysis)
    demEXTRACT_LCAstats = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\demEXTRACT_LCAstats"
    arcpy.analysis.Statistics(in_table=extracted, out_table=demEXTRACT_LCAstats, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["iso3", "Name"], concatenation_separator="")

    # Process: Table To Excel (Table To Excel) (conversion)
    demEXTRACT1500_LCAstats_xlsx = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\demEXTRACT1500_LCAstats.xlsx"
    arcpy.conversion.TableToExcel(Input_Table=[demEXTRACT_LCAstats], Output_Excel_File=demEXTRACT1500_LCAstats_xlsx, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Spatial Join (Spatial Join) (analysis)
    DemManualRef_Pro_SpatialJoin = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin"
    arcpy.analysis.SpatialJoin(target_features=Demarcations_manual_reference, join_features=Sub_Regions, out_feature_class=DemManualRef_Pro_SpatialJoin, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Spatial Join (2) (Spatial Join) (analysis)
    DemManualRef_REGIONS = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_REGIONS"
    arcpy.analysis.SpatialJoin(target_features=DemManualRef_Pro_SpatialJoin, join_features=Gran_Chaco, out_feature_class=DemManualRef_REGIONS, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="Join_Count \"Join_Count\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,TARGET_FID,-1,-1;OBJECTID \"OBJECTID\" true false false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,OBJECTID,-1,-1;DemSure \"Sure\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,DemSure,-1,-1;PerUnsure \"Unsure\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,PerUnsure,-1,-1;PeriodDetected \"PeriodDetected\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,PeriodDetected,-1,-1;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,ORIG_FID,-1,-1;ORIG_SEQ \"ORIG_SEQ\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,ORIG_SEQ,-1,-1;SHAPE_Length \"SHAPE_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,SHAPE_Length,-1,-1;iso3 \"iso3\" true true false 254 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,iso3,0,254;Shape_Length_1 \"Shape_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,Shape_Length_1,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\DemManualRef_Pro_SpatialJoin,Shape_Area,-1,-1;OBJECTID_1 \"OBJECTID\" true true false 4 Long 0 0,First,#,GranChaco,OBJECTID,-1,-1;AREA \"AREA\" true true false 8 Double 0 0,First,#,GranChaco,AREA,-1,-1;PERIMETER \"PERIMETER\" true true false 8 Double 0 0,First,#,GranChaco,PERIMETER,-1,-1;Name \"ECO_NAME\" true true false 99 Text 0 0,First,#,GranChaco,Name,0,99;REALM \"REALM\" true true false 3 Text 0 0,First,#,GranChaco,REALM,0,3;BIOME \"BIOME\" true true false 8 Double 0 0,First,#,GranChaco,BIOME,-1,-1;ECO_NUM \"ECO_NUM\" true true false 8 Double 0 0,First,#,GranChaco,ECO_NUM,-1,-1;ECO_ID \"ECO_ID\" true true false 8 Double 0 0,First,#,GranChaco,ECO_ID,-1,-1;ECO_SYM \"ECO_SYM\" true true false 8 Double 0 0,First,#,GranChaco,ECO_SYM,-1,-1;GBL_STAT \"GBL_STAT\" true true false 8 Double 0 0,First,#,GranChaco,GBL_STAT,-1,-1;G200_REGIO \"G200_REGIO\" true true false 99 Text 0 0,First,#,GranChaco,G200_REGIO,0,99;G200_NUM \"G200_NUM\" true true false 8 Double 0 0,First,#,GranChaco,G200_NUM,-1,-1;G200_BIOME \"G200_BIOME\" true true false 8 Double 0 0,First,#,GranChaco,G200_BIOME,-1,-1;G200_STAT \"G200_STAT\" true true false 8 Double 0 0,First,#,GranChaco,G200_STAT,-1,-1;Shape_Leng \"Shape_Leng\" true true false 8 Double 0 0,First,#,GranChaco,Shape_Leng,-1,-1;area_km2 \"area_km2\" true true false 4 Long 0 0,First,#,GranChaco,area_km2,-1,-1;eco_code \"eco_code\" true true false 50 Text 0 0,First,#,GranChaco,eco_code,0,50;PER_area \"PER_area\" true true false 8 Double 0 0,First,#,GranChaco,PER_area,-1,-1;PER_area_1 \"PER_area_1\" true true false 8 Double 0 0,First,#,GranChaco,PER_area_1,-1,-1;PER_area_2 \"PER_area_2\" true true false 8 Double 0 0,First,#,GranChaco,PER_area_2,-1,-1;Chaco \"Chaco\" true true false 2 Short 0 0,First,#,GranChaco,Chaco,-1,-1;Shape_Length_12 \"Shape_Length\" false true true 8 Double 0 0,First,#,GranChaco,Shape_Length,-1,-1;Shape_Area_1 \"Shape_Area\" false true true 8 Double 0 0,First,#,GranChaco,Shape_Area,-1,-1", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Buffer (Buffer) (analysis)
    buffered_reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\DemsManualRef_Buffer"
    arcpy.analysis.Buffer(in_features=DemManualRef_REGIONS, out_feature_class=buffered_reference, buffer_distance_or_field="25 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Pairwise Intersect (Pairwise Intersect) (analysis)
    matched = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matched"
    arcpy.analysis.PairwiseIntersect(in_features=[buffered_reference, extracted], out_feature_class=matched, join_attributes="ALL", cluster_tolerance="", output_type="LINE")

    # Process: Summary Statistics (Summary Statistics) (analysis)
    demMATCHED_LCAstats = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\demMATCHED_LCAstats"
    arcpy.analysis.Statistics(in_table=matched, out_table=demMATCHED_LCAstats, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["iso3", "Name", "DemSure"], concatenation_separator="")

    # Process: Table To Excel (2) (Table To Excel) (conversion)
    demMATCHED1500_LCAstats_xlsx = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\demMATCHED1500_LCAstats.xlsx"
    arcpy.conversion.TableToExcel(Input_Table=[demMATCHED_LCAstats], Output_Excel_File=demMATCHED1500_LCAstats_xlsx, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Copy (2) (Copy) (management)
    reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\reference"
    arcpy.management.Copy(in_data=DemManualRef_REGIONS, out_data=reference, data_type="", associated_data=[])

    # Process: Summary Statistics (2) (Summary Statistics) (analysis)
    demREFERENCE_LCAstats = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LCA1500.gdb\\demREFERENCE_LCAstats"
    arcpy.analysis.Statistics(in_table=reference, out_table=demREFERENCE_LCAstats, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["iso3", "Name", "DemSure"], concatenation_separator="")

    # Process: Table To Excel (3) (Table To Excel) (conversion)
    demREFERENCE1500_LCAstats_xlsx = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\demREFERENCE1500_LCAstats.xlsx"
    arcpy.conversion.TableToExcel(Input_Table=[demREFERENCE_LCAstats], Output_Excel_File=demREFERENCE1500_LCAstats_xlsx, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LCA1500.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LCA1500.gdb"):
        LCA2()
