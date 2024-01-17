"""
-*- Code to compare claiming metrics with smallholder puesto disappearance (Levers et al. 2022) -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3
2023-12-19 15:02:19

"""
import arcpy
from arcpy.ia import *

def PuestoDisapChoropleth():  # Disappeared puestos Choropleth

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Analysis Tools.tbx")
    Gran_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\Masks.gdb\\GranChaco"
    Puestos = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\RawPuestos.gdb\\AllPuestos"
    Maintained = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Maintained")
    Emerging = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Emerging")
    Consolidating = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Consolidating")
    Density_weighted_ = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\Inputs\\Metrics.gdb\\Density_weighted")
    Peak_Period_classified_ = arcpy.Raster("PeakPeriod_classified")
    Speed_classified_ = arcpy.Raster("Speed_NaturalClasses")
    Recent_Activity_2Classes_ = arcpy.Raster("RecentActivity_2Classes")

    # Process: Generate Tessellation (Generate Tessellation) (management)
    HexGrid = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003"
    arcpy.management.GenerateTessellation(Output_Feature_Class=HexGrid, Extent="-67.7200854859564 -33.8686498677971 -55.7623294678306 -17.54059819585 GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", Shape_Type="HEXAGON", Size="0.03 Unknown", Spatial_Reference="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1111948722.22222;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Clip (Clip) (analysis)
    Clipped_HexGrid = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003_Chaco"
    arcpy.analysis.Clip(in_features=HexGrid, clip_features=Gran_Chaco, out_feature_class=Clipped_HexGrid, cluster_tolerance="")

    # Process: Copy (Copy) (management)
    Puestos_MeansJoined = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Puestos_MeansJoined"
    arcpy.management.Copy(in_data=Puestos, out_data=Puestos_MeansJoined, data_type="FeatureClass", associated_data=[])

    # Process: Pairwise Buffer (Pairwise Buffer) (analysis)
    Puestos_Buffer_10_km = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\AllPuestos_Buffer10"
    arcpy.analysis.PairwiseBuffer(in_features=Puestos, out_feature_class=Puestos_Buffer_10_km, buffer_distance_or_field="10 Kilometers", dissolve_option="NONE", dissolve_field=[], method="PLANAR", max_deviation="0 DecimalDegrees")

    # Process: Zonal Statistics as Table (6) (Zonal Statistics as Table) (sa)
    Mean_Maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Maintained"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Maintained, out_table=Mean_Maintained, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_6_)


    # Process: Alter Field (1) (Alter Field) (management)
    Table_1 = arcpy.management.AlterField(in_table=Mean_Maintained, field="MEAN", new_field_name="MeanMaintained", new_field_alias="MeanMaintained", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (1) (Join Field) (management)
    Join_1_ = arcpy.management.JoinField(in_data=Puestos_MeansJoined, in_field="UID", join_table=Table_1, join_field="UID", fields=["MeanMaintained"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (7) (Zonal Statistics as Table) (sa)
    Mean_Emerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Emerging"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Emerging, out_table=Mean_Emerging, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_7_)


    # Process: Alter Field (2) (Alter Field) (management)
    Table_2 = arcpy.management.AlterField(in_table=Mean_Emerging, field="MEAN", new_field_name="MeanEmerging", new_field_alias="MeanEmerging", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (2) (Join Field) (management)
    Join_2_ = arcpy.management.JoinField(in_data=Join_1_, in_field="UID", join_table=Table_2, join_field="UID", fields=["MeanEmerging"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (8) (Zonal Statistics as Table) (sa)
    Mean_Consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Consolidating"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Consolidating, out_table=Mean_Consolidating, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_8_)


    # Process: Alter Field (3) (Alter Field) (management)
    Table_3 = arcpy.management.AlterField(in_table=Mean_Consolidating, field="MEAN", new_field_name="MeanConsolidating", new_field_alias="MeanConsolidating", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (3) (Join Field) (management)
    Join_3_ = arcpy.management.JoinField(in_data=Join_2_, in_field="UID", join_table=Table_3, join_field="UID", fields=["MeanConsolidating"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Raster Calculator (Raster Calculator) (ia)
    merge_3_types = "d:\\gis_chapter1\\demarcation_analysis\\Outputs\\smallholderimpacts\\Inputs\\Metrics.gdb\\mergepattern"
    Raster_Calculator = merge_3_types
    merge_3_types = "Maintained" + "Consolidating" + "Emerging"
    merge_3_types.save(Raster_Calculator)


    # Process: Zonal Statistics as Table (2) (Zonal Statistics as Table) (sa)
    Mean_Pattern_Single = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_PatternSingle"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=merge_3_types, out_table=Mean_Pattern_Single, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_2_)


    # Process: Alter Field (4) (Alter Field) (management)
    Table_4 = arcpy.management.AlterField(in_table=Mean_Pattern_Single, field="MEAN", new_field_name="MeanPattern", new_field_alias="MeanPattern", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (4) (Join Field) (management)
    Join_4_ = arcpy.management.JoinField(in_data=Join_3_, in_field="UID", join_table=Table_4, join_field="UID", fields=["MeanPattern"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (3) (Zonal Statistics as Table) (sa)
    mean_density_weighted_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Density"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Density_weighted_, out_table=mean_density_weighted_, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_3_)


    # Process: Alter Field (5) (Alter Field) (management)
    Table_5 = arcpy.management.AlterField(in_table=mean_density_weighted_, field="MEAN", new_field_name="MeanDensityW", new_field_alias="MeanDensityW", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (5) (Join Field) (management)
    Join_5_ = arcpy.management.JoinField(in_data=Join_4_, in_field="UID", join_table=Table_5, join_field="UID", fields=["MeanDensityW"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (4) (Zonal Statistics as Table) (sa)
    Mean_Peak_Period_classified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_PeakPeriodClassified"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Peak_Period_classified_, out_table=Mean_Peak_Period_classified_, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_4_)


    # Process: Alter Field (6) (Alter Field) (management)
    Table_6 = arcpy.management.AlterField(in_table=Mean_Peak_Period_classified_, field="MEAN", new_field_name="MeanPeakClass", new_field_alias="MeanPeakClass", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (6) (Join Field) (management)
    Join_6_ = arcpy.management.JoinField(in_data=Join_5_, in_field="UID", join_table=Table_6, join_field="UID", fields=["MeanPeakClass"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (5) (Zonal Statistics as Table) (sa)
    Mean_Speed_classified_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Speed"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Speed_classified_, out_table=Mean_Speed_classified_, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_5_)


    # Process: Alter Field (7) (Alter Field) (management)
    Table_7 = arcpy.management.AlterField(in_table=Mean_Speed_classified_, field="MEAN", new_field_name="MeanSpeed", new_field_alias="MeanSpeed", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (7) (Join Field) (management)
    Join_7_ = arcpy.management.JoinField(in_data=Join_6_, in_field="UID", join_table=Table_7, join_field="UID", fields=["MeanSpeed"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Zonal Statistics as Table (9) (Zonal Statistics as Table) (sa)
    MeanRecent_Activity = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\Buff10_ZonalMean_Recent"
    arcpy.sa.ZonalStatisticsAsTable(in_zone_data=Puestos_Buffer_10_km, zone_field="UID", in_value_raster=Recent_Activity_2Classes_, out_table=MeanRecent_Activity, ignore_nodata="DATA", statistics_type="MEAN", process_as_multidimensional="CURRENT_SLICE", percentile_values=[90], percentile_interpolation_type="AUTO_DETECT", circular_calculation="ARITHMETIC", circular_wrap_value=360)
    .save(Zonal_Statistics_as_Table_9_)


    # Process: Alter Field (8) (Alter Field) (management)
    Table_8 = arcpy.management.AlterField(in_table=MeanRecent_Activity, field="MEAN", new_field_name="MeanRecentAct", new_field_alias="MeanRecentAct", field_type="", field_length=8, field_is_nullable="NON_NULLABLE", clear_field_alias="DO_NOT_CLEAR")[0]

    # Process: Join Field (8) (Join Field) (management)
    Puestos_Means_Joined_All = arcpy.management.JoinField(in_data=Join_7_, in_field="UID", join_table=Table_8, join_field="UID", fields=["MeanRecentAct"], fm_option="NOT_USE_FM", field_mapping="")[0]

    # Process: Summarize Within (Summarize Within) (analysis)
    Summarized_Within = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\HexGrid003_Chaco_SummarizeWithin"
    F2018_Summary = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\SmallholderImpacts\\PuestoDisapChoropleth.gdb\\F2018_Summary"
    arcpy.analysis.SummarizeWithin(in_polygons=Clipped_HexGrid, in_sum_features=Puestos_Means_Joined_All, out_feature_class=Summarized_Within, keep_all_polygons="ONLY_INTERSECTING", sum_fields=[["F2018", "Sum"], ["MeanMaintained", "Mean"], ["MeanEmerging", "Mean"], ["MeanConsolidating", "Mean"], ["MeanPattern", "Mean"], ["MeanDensityW", "Mean"], ["MeanPeakClass", "Mean"], ["MeanSpeed", "Mean"], ["MeanRecentAct", "Mean"]], sum_shape="NO_SHAPE_SUM", shape_unit="SQUAREKILOMETERS", group_field="F2018", add_min_maj="NO_MIN_MAJ", add_group_percent="ADD_PERCENT", out_group_table=F2018_Summary)

    # Process: Transfrom point count to double (Calculate Field) (management)
    Updated = arcpy.management.CalculateField(in_table=Summarized_Within, field="Pointcount_double", expression="!Point_Count!", expression_type="PYTHON3", code_block="", field_type="LONG", enforce_domains="NO_ENFORCE_DOMAINS")[0]

    # Process: Calculate number disappeared (Calculate Field) (management)
    With_number_disappeared = arcpy.management.CalculateField(in_table=Updated, field="CountDisappeared2018", expression="!Point_Count! - !sum_F2018!", expression_type="PYTHON3", code_block="", field_type="DOUBLE", enforce_domains="NO_ENFORCE_DOMAINS")[0]

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\SmallholderImpacts\PuestoDisapChoropleth.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\SmallholderImpacts\PuestoDisapChoropleth.gdb"):
        PuestoDisapChoropleth()
