"""
-*- Code to generate summary statistics comparing claiming and deforestation metrics -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""
import arcpy

def ClaimVsERLsummarytables1():  # ClaimVsERLsummarytablesUPDATE

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Conversion Tools.tbx")
    DemERLmetrics_JOINED_8_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\Joined.gdb\\DemERLmetrics_JOINED"
    CHACO_AdminBoundaries = "CHACO_AdminBoundaries"

    # Process: Project (Project) (management)
    DemERLmetrics_JOINED_Project = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_JOINED_Project"
    arcpy.management.Project(in_dataset=DemERLmetrics_JOINED_8_, out_dataset=DemERLmetrics_JOINED_Project, out_coor_system="PROJCS[\"WGS_1984_UTM_Zone_18S\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",10000000.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", transform_method=[], in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

    # Process: Copy (4) (Copy) (management)
    DemERLmetrics_JOINED1 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_JOINED1"
    arcpy.management.Copy(in_data=DemERLmetrics_JOINED_Project, out_data=DemERLmetrics_JOINED1, data_type="", associated_data=[])

    # Process: Select Layer By Attribute (3) (Select Layer By Attribute) (management)
    DemERLmetrics_JOINED1_Layer, Count_3_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=DemERLmetrics_JOINED1, selection_type="NEW_SELECTION", where_clause="ERLmetric_Activeness >= 2", invert_where_clause="")

    # Process: Export Features (3) (Export Features) (conversion)
    DemERLmetrics_ERLActiveEmerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__ERLActiveEmerging"
    arcpy.conversion.ExportFeatures(in_features=DemERLmetrics_JOINED1_Layer, out_features=DemERLmetrics_ERLActiveEmerging, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="", sort_field=[])

    # Process: Near (Near) (analysis)
    DemERLmetrics_JOINED_2_ = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED_Project, near_features=[DemERLmetrics_ERLActiveEmerging], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestACTIVtoPeak_FID"], ["NEAR_DIST", "NearestACTIVtoPeak_DIST"]])[0]

    # Process: Near (2) (Near) (analysis)
    DemERLmetrics_JOINED = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED_2_, near_features=[DemERLmetrics_ERLActiveEmerging], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestACTIVtoDens_FID"], ["NEAR_DIST", "NearestACTIVtoDens_DIST"]])[0]

    # Process: Near (3) (Near) (analysis)
    DemERLmetrics_JOINED_3_ = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED, near_features=[DemERLmetrics_ERLActiveEmerging], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestACTIVtoSpeed_FID"], ["NEAR_DIST", "NearestACTIVtoSpeed_DIST"]])[0]

    # Process: Near (4) (Near) (analysis)
    DemERLmetrics_JOINED_4_ = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED_3_, near_features=[DemERLmetrics_ERLActiveEmerging], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestACTIVtoRecent_FID"], ["NEAR_DIST", "NearestACTIVtoRecent_DIST"]])[0]

    # Process: Copy (3) (Copy) (management)
    DemERLmetrics_JOINED3 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_JOINED3"
    arcpy.management.Copy(in_data=DemERLmetrics_JOINED_Project, out_data=DemERLmetrics_JOINED3, data_type="", associated_data=[])

    # Process: Select Layer By Attribute (4) (Select Layer By Attribute) (management)
    DemERLmetrics_JOINED3_2_, Count_4_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=DemERLmetrics_JOINED3, selection_type="NEW_SELECTION", where_clause="ERLmetric_Speed = 1", invert_where_clause="")

    # Process: Export Features (Export Features) (conversion)
    DemERLmetrics_ERLFast = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__ERLFast"
    arcpy.conversion.ExportFeatures(in_features=DemERLmetrics_JOINED3_2_, out_features=DemERLmetrics_ERLFast, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="", sort_field=[])

    # Process: Near (5) (Near) (analysis)
    DemERLmetrics_JOINED_5_ = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED_4_, near_features=[DemERLmetrics_ERLFast], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestFASTtoRecent_FID"], ["NEAR_DIST", "NearestFASTtoRecent_DIST"]])[0]

    # Process: Copy (2) (Copy) (management)
    DemERLmetrics_JOINED2 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_JOINED2"
    arcpy.management.Copy(in_data=DemERLmetrics_JOINED_Project, out_data=DemERLmetrics_JOINED2, data_type="", associated_data=[])

    # Process: Select Layer By Attribute (5) (Select Layer By Attribute) (management)
    DemERLmetrics_JOINED2_Layer, Count_5_ = arcpy.management.SelectLayerByAttribute(in_layer_or_view=DemERLmetrics_JOINED2, selection_type="NEW_SELECTION", where_clause="ERLmetric_Onset >= 2015", invert_where_clause="")

    # Process: Export Features (2) (Export Features) (conversion)
    DemERLmetrics_ERLOnset2015_2019 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__ERLOnset2015_2019"
    arcpy.conversion.ExportFeatures(in_features=DemERLmetrics_JOINED2_Layer, out_features=DemERLmetrics_ERLOnset2015_2019, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="", sort_field=[])

    # Process: Near (6) (Near) (analysis)
    final_near = arcpy.analysis.Near(in_features=DemERLmetrics_JOINED_5_, near_features=[DemERLmetrics_ERLOnset2015_2019], search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="PLANAR", field_names=[["NEAR_FID", "NearestONSETtoPeak_FID"], ["NEAR_DIST", "NearestONSETtoPeak_DIST"]])[0]

    # Process: Spatial Join (Spatial Join) (analysis)
    DemERLmetrics_JOINED_FINAL = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL"
    arcpy.analysis.SpatialJoin(target_features=final_near, join_features=CHACO_AdminBoundaries, out_feature_class=DemERLmetrics_JOINED_FINAL, join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping="", match_option="INTERSECT", search_radius="", distance_field_name="")

    # Process: Export Table (Export Table) (conversion)
    DemERLmetricsJOINED_FINALtable = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetricsJOINED_FINALtable"
    arcpy.conversion.ExportTable(in_table=DemERLmetrics_JOINED_FINAL, out_table=DemERLmetricsJOINED_FINALtable, where_clause="", use_field_alias_as_name="NOT_USE_ALIAS", field_mapping="Join_Count \"Join_Count\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Join_Count,-1,-1;TARGET_FID \"TARGET_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,TARGET_FID,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,TARGET_FID,-1,-1;GRID_ID \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,GRID_ID,0,12;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ORIG_FID,-1,-1;ERLmetric_ProgLeap \"ERLmetric_ProgLeap_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_ProgLeap,-1,-1;ERLmetric_Onset \"ERLmetric_Onset_1\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_Onset,-1,-1;ERLmetric_Woodland \"ERLmetric_Woodland_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_Woodland,-1,-1;ERLmetric_Speed \"ERLmetric_Speed_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_Speed,-1,-1;ERLmetric_Transition \"ERLmetric_Transition_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_Transition,-1,-1;ERLmetric_Activeness \"ERLmetric_Activeness_1\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ERLmetric_Activeness,-1,-1;OBJECTID \"OBJECTID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,OBJECTID,-1,-1;GRID_ID_1 \"GRID_ID\" true true false 12 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,GRID_ID_1,0,12;ORIG_FID_1 \"ORIG_FID\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,ORIG_FID_1,-1,-1;Density1500_correctedNB5 \"Density1500_correctedNB5\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Density1500_correctedNB5,-1,-1;Density1500Corrected_unclassified \"Density1500Corrected_unclassified\" true true false 4 Float 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Density1500Corrected_unclassified,-1,-1;PeakPeriod1500_classified \"PeakPeriod1500_classified\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,PeakPeriod1500_classified,-1,-1;PeakPeriod1500_unclassified \"PeakPeriod1500_unclassified\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,PeakPeriod1500_unclassified,-1,-1;RecentActivity1500_2Classes2016 \"RecentActivity1500_2Classes2016\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,RecentActivity1500_2Classes2016,-1,-1;RecentActivity1500_unclassified \"RecentActivity1500_unclassified\" true true false 4 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,RecentActivity1500_unclassified,-1,-1;Speed1500_NB3 \"Speed1500_NB3\" true true false 2 Short 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Speed1500_NB3,-1,-1;Speed1500_unclassified \"Speed1500_unclassified\" true true false 4 Float 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Speed1500_unclassified,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Shape_Length,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Shape_Area,-1,-1,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,Shape_Area,-1,-1;NearestACTIVtoPeak_FID \"NearestACTIVtoPeak_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoPeak_FID,-1,-1;NearestACTIVtoPeak_DIST \"NearestACTIVtoPeak_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoPeak_DIST,-1,-1;NearestACTIVtoDens_FID \"NearestACTIVtoDens_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoDens_FID,-1,-1;NearestACTIVtoDens_DIST \"NearestACTIVtoDens_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoDens_DIST,-1,-1;NearestACTIVtoSpeed_FID \"NearestACTIVtoSpeed_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoSpeed_FID,-1,-1;NearestACTIVtoSpeed_DIST \"NearestACTIVtoSpeed_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoSpeed_DIST,-1,-1;NearestACTIVtoRecent_FID \"NearestACTIVtoRecent_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoRecent_FID,-1,-1;NearestACTIVtoRecent_DIST \"NearestACTIVtoRecent_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestACTIVtoRecent_DIST,-1,-1;NearestFASTtoRecent_FID \"NearestFASTtoRecent_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestFASTtoRecent_FID,-1,-1;NearestFASTtoRecent_DIST \"NearestFASTtoRecent_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestFASTtoRecent_DIST,-1,-1;NearestONSETtoPeak_FID \"NearestONSETtoPeak_FID\" true true false 0 Long 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestONSETtoPeak_FID,-1,-1;NearestONSETtoPeak_DIST \"NearestONSETtoPeak_DIST\" true true false 0 Double 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,NearestONSETtoPeak_DIST,-1,-1;name \"name\" true true false 254 Text 0 0,First,#,D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics__JOINED_FINAL,name,0,254", sort_field=[])

    # Process: Summary Statistics (Summary Statistics) (analysis)
    DemERLmetrics_SummaryDensity = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummaryDensity"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummaryDensity, statistics_fields=[["NearestACTIVtoDens_DIST", "MEAN"], ["NearestACTIVtoDens_DIST", "MEDIAN"], ["NearestACTIVtoDens_DIST", "VARIANCE"], ["NearestACTIVtoDens_DIST", "STD"]], case_field=["Density1500_correctedNB5"], concatenation_separator="")

    # Process: Table To Excel (Table To Excel) (conversion)
    NearesACTIVtoDens_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoDens.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummaryDensity], Output_Excel_File=NearesACTIVtoDens_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (2) (Summary Statistics) (analysis)
    DemERLmetrics_SummaryPeak = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummaryPeak"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummaryPeak, statistics_fields=[["NearestACTIVtoPeak_DIST", "MEAN"], ["NearestACTIVtoPeak_DIST", "MEDIAN"], ["NearestACTIVtoPeak_DIST", "VARIANCE"], ["NearestACTIVtoPeak_DIST", "STD"]], case_field=["PeakPeriod1500_classified"], concatenation_separator="")

    # Process: Table To Excel (2) (Table To Excel) (conversion)
    NearesACTIVtoPeak_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoPeak.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummaryPeak], Output_Excel_File=NearesACTIVtoPeak_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (3) (Summary Statistics) (analysis)
    DemERLmetrics_SummarySpeed = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummarySpeed"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummarySpeed, statistics_fields=[["NearestACTIVtoSpeed_DIST", "MEAN"], ["NearestACTIVtoSpeed_DIST", "MEDIAN"], ["NearestACTIVtoSpeed_DIST", "VARIANCE"], ["NearestACTIVtoSpeed_DIST", "STD"]], case_field=["Speed1500_NB3"], concatenation_separator="")

    # Process: Table To Excel (3) (Table To Excel) (conversion)
    NearesACTIVtoSpeed_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoSpeed.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummarySpeed], Output_Excel_File=NearesACTIVtoSpeed_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (4) (Summary Statistics) (analysis)
    DemERLmetrics_SummaryRecent = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummaryRecent"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummaryRecent, statistics_fields=[["NearestACTIVtoRecent_DIST", "MEAN"], ["NearestACTIVtoRecent_DIST", "MEDIAN"], ["NearestACTIVtoRecent_DIST", "VARIANCE"], ["NearestACTIVtoRecent_DIST", "STD"]], case_field=["RecentActivity1500_2Classes2016", "name"], concatenation_separator="")

    # Process: Table To Excel (4) (Table To Excel) (conversion)
    NearesACTIVtoRecent_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoRecent.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummaryRecent], Output_Excel_File=NearesACTIVtoRecent_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (5) (Summary Statistics) (analysis)
    DemERLmetrics_FastxSpeed = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_FastxSpeed"
    arcpy.analysis.Statistics(in_table="", out_table=DemERLmetrics_FastxSpeed, statistics_fields=[["NearestFASTtoSpeed_DIST", "MEAN"], ["NearestFASTtoSpeed_DIST", "MEDIAN"], ["NearestFASTtoSpeed_DIST", "VARIANCE"], ["NearestFASTtoSpeed_DIST", "STD"]], case_field=["Speed1500_NB3", "name"], concatenation_separator="")

    # Process: Table To Excel (5) (Table To Excel) (conversion)
    NearesFasttoSpeed_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesFasttoSpeed.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_FastxSpeed], Output_Excel_File=NearesFasttoSpeed_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (6) (Summary Statistics) (analysis)
    DemERLmetrics_OnsetxPeak = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_OnsetxPeak"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_OnsetxPeak, statistics_fields=[["NearestONSETtoPeak_DIST", "MEAN"], ["NearestONSETtoPeak_DIST", "MEDIAN"], ["NearestONSETtoPeak_DIST", "VARIANCE"], ["NearestONSETtoPeak_DIST", "STD"]], case_field=["PeakPeriod1500_classified", "name"], concatenation_separator="")

    # Process: Table To Excel (6) (Table To Excel) (conversion)
    NearesOnsettoPeak_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesOnsettoPeak.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_OnsetxPeak], Output_Excel_File=NearesOnsettoPeak_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (7) (Summary Statistics) (analysis)
    SummaryDensityXCountry = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\SummaryDensityXCountry"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=SummaryDensityXCountry, statistics_fields=[["NearestACTIVtoDens_DIST", "MEAN"], ["NearestACTIVtoDens_DIST", "MEDIAN"], ["NearestACTIVtoDens_DIST", "VARIANCE"], ["NearestACTIVtoDens_DIST", "STD"]], case_field=["Density1500_correctedNB5", "name"], concatenation_separator="")

    # Process: Table To Excel (7) (Table To Excel) (conversion)
    NearesACTIVtoDensXCountry_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoDensXCountry.xls"
    arcpy.conversion.TableToExcel(Input_Table=[SummaryDensityXCountry], Output_Excel_File=NearesACTIVtoDensXCountry_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (8) (Summary Statistics) (analysis)
    DemERLmetrics_SummaryPeakXCountry = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummaryPeakXCountry"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummaryPeakXCountry, statistics_fields=[["NearestACTIVtoPeak_DIST", "MEAN"], ["NearestACTIVtoPeak_DIST", "MEDIAN"], ["NearestACTIVtoPeak_DIST", "VARIANCE"], ["NearestACTIVtoPeak_DIST", "STD"]], case_field=["PeakPeriod1500_classified", "name"], concatenation_separator="")

    # Process: Table To Excel (8) (Table To Excel) (conversion)
    NearesACTIVtoPeakXCountry_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoPeakXCountry.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummaryPeakXCountry], Output_Excel_File=NearesACTIVtoPeakXCountry_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

    # Process: Summary Statistics (9) (Summary Statistics) (analysis)
    DemERLmetrics_SummarySpeedXCountry = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimVsERL\\DistanceMetrics.gdb\\DemERLmetrics_SummarySpeedXCountry"
    arcpy.analysis.Statistics(in_table=DemERLmetricsJOINED_FINALtable, out_table=DemERLmetrics_SummarySpeedXCountry, statistics_fields=[["NearestACTIVtoSpeed_DIST", "MEAN"], ["NearestACTIVtoSpeed_DIST", "MEDIAN"], ["NearestACTIVtoSpeed_DIST", "VARIANCE"], ["NearestACTIVtoSpeed_DIST", "STD"]], case_field=["Speed1500_NB3", "name"], concatenation_separator="")

    # Process: Table To Excel (9) (Table To Excel) (conversion)
    NearesACTIVtoSpeedXCountry_xls = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Stats\\NearesACTIVtoSpeedXCountry.xls"
    arcpy.conversion.TableToExcel(Input_Table=[DemERLmetrics_SummarySpeedXCountry], Output_Excel_File=NearesACTIVtoSpeedXCountry_xls, Use_field_alias_as_column_header="NAME", Use_domain_and_subtype_description="CODE")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\ClaimVsERL\DistanceMetrics.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\ClaimVsERL\DistanceMetrics.gdb"):
        ClaimVsERLsummarytables1()
