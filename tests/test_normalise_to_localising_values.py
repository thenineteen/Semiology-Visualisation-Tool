import sys
import unittest

import pandas as pd

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.gif_sheet_names import gif_sheet_names
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.semiology import (  # semiology_dict_path,
    QUERY_LATERALISATION, QUERY_SEMIOLOGY, Laterality, Semiology,
    map_df_dict)
from mega_analysis.crosstab.mega_analysis.mapping import pivot_result_to_one_map, big_map


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
    sheet_name=gif_sheet_names,
    engine="openpyxl",
)

one_map_dummy = big_map(dummy_map_df_dict)


class NormaliseLocalisingValues(unittest.TestCase):
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

    def test_prelim1_dummy_ILV_1(self):
        """
        Preliminary test as per issues #169 on GitHub.
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

    def test_prelim2_dummy_ILV_control(self):
        """
        Preliminary test as per issues #169 on GitHub.
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

    def factor_ql(self, term, normalise_to_localising_values=False):
        """
        factor function.
        NB normalise_to_localising_values default is False in semiology.py
        """
        patient = Semiology(term,
                            Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df

        patient.normalise_to_localising_values = normalise_to_localising_values

        all_combined_gifs = patient.query_lateralisation(
            one_map_dummy)

        return all_combined_gifs

    def test_NotILV_default(self):
        """
        SVT default behaviour (v 1.3.1) is that Example 1 (singlept) and 2 (fourpts) return the same result.
        As per issues #169 on GitHub.
        https://github.com/thenineteen/Semiology-Visualisation-Tool/issues/169

        """
        all_combined_gifs_singlept = self.factor_ql('ILV_1')
        all_combined_gifs_fourpts = self.factor_ql('ILV_4')

        self.assertIs(type(all_combined_gifs_singlept), pd.DataFrame)
        assert not all_combined_gifs_singlept.empty
        self.assertIs(type(all_combined_gifs_fourpts), pd.DataFrame)
        assert not all_combined_gifs_fourpts.empty

        assert all_combined_gifs_singlept.shape == all_combined_gifs_fourpts.shape

        all_combined_gifs_singlept.drop(columns='Semiology Term', inplace=True)
        all_combined_gifs_fourpts.drop(columns='Semiology Term', inplace=True)
        assert (all_combined_gifs_singlept ==
                all_combined_gifs_fourpts).all().all()

    def test_ILV_function_doesnt_change_ratio1(self):
        """
        In Example 2 (4pts), the use of normalise_to_localising_values should make no difference.
        """
        fourptsILV_gifs = self.factor_ql(
            'ILV_4', normalise_to_localising_values=True)

        fourpts_gifs = self.factor_ql(
            'ILV_4', normalise_to_localising_values=False)

        assert fourptsILV_gifs.shape == fourpts_gifs.shape

        # Semiology Term contains NaNs which complicates assertions
        fourptsILV_gifs.drop(columns='Semiology Term', inplace=True)
        fourpts_gifs.drop(columns='Semiology Term', inplace=True)
        assert (fourptsILV_gifs == fourpts_gifs).all().all()

    def test_normalise_toLocalisingValues_function(self):
        """
        Test the method of normalising-to-localising-value as per issues #169 on GitHub.
        Example 1 should return 0.25 for each localisation GIF, whereas Example 2 should remain the same.
        https://github.com/thenineteen/Semiology-Visualisation-Tool/issues/169

        """
        # set normalise_to_localising_values=True
        all_combined_gifs_singlept = self.factor_ql(
            'ILV_1', normalise_to_localising_values=True)
        all_combined_gifs_fourpts = self.factor_ql(
            'ILV_4', normalise_to_localising_values=True)

        # basic baseline control assertions
        self.assertIs(type(all_combined_gifs_singlept), pd.DataFrame)
        assert not all_combined_gifs_singlept.empty
        self.assertIs(type(all_combined_gifs_fourpts), pd.DataFrame)
        assert not all_combined_gifs_fourpts.empty

        # shapes remain the same as GIFs are the same
        assert all_combined_gifs_singlept.shape == all_combined_gifs_fourpts.shape

        # DataFrames (values) are no longer the same
        all_combined_gifs_singlept.drop(columns='Semiology Term', inplace=True)
        all_combined_gifs_fourpts.drop(columns='Semiology Term', inplace=True)
        thesame = (all_combined_gifs_singlept ==
                   all_combined_gifs_fourpts).all().all()
        assert not thesame

        # Specifically, Gif parecellations are the same...:
        assert (all_combined_gifs_singlept['Gif Parcellations'] ==
                all_combined_gifs_fourpts['Gif Parcellations']).all()

        # ... but values of pt #s are NO longer the same:
        assert not (all_combined_gifs_singlept['pt #s'] ==
                    all_combined_gifs_fourpts['pt #s']).all()

        # and finally ensure the values are either 1/4 = 0.25 or 0:
        # can't use sum()==1 as mappings can make sum more than 1 here for singlept
        # assert all_combined_gifs_singlept['pt #s'].sum() > 0
        assert (all_combined_gifs_singlept['pt #s'].unique() ==
                [0, 0.25]).all()

    # for debugging with __init__():
    # query = TestDummyDataDummyDictionary()
    # query.test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary()
    # for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
