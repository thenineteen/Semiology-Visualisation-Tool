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

# define paths: note dummy data has a tab called test_counts
# a hand crafted test fixture count
repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = \
    file_paths(dummy_data=True)

# Define the gif sheet names
gif_sheet_names = gif_sheet_names()

# Read Excel file only three times at initialisation
test_df, _, _ = MEGA_ANALYSIS(
    excel_data=dummy_data_path,
    n_rows=100,
    usecols="A:DH",
    header=1,
    exclude_data=False,
    plot=True,
)

map_df_dict = pd.read_excel(
    dummy_data_path,
    header=1,
    sheet_name=gif_sheet_names
)
gif_lat_file = pd.read_excel(
    dummy_data_path,
    header=0,
    sheet_name='Full GIF Map for Review '
)


class TestDummyDataDummyDictionary(unittest.TestCase):
    """
    any tests/fixtures with gifs, rely on the mapping strategy used.
    Therefore these can be commented out or updated when mapping is updated.

    Note this uses the dummy data mapping not the live SemioBrain Database.
    Note also that the SemioDict is the live one unless specifically specified
        e.g. as an argument to QUERY_SEMIOLOGY(semiology_dict_path=dummy_semiology_dict_path=dummy_semiology_dict_path)

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

    def test_default_vs_exclusions(self):
        # self.df.to_csv(r'D:\self_df.csv')
        # exclusions(self.df).to_csv(r'D:\self_df_exclusions.csv')

        not pd.testing.assert_frame_equal(self.df, exclusions(self.df))
        # assert not self.df.equals(exclusions(self.df))
        # exclusions default is to exclude postictals and PETs only
        # print('\n1\n')

    def test_parenthesis_and_caps_QUERY_SEMIOLOGY_regex_pickup(self):
        """
        default QUERY_SEMIOLOGY doesn't exclude paed cases
        """
        query = QUERY_SEMIOLOGY(
            self.df,
            semiology_term=['aphasia'],
            ignore_case=True,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category',
        )
        assert(query['Localising'].sum() == 14)
        assert(query['Lateralising'].sum() == 6)
        # print('\n2\n')

    def test_postictal_exclusion(self):
        """
        Exclude the single postictal aphasia.
        After update in June, default is to exclude postictals.
        So the result of this should be the same as query_semiology()
        """
        df_excl = exclusions(self.df)
        query = QUERY_SEMIOLOGY(
            df_excl,
            semiology_term=['aphasia'],
            ignore_case=True,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category',
        )
        assert(query['Localising'].sum() == 13)
        assert(query['Lateralising'].sum() == 5)
        print('\n2.2 postictal\n')

    def test_caps_QUERY_SEMIOLOGY_regex_pickup(self):
        """
        when ignore case is false, it won't pick up case mismatches.
        so sum is slightly less.
        """
        query = QUERY_SEMIOLOGY(
            self.df,
            semiology_term=['aphasia'],
            ignore_case=False,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category',
        )
        assert(query['Localising'].sum() == 13)
        assert(query['Lateralising'].sum() == 6)
        # print('\n3\n')

    def test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary(self):
        query = QUERY_SEMIOLOGY(
            self.df,
            semiology_term='aphasia',
            ignore_case=False,
            # in QUERY_SEMIO re.IGNORECASE is used for dictionary anyway
            semiology_dict_path=dummy_semiology_dict_path,
            col1='Reported Semiology',
            col2='Semiology Category',
        )
        assert(query['Localising'].sum() == 14)
        assert(query['Lateralising'].sum() == 6)
        # print('\n4\n')

    def test_toplevel_aphasia_parentheses_and_caps(self):
        """
        test query_semiology which calls QUERY_SEMIOLOGY
        Need to change the call to the semiology_dictionary to
            make it the dummy_semio_dict
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        # deafult excludes postictals
        assert(inspect_result['Localising'].sum() == 14-1)
        assert(inspect_result['Lateralising'].sum() == 6-1)
        # print('\n5\n')

    def test_toplevel_query_lat(self):
        """
        Need to change the call to the semiology_dictionary to
            make it the dummy_semio_dict
        Relies on mapping strategy as uses gifs
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        all_combined_gifs = patient.query_lateralisation()

        self.assertIs(type(all_combined_gifs), pd.DataFrame)
        assert not all_combined_gifs.empty

        labels = ['Gif Parcellations', 'pt #s']
        all_combined_gifs = all_combined_gifs.astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        new_all_combined_gifindexed = all_combined_gifs.loc[:, labels]

        new_all_combined_gifindexed.set_index(
            'Gif Parcellations', inplace=True)

        # load fixture:
        fixture = pd.read_excel(
            dummy_data_path,
            header=0,
            usecols='A:B',
            sheet_name='fixture_aphasia',
            index_col=0,
        )
        # fixture.sort_index(inplace=True)
        # new_all_combined_gifindexed.to_csv(r'D:\fixture_aphasia.csv')
        assert((new_all_combined_gifindexed.shape) == (fixture.shape))
#         print('new_all_combined_gifindexed.shape is: ',
#               new_all_combined_gifindexed.shape)
#         print('fixture.shape.shape is: ', fixture.shape)

        assert(new_all_combined_gifindexed.index.all() == fixture.index.all())
        assert(
            new_all_combined_gifindexed.values.all() == fixture.values.all())
#         print('\n6 query lat\n')

    def test_paed_default_query_semio(self):
        """
        Test query_semiology for excluding paediatric cases.
        This test now shows that default query_semiology() DOES filter paediatric cases.

        """
        patient = Semiology('spasm', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        # revert default paed exclusions
        patient.include_only_paediatric_cases = True
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 10)
        assert(inspect_result['Lateralising'].sum() == 0)
        print('\n7 paed query_semio()\n')

    def test_paed_exclusions_query_semio(self):
        """
        Test query_semiology then exclude paediatric cases.
        """
        patient = Semiology('spasm', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()
        inspect_result = exclude_paediatric_cases(inspect_result)

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 5+1)
        assert(inspect_result['Lateralising'].sum() == 0)
        print('\n8 paed exclusions query_semio()\n')

    def test_NegativeLookBehind_Regex(self):
        """
        Test the NLB regex used in differentiating Tonic vs Asymmetric Tonic, atonic, generalised tonic, tonic-clonic etc in SemioDict .
        """
        patient = Semiology('Tonic', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 1+10)
        assert(inspect_result['Lateralising'].sum() == 1)
        print('\n9 negative lookbehind regex\n')

# for debugging with __init__():
# query = TestDummyDataDummyDictionary()
# query.test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary()


# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
