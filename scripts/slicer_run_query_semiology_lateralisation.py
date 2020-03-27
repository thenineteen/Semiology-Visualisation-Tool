#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import numpy as np
import pandas as pd
import pickle

# needed for querying dataframe localisations, Transforming and mapping to EpiNav gif parcellations
# from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import *
from mega_analysis.crosstab.mega_analysis.QUERY_SEMIOLOGY import *
from mega_analysis.crosstab.mega_analysis.QUERY_INTERSECTION_TERMS import QUERY_INTERSECTION_TERMS
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import *
from mega_analysis.crosstab.mega_analysis.pivot_result_to_pixel_intensities import *

# needed to collate lateralisation data
from mega_analysis.crosstab.mega_analysis.QUERY_LATERALISATION import *
from mega_analysis.crosstab.mega_analysis.lateralised_intensities import lateralisation_to_pixel_intensities
from mega_analysis.crosstab.mega_analysis.pivot_result_to_pixel_intensities import *

# mapping to gif
from mega_analysis.crosstab.mega_analysis.mapping import mapping, big_map, pivot_result_to_one_map

# exclusions:
from mega_analysis.crosstab.mega_analysis.exclusions import exclusions, exclude_ET, exclude_sEEG_ES

# resources
repo_dir = Path(__file__).parent.parent
resources_dir = repo_dir / 'resources'
excel_path = resources_dir / 'syst_review_single_table.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'
path_to_pickled_df_4 = resources_dir / DataFrames_Exclusions_df_postictalPEThyper_concordance_ET.pickle
path_to_pickled_df_1 = resources_dir / DataFrames_Exclusions_dfETconc.pickle

# load pickles:
with open(path_to_pickled_df_4, 'rb') as f:
        data = pickle.load(f)          
(df, # the entire df
 df_exclusions_postictal_PEThyper,  # df excluding postictals, PET hypermetabolism
             df_exclusions_concordance,  # df excluding all concordance criteria
             df_exclusions_ET,  # df exclusion epilepsy topology priors
             ) = data 

with open(path_to_pickled_df_1, 'rb') as f:
        data = pickle.load(f)
df_exclusions_ET_conc = data      # df exclusing both topology priors and concordance groun truths





# set the semiology of interest:
# semiology_term='Dialeptic/loa'
# semiology_term='tonic'
semiology_term='Head Version'

# I recommend keep this to True - needs a tick box in advanced slicer settings to toggle this off:
use_semiology_dictionary = True

# # LATERALISATION initilisation

## I reconmend minmaxscaler.
# method = 'non-linear'  # equivalent to QuantileTransformer
method = 'min_max'
# method = 'linear'
# method = 'chi2-dist'
# method = 'raw'  # return the data without scaling/transforming ()
scale_factor = 15
quantiles = 100


if method in ('non-linear', 'nonlinear'):
    raw_pt_numbers_string = 'normal QuantileTransformer'
else:
    raw_pt_numbers_string = str(method)
intensity_label = 'Lateralised Intensity. '+str(raw_pt_numbers_string)+'. '+'quantiles: '+str(quantiles)+'. '+'scale: '+str(scale_factor)


## The below is only required if the data collection has been updated 
# - otherwise use pickled DataFrame:
# df, df_ground_truth, df_study_type = MEGA_ANALYSIS(excel_data=excel_path)






# https://github.com/fepegar/EpilepsySemiology/issues/2
# so now it depends on slicer options on tick boxes: df is entire df. could use the other ones:
try:
    if slicer_tickbox_concordance == False:
        df_exclusions_concordance = exclusions(df, 
                POST_ictals=False,
                PET_hypermetabolism=False,
                SPECT_PET=False,
                CONCORDANCE=True)
        df = df_exclusions_concordance
except: pass

try:
    if slicer_tickbox_ET == False:
        
        df = exclude_ET(df)
except: pass

try:
    if slicer_tickbox_sEEG_ES == False:
        df = exclude_sEEG_ES(df)
except: pass





# now below df will reflect the Slicer Ground Truth and Prior Selections 
# https://github.com/fepegar/EpilepsySemiology/issues/2
inspect_result = QUERY_SEMIOLOGY(
    df,
    semiology_term=semiology_term,
    use_semiology_dictionary=use_semiology_dictionary,
)


# # 2.3 QUERY_LATERALISATION
all_combined_gifs = QUERY_LATERALISATION(
    inspect_result,
    df,
    excel_path,
    side_of_symptoms_signs='R',
    pts_dominant_hemisphere_R_or_L='L',
)

all_lateralised_gifs = lateralisation_to_pixel_intensities(
    all_combined_gifs,
    df,
    semiology_term,
    quantiles,
    method=method,
    scale_factor=scale_factor,
    intensity_label=intensity_label,
    use_semiology_dictionary=use_semiology_dictionary,
)

array = np.array(all_lateralised_gifs)
labels = array[:, 1].astype(np.uint16)
scores = array[:, 3].astype(np.float32)

scores_dict = {int(label): float(score) for (label, score) in zip(labels, scores)}

result = pd.DataFrame(np.column_stack([labels, scores]), columns=['Label', 'Score'])

result.to_csv('/tmp/test.csv', index=False)

# you want the final column of all_lateralised_gifs and the 'Gif Parcellations' too.
