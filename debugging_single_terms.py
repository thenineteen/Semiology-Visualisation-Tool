import mega_analysis
from mega_analysis import Semiology, Laterality

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.semiology import get_df_from_semiologies, combine_semiologies


patient = Semiology(
    # 'Figure of 4',
    # symptoms_side=Laterality.LEFT,
    # dominant_hemisphere=Laterality.LEFT,

    # 'Blink',
    # Laterality.NEUTRAL,
    # Laterality.LEFT,

    # 'All Automatisms (oral, automotor)',
    # Laterality.LEFT,
    # Laterality.LEFT,

    # 'Grimace', Laterality.NEUTRAL, Laterality.NEUTRAL,

    # 'latexceedsloc',  # switch to dummy data
    # symptoms_side=Laterality.LEFT,
    # dominant_hemisphere=Laterality.LEFT,

    'Head Version',
    symptoms_side=Laterality.LEFT,
    dominant_hemisphere=Laterality.NEUTRAL,
    normalise_to_localising_values=True,  # default is False
)
patient2 = Semiology(
    'Epigastric',
    symptoms_side=Laterality.LEFT,
    dominant_hemisphere=Laterality.NEUTRAL,
    normalise_to_localising_values=True,  # default is False
)
###
##
# # if we want to use the dummy_data instead of real Semio2Brain DataFrame:
# repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = \
#     file_paths(dummy_data=True)

# patient.data_frame, _, _ = MEGA_ANALYSIS(
#     excel_data=dummy_data_path,
#     n_rows=100,
#     usecols="A:DH",
#     header=1,
#     exclude_data=False,
#     plot=True,
# )
#
##
###

###
##
# # if we want to set top_level_lobes to True:
# patient.granular = False
# patient.top_level_lobes = True

# num_datapoints_dict_Bayesian = patient.get_num_datapoints_dict(method='Bayesian only')
# df_Bayesian = get_df_from_semiologies([patient], method='Bayesian only')

num_datapoints_dict_proportions = patient.get_num_datapoints_dict(method='proportions')
df_proportions, all_combind_gif_df = get_df_from_semiologies([patient], method='proportions')
combined_df = combine_semiologies([patient, patient2], normalise_method='proportions')

print("\nSemiology: ", patient.term)
print('\nResult:', heatmap, '\n')
