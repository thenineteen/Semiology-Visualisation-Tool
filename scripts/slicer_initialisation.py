# run this from slicer when it runs for the first time. Then we have the df below and store it.
# next when a semiology is ticked and run, slicer should run slicer_run)query_semiology_lateralisation.py script

from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import *

df, df_ground_truth, df_study_type = MEGA_ANALYSIS(excel_data=excel_path)