import unittest
import sys

from mega_analysis import Semiology, Laterality
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.semiology import get_df_from_semiologies, combine_semiologies


class CombineSemiolgies(unittest.TestCase):
    """
    Test probabilities of all gifs per semiology add up to 1 before combining semiologies using proportions.
    """

    def test_combine_semiologies_proportions_sum_to_1(self):
        patient = Semiology(
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
        ##
        ###
        ###
        ##
        # # if we want to set top_level_lobes to True:
        # patient.granular = False
        # patient.top_level_lobes = True

        df, all_combined_gif_df = combine_semiologies([patient, patient2], normalise_method='proportions')

        assert (df.sum(axis=1)).all() == 1



# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)



