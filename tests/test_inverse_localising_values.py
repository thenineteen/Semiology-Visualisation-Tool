import sys
import unittest

import pandas as pd

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.gif_sheet_names import gif_sheet_names
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclude_cortical_stimulation, exclude_ET, exclude_paediatric_cases,
    exclude_postictals, exclude_sEEG, exclude_seizure_free,
    exclude_spontaneous_semiology, exclusions)
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.semiology import (  # semiology_dict_path,
    QUERY_LATERALISATION, QUERY_SEMIOLOGY, Laterality, Semiology,
    all_semiology_terms, gif_lat_file, map_df_dict, mega_analysis_df,
    melt_then_pivot_query, pivot_result_to_one_map)
from mega_analysis.crosstab.mega_analysis.gifs_lat_factor import gifs_lat_factor


# define paths: note dummy data has a tab called test_counts
# a hand crafted test fixture count
repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = \
    file_paths(dummy_data=True)

# Define the gif sheet names
gif_sheet_names = gif_sheet_names()

# Read Excel for the dummy database
test_df, _, _, _, _, _, _ = MEGA_ANALYSIS(
    excel_data=dummy_data_path,
    n_rows=100,
    usecols="A:DH",
    header=1,
    exclude_data=False,
    plot=True,
)

# read excel for the dummy mappings
dummy_map_df_dict = pd.read_excel(
    dummy_data_path,
    header=1,
    sheet_name=gif_sheet_names
)


class InverseLocalisingValues(unittest.TestCase):
    """


    for debugging run as such (at end of file) if def __init__(self):
        query = TestDummyDataDummyDictionary()
        query.test_default_no_exclusions()
    Otherwise:
        if __name__ == '__main__':
            sys.argv.insert(1, '--verbose')
            unittest.main(argv=sys.argv)
    """

    def setUp(self):
        self.df = test_df.copy()
        print('setup')

    def test_dummy_data_ILV_1(self):
        """
        Test the method of inverse-localising-value as per issues #169 on GitHub.
        This uses "IVL_1" as semiology term, which is the same as Example 1 on GitHub:
        https://github.com/thenineteen/Semiology-Visualisation-Tool/issues/169

        """
        patient = Semiology('ILV_1',
                            Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 1)
        assert(inspect_result['Lateralising'].sum() == 0)

    def test_dummy_data_ILV_control(self):
        """
        Test the method of inverse-localising-value as per issues #169 on GitHub.
        This uses "ILV_4" as semiology term, which is Example 2 on GitHub:
        https://github.com/thenineteen/Semiology-Visualisation-Tool/issues/169

        """
        patient = Semiology('ILV_4',
                            Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 4)
        assert(inspect_result['Lateralising'].sum() == 0)

    def factor_ql(self, term):
        patient = Semiology(term,
                            Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df
        all_combined_gifs = patient.query_lateralisation(
            map_df_dict=dummy_map_df_dict)

        return all_combined_gifs

    def test_NotILV_default(self):
        """
        SVT default behaviour (v 1.3.1) is that Example 1 (singlept) and 2 (fourpts) return the same result.
        Test the method of inverse-localising-value as per issues #169 on GitHub.
        https://github.com/thenineteen/Semiology-Visualisation-Tool/issues/169

        """
        all_combined_gifs_singlept = self.factor_ql('ILV_1')
        all_combined_gifs_fourpts = self.factor_ql('ILV_4')

        self.assertIs(type(all_combined_gifs_singlept), pd.DataFrame)
        assert not all_combined_gifs_singlept.empty
        self.assertIs(type(all_combined_gifs_fourpts), pd.DataFrame)
        assert not all_combined_gifs_fourpts.empty

        assert all_combined_gifs_singlept.shape == all_combined_gifs_fourpts.shape
        assert all_combined_gifs_singlept.all().all(
        ) == all_combined_gifs_fourpts.all().all()


    # for debugging with __init__():
    # query = TestDummyDataDummyDictionary()
    # query.test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary()
    # for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
