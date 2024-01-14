"""
-*- Code used to assign aggregate pixels to the claiming pattern typology -*-

del Giorgio et al. 
ArcGIS Pro version 3.0.3

"""

import arcpy
from arcpy.sa import *
from arcpy.sa import *
from arcpy.sa import *

def ClaimingHotspotsModel():  # ClaimingHotspots Model

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    # Check out any necessary licenses.
    arcpy.CheckOutExtension("3D")
    arcpy.CheckOutExtension("spatial")
    arcpy.CheckOutExtension("ImageAnalyst")

    Density = arcpy.Raster("Density_Weighted_NaturalClasses")
    Peak_Period = arcpy.Raster("PeakPeriod_classified")
    Recent_Activity = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics.gdb\\RecentActivity_2Classes")
    Speed = arcpy.Raster("D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Metrics.gdb\\Speed_NaturalClasses")

    # Process: Reclassify - 2 (Reclassify) (sa)
    Density_Low_Med_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Density_LowMed"
    Reclassify_2 = Density_Low_Med_
    Density_Low_Med_ = arcpy.sa.Reclassify(in_raster=Density, reclass_field="Value", remap="1 1;2 1;3 1;4 1;5 0;6 0", missing_values="DATA")
    Density_Low_Med_.save(Reclassify_2)


    # Process: Reclassify - 4 (Reclassify) (sa)
    Peak_1995_2020_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Peak_1995_2020"
    Reclassify_4 = Peak_1995_2020_
    Peak_1995_2020_ = arcpy.sa.Reclassify(in_raster=Peak_Period, reclass_field="Value", remap="1 0;2 1;3 1;4 1;5 1", missing_values="DATA")
    Peak_1995_2020_.save(Reclassify_4)


    # Process: Reclassify - 7 (Reclassify) (sa)
    Active_Less_5_years_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Active_Less5"
    Reclassify_7 = Active_Less_5_years_
    Active_Less_5_years_ = arcpy.sa.Reclassify(in_raster=Recent_Activity, reclass_field="Value", remap="1 0;2 1", missing_values="DATA")
    Active_Less_5_years_.save(Reclassify_7)


    # Process: Reclassify - 1 (Reclassify) (sa)
    Speed_Med_Fast_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Speed_MedFast"
    Reclassify_1 = Speed_Med_Fast_
    Speed_Med_Fast_ = arcpy.sa.Reclassify(in_raster=Speed, reclass_field="Value", remap="1 1;2 1;3 0", missing_values="NODATA")
    Speed_Med_Fast_.save(Reclassify_1)


    # Process: Raster Calculator (Raster Calculator) (sa)
    Sum_Emerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\hotspots_update.gdb\\Hotspots_Emerging"
    Raster_Calculator = Sum_Emerging
    Sum_Emerging =  "%Density_LowMed%" + "%Peak_1995_2020%" + Active_Less_5_years_ + "%Speed Med-Fast%"
    Sum_Emerging.save(Raster_Calculator)


    # Process: Reclassify - 9 (Reclassify) (sa)
    Emerging = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Emerging"
    Reclassify_9 = Emerging
    Emerging = arcpy.sa.Reclassify(in_raster=Sum_Emerging, reclass_field="VALUE", remap="0 0;1 0;2 0;3 0;4 1", missing_values="DATA")
    Emerging.save(Reclassify_9)


    # Process: Reclassify - 5 (Reclassify) (sa)
    Density_Med_High_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Density_MedHigh"
    Reclassify_5 = Density_Med_High_
    Density_Med_High_ = arcpy.sa.Reclassify(in_raster=Density, reclass_field="Value", remap="1 0;2 0;3 0;4 1;5 1;6 1", missing_values="DATA")
    Density_Med_High_.save(Reclassify_5)


    # Process: Raster Calculator (2) (Raster Calculator) (sa)
    Sum_Consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\hotspots_update.gdb\\Hotspots_Consolidating"
    Raster_Calculator_2_ = Sum_Consolidating
    Sum_Consolidating =  "%Density_MedHigh%" + "%Peak_1995_2020%" + Active_Less_5_years_
    Sum_Consolidating.save(Raster_Calculator_2_)


    # Process: Reclassify - 10 (Reclassify) (sa)
    Consolidating = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Consolidating"
    Reclassify_10 = Consolidating
    Consolidating = arcpy.sa.Reclassify(in_raster=Sum_Consolidating, reclass_field="VALUE", remap="0 0;1 0;2 0;3 1", missing_values="DATA")
    Consolidating.save(Reclassify_10)


    # Process: Reclassify - 3 (Reclassify) (sa)
    Density_High_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Density_High"
    Reclassify_3 = Density_High_
    Density_High_ = arcpy.sa.Reclassify(in_raster=Density, reclass_field="Value", remap="1 0;2 0;3 0;4 0;5 1;6 1", missing_values="DATA")
    Density_High_.save(Reclassify_3)


    # Process: Reclassify - 6 (Reclassify) (sa)
    Peak_1995_2014_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Peak_1995_2014"
    Reclassify_6 = Peak_1995_2014_
    Peak_1995_2014_ = arcpy.sa.Reclassify(in_raster=Peak_Period, reclass_field="Value", remap="1 0;2 1;3 1;4 1;5 0", missing_values="DATA")
    Peak_1995_2014_.save(Reclassify_6)


    # Process: Reclassify - 8 (Reclassify) (sa)
    Inactive_More_5_years_ = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Inactive_More5"
    Reclassify_8 = Inactive_More_5_years_
    Inactive_More_5_years_ = arcpy.sa.Reclassify(in_raster=Recent_Activity, reclass_field="Value", remap="1 1;2 0", missing_values="DATA")
    Inactive_More_5_years_.save(Reclassify_8)


    # Process: Raster Calculator (3) (Raster Calculator) (sa)
    Sum_Maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\hotspots_update.gdb\\Hotspots_Maintained"
    Raster_Calculator_3_ = Sum_Maintained
    Sum_Maintained =  "%Density_High%" + "%Peak_1995_2014%" + Inactive_More_5_years_
    Sum_Maintained.save(Raster_Calculator_3_)


    # Process: Reclassify - 11 (Reclassify) (sa)
    Maintained = "D:\\GIS_Chapter1\\Demarcation_analysis\\Outputs\\Hotspots_UPDATE.gdb\\Maintained"
    Reclassify_11 = Maintained
    Maintained = arcpy.sa.Reclassify(in_raster=Sum_Maintained, reclass_field="VALUE", remap="0 0;1 0;2 0;3 1;NODATA 0", missing_values="DATA")
    Maintained.save(Reclassify_11)


if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Visualizations\Base_vis.gdb", workspace=r"D:\GIS_Chapter1\Demarcation_analysis\Outputs\Visualizations\Base_vis.gdb"):
        ClaimingHotspotsModel()
