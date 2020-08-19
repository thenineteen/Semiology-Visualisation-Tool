import mega_analysis
from mega_analysis import Semiology, Laterality
from pathlib import Path

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS

file = Path(__file__).parent/'resources'/'semiologies_neutral_only.txt'
list_of_terms = list(open(file, 'r'))

# list_of_terms = ['Mimetic Automatisms',
#                  'No Semiology - Only Stimulation Studies',
#                  'Non-Specific Aura', 'Olfactory-Gustatory', 'Palilalia', 'Psychic', 'Spitting', 'Vestibular', 'Vocalisation', 'Whistling']

for term in list_of_terms:
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

        # 'latexceedsloc',
        # symptoms_side=Laterality.LEFT,
        # dominant_hemisphere=Laterality.LEFT,

        term.strip(),
        symptoms_side=Laterality.LEFT,
        dominant_hemisphere=Laterality.LEFT,
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

    heatmap = patient.get_num_datapoints_dict()
    print("\nSemiology: ", term)
    print('\nResult:', heatmap, '\n')
