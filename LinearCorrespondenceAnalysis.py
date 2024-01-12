"""
-*- Code used to calculate the linear correspondence between the extracted and reference demarcations -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3
2024-01-12

"""
import arcpy
from Tmp.BatchClip import BatchClip
from Tmp.BatchClip import BatchClip

def LCA1():  # Linear Correspondence visual

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    dem_YOD1985_final = "dem_YOD1985_final"
    Demarcations_manual_reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Dem_Validation.gdb\\Demarcations_ManualRef_Coding"
    demarcations_automatic_extraction = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\Demarcations.gdb\\dem_YOD1985_final"
    HexGrid_random_selection = "HexGrid10km2__100RandomSelect"
    Dry_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Base_files\\Chaco\\Limites\\GranChaco_DRY.shp"
    Humid_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Base_files\\Chaco\\Limites\\GranChaco_HUMID.shp"
    reference_clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_reference"
    reference_sure_clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_reference"
    matched_sure_clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_matched"
    matched_clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_matched"
    extracted_clipped = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_extracted"

    # Process: Copy (Copy) (management)
    reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\reference"
    arcpy.management.Copy(in_data=Demarcations_manual_reference, out_data=reference, data_type="", associated_data=[])

    # Process: Summary Statistics (4) (Summary Statistics) (analysis)
    reference_all_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\referenceTotal_Statistics"
    arcpy.analysis.Statistics(in_table=reference, out_table=reference_all_, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

    # Process: Summary Statistics (5) (Summary Statistics) (analysis)
    reference_sure_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\reference_Statistics"
    arcpy.analysis.Statistics(in_table=reference, out_table=reference_sure_, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["DemSure"], concatenation_separator="")

    # Process: Buffer (Buffer) (analysis)
    buffered_reference = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\DemsManualRef_Buffer"
    arcpy.analysis.Buffer(in_features=Demarcations_manual_reference, out_feature_class=buffered_reference, buffer_distance_or_field="25 Meters", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Pairwise Intersect (Pairwise Intersect) (analysis)
    matched = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matched"
    arcpy.analysis.PairwiseIntersect(in_features=[demarcations_automatic_extraction, buffered_reference], out_feature_class=matched, join_attributes="ALL", cluster_tolerance="", output_type="LINE")

    # Process: Summary Statistics (3) (Summary Statistics) (analysis)
    matched_sure_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matchedSure_Statistics"
    arcpy.analysis.Statistics(in_table=matched, out_table=matched_sure_, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["DemSure"], concatenation_separator="")

    # Process: Summary Statistics (2) (Summary Statistics) (analysis)
    matched_all_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matchedTotal_Statistics"
    arcpy.analysis.Statistics(in_table=matched, out_table=matched_all_, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

    # Process: Clip (Clip) (analysis)
    extracted = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\extracted"
    arcpy.analysis.Clip(in_features=demarcations_automatic_extraction, clip_features=HexGrid_random_selection, out_feature_class=extracted, cluster_tolerance="")

    # Process: Summary Statistics (1) (Summary Statistics) (analysis)
    extracted_dems = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\extractedTotal_Statistics"
    arcpy.analysis.Statistics(in_table=extracted, out_table=extracted_dems, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

    # Process: Batch Clip (Batch Clip) (Tmp)
    acuraccy_metrics_clipped_dry_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_DRY_%Name%"
    BatchClip(in_features=[extracted, matched, reference], clip_features=Dry_Chaco, out_feature_class=acuraccy_metrics_clipped_dry_chaco, cluster_tolerance="")

    # Process: Batch Clip (2) (Batch Clip) (Tmp)
    acuraccy_metrics_clipped_humid_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\GranChaco_HUMID_%Name%"
    BatchClip(in_features=[extracted, matched, reference], clip_features=Humid_Chaco, out_feature_class=acuraccy_metrics_clipped_humid_chaco, cluster_tolerance="")

    # Process: Summary Statistics (9) (Summary Statistics) (analysis)
    reference_all_dry_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\reference_DryChaco_All"
    arcpy.analysis.Statistics(in_table=reference_clipped, out_table=reference_all_dry_chaco, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

    # Process: Summary Statistics (10) (Summary Statistics) (analysis)
    reference_sure_dry_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\reference_DryChaco_sure"
    arcpy.analysis.Statistics(in_table=reference_sure_clipped, out_table=reference_sure_dry_chaco, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["DemSure"], concatenation_separator="")

    # Process: Summary Statistics (8) (Summary Statistics) (analysis)
    matched_sure_dry_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matched_DryChaco_Sure"
    arcpy.analysis.Statistics(in_table=matched_sure_clipped, out_table=matched_sure_dry_chaco, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=["DemSure"], concatenation_separator="")

    # Process: Summary Statistics (7) (Summary Statistics) (analysis)
    matched_all_dry_chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\matched_DryChaco"
    arcpy.analysis.Statistics(in_table=matched_clipped, out_table=matched_all_dry_chaco, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

    # Process: Summary Statistics (6) (Summary Statistics) (analysis)
    extracted_Dry_Chaco = "D:\\GIS_Chapter1\\Demarcation_analysis\\Validation\\LinearCorrespondence.gdb\\extracted_DryChaco"
    arcpy.analysis.Statistics(in_table=extracted_clipped, out_table=extracted_Dry_Chaco, statistics_fields=[["SHAPE_Length", "SUM"]], case_field=[], concatenation_separator="")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LinearCorrespondence.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Validation\LinearCorrespondence.gdb"):
        LCA1()
