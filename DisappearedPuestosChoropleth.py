"""
-*- Code to compare claiming metrics with smallholder puesto disappearance (Levers et al. 2022) -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""
import arcpy

def PuestoDisapChoropleth():  # Disappeared puestos Choropleth

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Analysis Tools.tbx")
    Puestos = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\RawPuestos.gdb\\AllPuestos"
    Gran_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\Masks.gdb\\GranChaco"
    AllPuestos_Buffer10 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\AllPuestos_Buffer10"
    Density = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Density1500Corrected_Thresholded")
    Peak_Period = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\Metrics.gdb\\PeakPeriod1500_unclassified")
    Speed = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Speed1500_unclassified")
    Last_Activity = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\Inputs\\Metrics.gdb\\RecentActivity1500_unclassified")

    # Process: Project (Project) (management)
    AllPuestos_Project = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\AllPuestos_Project"
    arcpy.management.Project(in_dataset=Puestos, out_dataset=AllPuestos_Project, out_coor_system="PROJCS[\"WGS_1984_UTM_Zone_18S\",GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Transverse_Mercator\"],PARAMETER[\"False_Easting\",500000.0],PARAMETER[\"False_Northing\",10000000.0],PARAMETER[\"Central_Meridian\",-75.0],PARAMETER[\"Scale_Factor\",0.9996],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]", transform_method=[], in_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", preserve_shape="NO_PRESERVE_SHAPE", max_deviation="", vertical="NO_VERTICAL")

    # Process: Pairwise Buffer (Pairwise Buffer) (analysis)
    Puestos_Buffer_10_km = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\AllPuestos_Buffer10"
    arcpy.analysis.PairwiseBuffer(in_features=AllPuestos_Project, out_feature_class=Puestos_Buffer_10_km, buffer_distance_or_field="10 Kilometers", dissolve_option="NONE", dissolve_field=[], method="PLANAR", max_deviation="0 DecimalDegrees")

    # Process: Generate Tessellation (Generate Tessellation) (management)
    HexGrid = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003"
    arcpy.management.GenerateTessellation(Output_Feature_Class=HexGrid, Extent="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="HEXAGON", Size="0.03 Unknown", Spatial_Reference="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1111948722.22222;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Clip (Clip) (analysis)
    Clipped_HexGrid = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003_Chaco"
    arcpy.analysis.Clip(in_features=HexGrid, clip_features=Gran_Chaco, out_feature_class=Clipped_HexGrid, cluster_tolerance="")

    # Process: Copy (Copy) (management)
    Puestos_MeansJoined = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Puestos_MeansJoined"
    arcpy.management.Copy(in_data=AllPuestos_Project, out_data=Puestos_MeansJoined, data_type="", associated_data=[])

    # Process: Zonal Statistics as Table (3) (Zonal Statistics as Table) (sa)
    mean_density = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Density"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=AllPuestos_Buffer10, zone_field="UID", in_value_raster=Density, out_table=mean_density, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_3_)


    # Process: Alter Field (5) (Alter Field) (management)
    Table_5 = arcpy.management.AlterField(in_table=mean_density, field="MEAN", new_field_name="MeanDensityC", new_field_alias="MeanDensityC", field_type="DOUBLE", field_length=8, field_is_nullable="NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (5) (Join Field) (management)
    Join_5_ = arcpy.management.JoinField(in_data=Puestos_MeansJoined, in_field="UID", join_table=Table_5, join_field="UID", fields=["MeanDensityC"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (4) (Zonal Statistics as Table) (sa)
    Mean_Peak_Period = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_PeakPeriod"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=AllPuestos_Buffer10, zone_field="UID", in_value_raster=Peak_Period, out_table=Mean_Peak_Period, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_4_)


    # Process: Alter Field (6) (Alter Field) (management)
    Table_6 = arcpy.management.AlterField(in_table=Mean_Peak_Period, field="MEAN", new_field_name="MeanPeak", new_field_alias="MeanPeak", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (6) (Join Field) (management)
    Join_6_ = arcpy.management.JoinField(in_data=Join_5_, in_field="UID", join_table=Table_6, join_field="UID", fields=["MeanPeak"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (5) (Zonal Statistics as Table) (sa)
    Mean_Speed_classified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Speed"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=AllPuestos_Buffer10, zone_field="UID", in_value_raster=Speed, out_table=Mean_Speed_classified_, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_5_)


    # Process: Alter Field (7) (Alter Field) (management)
    Table_7 = arcpy.management.AlterField(in_table=Mean_Speed_classified_, field="MEAN", new_field_name="MeanSpeed", new_field_alias="MeanSpeed", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (7) (Join Field) (management)
    Join_7_ = arcpy.management.JoinField(in_data=Join_6_, in_field="UID", join_table=Table_7, join_field="UID", fields=["MeanSpeed"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (9) (Zonal Statistics as Table) (sa)
    MeanRecent_Activity = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Recent"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=AllPuestos_Buffer10, zone_field="UID", in_value_raster=Last_Activity, out_table=MeanRecent_Activity, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_9_)


    # Process: Alter Field (8) (Alter Field) (management)
    Table_8 = arcpy.management.AlterField(in_table=MeanRecent_Activity, field="MEAN", new_field_name="MeanRecentAct", new_field_alias="MeanRecentAct", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (8) (Join Field) (management)
    Puestos_Means_Joined_All = arcpy.management.JoinField(in_data=Join_7_, in_field="UID", join_table=Table_8, join_field="UID", fields=["MeanRecentAct"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Summarize Within (Summarize Within) (analysis)
    Summarized_Within = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003_Chaco_SummarizeWithin"
    F2018_Summary = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\OLD\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\F2018_Summary"
    arcpy.analysis.SummarizeWithin(in_polygons=Clipped_HexGrid, in_sum_features=Puestos_Means_Joined_All, out_feature_class=Summarized_Within, keep_all_polygons="ONLY_INTERSECTING", sum_fields=[["F2018", "Sum"], ["MeanDensityC", "Mean"], ["MeanPeak", "Mean"], ["MeanSpeed", "Mean"], ["MeanRecentAct", "Mean"]], sum_shape="ADD_SHAPE_SUM", shape_unit="SQUAREKILOMETERS", group_field="F2018", add_min_maj="NO_MIN_MAJ", add_group_percent="ADD_PERCENT", out_group_table=F2018_Summary)

    # Process: Transfrom point count to double (Calculate Field) (management)
    Updated = arcpy.management.CalculateField(in_table=Summarized_Within, field="Pointcount_double", expression="!Point_Count!", expression_type="PYTHON3", code_block="", field_type="LONG", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate number disappeared (Calculate Field) (management)
    With_number_disappeared = arcpy.management.CalculateField(in_table=Updated, field="CountDisappeared2018", expression="!Point_Count! - !sum_F2018!", expression_type="PYTHON3", code_block="", field_type="DOUBLE", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate number disappeared (2) (Calculate Field) (management)
    With_number_disappeared_2_ = arcpy.management.CalculateField(in_table=With_number_disappeared, field="PROPORTIONDisappeared2018", expression="!CountDisappeared2018!/!Point_Count!", expression_type="PYTHON3", code_block="", field_type="DOUBLE", enforce_domains="NO_ENFORCE_DOMAINS")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\OLD\SmallholderImpacts\PuestoDisapChoropleth.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\OLD\SmallholderImpacts\PuestoDisapChoropleth.gdb"):
        PuestoDisapChoroplethUPDATE()
