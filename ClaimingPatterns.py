"""
-*- Code used to assign aggregate pixels to the claiming pattern typology -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""
import arcpy
from arcpy.sa import *

def ClaimingPatternModel():  # ClaimingPatternModel1500_DNB5

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")

    Density = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics_1500Filt.gdb\\Density1500_correctedNB5")
    Peak_Period = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics_1500Filt.gdb\\PeakPeriod1500_classified")
    Recent_Activity = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics_1500Filt.gdb\\RecentActivity1500_2Classes2016")
    Speed = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics_1500Filt.gdb\\Speed1500_NB3")

    # Process: Reclassify - 5 (Reclassify) (sa)
    Density_Med_High_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Density1500_MedVHigh"
    Reclassify_5 = Density_Med_High_
    Density_Med_High_ = arcpy.sa.Reclassify(in_raster=Density, reclass_field="Value", remap="1 0;2 0;3 1;4 1;5 1", missing_values="DATA")
    Density_Med_High_.save(Reclassify_5)


    # Process: Reclassify - 4 (Reclassify) (sa)
    Peak_1986_2020_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Peak1500_19862020"
    Reclassify_4 = Peak_1986_2020_
    Peak_1986_2020_ = arcpy.sa.Reclassify(in_raster=Peak_Period, reclass_field="Value", remap="1 1;2 1;3 1;4 1;5 1", missing_values="DATA")
    Peak_1986_2020_.save(Reclassify_4)


    # Process: Reclassify - 7 (Reclassify) (sa)
    Active_Less_5_years_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Active1500_Less5"
    Reclassify_7 = Active_Less_5_years_
    Active_Less_5_years_ = arcpy.sa.Reclassify(in_raster=Recent_Activity, reclass_field="Value", remap="1 0;2 1", missing_values="DATA")
    Active_Less_5_years_.save(Reclassify_7)


    # Process: Raster Calculator (2) (Raster Calculator) (sa)
    Sum_Consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Hotspots_Consolidating"
    Raster_Calculator_2_ = Sum_Consolidating
    Sum_Consolidating = Density_Med_High_ + Peak_1986_2020_ +   Active_Less_5_years_
    Sum_Consolidating.save(Raster_Calculator_2_)


    # Process: Reclassify - 10 (Reclassify) (sa)
    Consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Consolidating1500"
    Reclassify_10 = Consolidating
    Consolidating = arcpy.sa.Reclassify(in_raster=Sum_Consolidating, reclass_field="Value", remap="0 0;1 0;2 0;3 1", missing_values="DATA")
    Consolidating.save(Reclassify_10)


    # Process: Reclassify - 6 (Reclassify) (sa)
    Peak_1986_2014_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Peak1500_19862014"
    Reclassify_6 = Peak_1986_2014_
    Peak_1986_2014_ = arcpy.sa.Reclassify(in_raster=Peak_Period, reclass_field="Value", remap="1 1;2 1;3 1;4 1;5 0", missing_values="DATA")
    Peak_1986_2014_.save(Reclassify_6)


    # Process: Reclassify - 8 (Reclassify) (sa)
    Inactive_More_5years_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Inactive1500_More5"
    Reclassify_8 = Inactive_More_5years_
    Inactive_More_5years_ = arcpy.sa.Reclassify(in_raster=Recent_Activity, reclass_field="Value", remap="1 1;2 0", missing_values="DATA")
    Inactive_More_5years_.save(Reclassify_8)


    # Process: Raster Calculator (4) (Raster Calculator) (sa)
    Sum_Maintained_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Hotspots_Maintained"
    Raster_Calculator_4_ = Sum_Maintained_2_
    Sum_Maintained_2_ = Density_Med_High_ + Peak_1986_2014_ +   Inactive_More_5years_
    Sum_Maintained_2_.save(Raster_Calculator_4_)


    # Process: Reclassify - 11 (2) (Reclassify) (sa)
    Maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Maintained1500"
    Reclassify_11_2_ = Maintained
    Maintained = arcpy.sa.Reclassify(in_raster=Sum_Maintained_2_, reclass_field="Value", remap="0 0;1 0;2 0;3 1;NODATA 0", missing_values="DATA")
    Maintained.save(Reclassify_11_2_)


    # Process: Reclassify - 2 (2) (Reclassify) (sa)
    Density_Low_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Density1500_Low"
    Reclassify_2_2_ = Density_Low_
    Density_Low_ = arcpy.sa.Reclassify(in_raster=Density, reclass_field="Value", remap="1 1;2 1;3 0;4 0;5 0", missing_values="DATA")
    Density_Low_.save(Reclassify_2_2_)


    # Process: Reclassify - 4 (2) (Reclassify) (sa)
    Peak_2000_2020 = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Peak1500_20002020"
    Reclassify_4_2_ = Peak_2000_2020
    Peak_2000_2020 = arcpy.sa.Reclassify(in_raster=Peak_Period, reclass_field="Value", remap="1 0;2 0;3 1;4 1;5 1", missing_values="DATA")
    Peak_2000_2020.save(Reclassify_4_2_)


    # Process: Reclassify - 1 (Reclassify) (sa)
    Speed_Med_Fast_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Speed1500_MedFast"
    Reclassify_1 = Speed_Med_Fast_
    Speed_Med_Fast_ = arcpy.sa.Reclassify(in_raster=Speed, reclass_field="Value", remap="1 1;2 1;3 0", missing_values="NODATA")
    Speed_Med_Fast_.save(Reclassify_1)


    # Process: Raster Calculator (5) (Raster Calculator) (sa)
    Sum_Emerging_2_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Hotspots_Emerging"
    Raster_Calculator_5_ = Sum_Emerging_2_
    Sum_Emerging_2_ = Density_Low_ + Peak_2000_2020 + Active_Less_5_years_ + Speed_Med_Fast_
    Sum_Emerging_2_.save(Raster_Calculator_5_)


    # Process: Reclassify - 9 (2) (Reclassify) (sa)
    Emerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\ClaimingPatterns\\Pattern_1500Filt.gdb\\Emerging1500"
    Reclassify_9_2_ = Emerging
    Emerging = arcpy.sa.Reclassify(in_raster=Sum_Emerging_2_, reclass_field="Value", remap="0 0;1 0;2 0;3 0;4 1", missing_values="DATA")
    Emerging.save(Reclassify_9_2_)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Metrics\Metrics_UnFilt.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Metrics\Metrics_UnFilt.gdb"):
        ClaimingHotspotsModel1111()

