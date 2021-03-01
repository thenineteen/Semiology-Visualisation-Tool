import sys
import unittest

import pandas as pd

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.gif_sheet_names import gif_sheet_names
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclude_paediatric_cases, exclusions, only_postictal_cases)
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.semiology import (  # semiology_dict_path,
    QUERY_LATERALISATION, QUERY_SEMIOLOGY, Laterality, Semiology, map_df_dict)
from mega_analysis.crosstab.mega_analysis.gifs_lat_factor import gifs_lat_factor
from mega_analysis.crosstab.mega_analysis.mapping import big_map


# define paths: note dummy data has a tab called test_counts
# a hand crafted test fixture count
repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = \
    file_paths(dummy_data=True)

# Define the gif sheet names
gif_sheet_names = gif_sheet_names()

# Read Excel file only three times at initialisation
test_df, _, _, _, _, _, _ = MEGA_ANALYSIS(
    excel_data=dummy_data_path,
    n_rows=100,
    usecols="A:DH",
    header=1,
    exclude_data=False,
    plot=True,
)

dummy_map_df_dict = pd.read_excel(
    dummy_data_path,
    header=1,
    sheet_name=gif_sheet_names,
    engine="openpyxl",
)

# dummy data one_map
one_map_dummy = big_map(map_df_dict=dummy_map_df_dict)


class TestDummyDataDummyDictionary(unittest.TestCase):
    """
    any tests/fixtures with gifs, rely on the mapping strategy used.
    Therefore these can be commented out or updated when mapping is updated.

    Note this uses the dummy data mapping not the live SemioBrain Database.
        to use dummy data mappings for top level query_lat, need to pass the argument
        map_df_dict=dummy_map_df_dict (previously) or after Profiling branch: just the already computed one_map=big_map(dummy_map_df_dict)
    Note also that the SemioDict is the live one unless specifically specified
        e.g. as an argument to QUERY_SEMIOLOGY(semiology_dict_path=dummy_semiology_dict_path)

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

        # not pd.testing.assert_frame_equal(self.df, exclusions(self.df))
        assert not self.df.equals(exclusions(self.df))
        # exclusions default is to exclude postictals and PETs only
        # print('\n1\n')

    def test_parenthesis_and_caps_QUERY_SEMIOLOGY_regex_pickup(self):
        """
        default QUERY_SEMIOLOGY doesn't exclude paed cases
        """
        query, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
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
        query, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
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
        query, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
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
        query, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
            self.df,
            # see dummy_SemioDict: equivalent to "Aphasia"
            semiology_term='dummy_test_link_aphasia',
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

    def test_toplevel_query_lat_mappings(self):
        """
        The call to the semiology_dictionary is the dummy_semio_dict as passed as an argument to q_l
        Relies on mapping strategy as uses gifs
        """

        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        all_combined_gifs = patient.query_lateralisation(
            one_map_dummy)

        self.assertIs(type(all_combined_gifs), pd.DataFrame)
        assert not all_combined_gifs.empty

        labels = ['Gif Parcellations', 'pt #s']
        all_combined_gifs = all_combined_gifs.astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        new_all_combined_gifindexed = all_combined_gifs.loc[:, labels]

        new_all_combined_gifindexed.set_index(
            'Gif Parcellations', inplace=True)

        # new_all_combined_gifindexed.to_csv(r'D:\aphasia_fixture.csv')
        # load fixture:
        fixture = pd.read_excel(
            dummy_data_path,
            header=0,
            usecols='A:B',
            sheet_name='fixture_aphasia',
            index_col=0,
            engine="openpyxl",
        )
        # fixture.sort_index(inplace=True)
        assert((new_all_combined_gifindexed.shape) == (fixture.shape))
#         print('new_all_combined_gifindexed.shape is: ',
#               new_all_combined_gifindexed.shape)
#         print('fixture.shape.shape is: ', fixture.shape)

        assert(new_all_combined_gifindexed.index == fixture.index).all()
        assert(new_all_combined_gifindexed.values == fixture.values).all()
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
        Test the NLB regex used in differentiating Tonic vs Asymmetric Tonic, atonic, generalised tonic, tonic-clonic etc in SemioDict.
        Note also that the SemioDict is the live one unless specifically specified:
            e.g. as an argument to QUERY_SEMIOLOGY(semiology_dict_path=dummy_semiology_dict_path=dummy_semiology_dict_path)
        """
        patient = Semiology('Tonic', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        tonic_result = patient.query_semiology()

        self.assertIs(type(tonic_result), pd.DataFrame)
        assert not tonic_result.empty
        assert(tonic_result['Localising'].sum() == 1+10)
        assert(tonic_result['Lateralising'].sum() == 1)

        # Now test for Atonic
        patient_two = Semiology(
            'Atonic', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient_two.data_frame = self.df
        atonic_result = patient_two.query_semiology()

        self.assertIs(type(atonic_result), pd.DataFrame)
        assert not atonic_result.empty
        assert(atonic_result['Localising'].sum() == 999)
        assert(atonic_result['Lateralising'].sum() == 2)

        print('\n9 negative lookbehind regex\n')

    def test_lat_not_loc_1(self):
        """
        Test capturing the lateralising but not localising data rather than skipping it.
        As implemented in QUERY_LATERALISATION in branch "Lateralising but no localising value".
        """
        patient = Semiology('lat_not_loc', Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df
        lat_not_loc_all_combined_gifs = patient.query_lateralisation(
            one_map_dummy)

        # inspect result
        lat_not_loc_result = patient.query_semiology()

        self.assertIs(type(lat_not_loc_all_combined_gifs), pd.DataFrame)
        assert not lat_not_loc_all_combined_gifs.empty

        # drop the zero entries as these are from the CL/IL zeros:
        lat_not_loc_all_combined_gifs = lat_not_loc_all_combined_gifs[['Gif Parcellations', 'pt #s']].astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        lat_not_loc_all_combined_gifs.set_index(
            'Gif Parcellations', inplace=True)
        lat_not_loc_gifsclean = lat_not_loc_all_combined_gifs.loc[
            lat_not_loc_all_combined_gifs['pt #s'] != 0, :]
        # now we know only the CL data remains in this dummy data, which is on the RIGHT.
        gifs_right, gifs_left = gifs_lat_factor()
        lat_not_loc_gifsclean_rights = (
            lat_not_loc_gifsclean.index.isin(gifs_right).all()
        )

        # inspect result assertions
        assert(lat_not_loc_result.Localising.sum() == 0)
        assert(lat_not_loc_result['Lateralising'].sum() == 1)

        # all_combined_gifs assertions
        assert((
            lat_not_loc_gifsclean_rights == True)
        )
        assert(
            (
                lat_not_loc_gifsclean.index.isin(gifs_left)).any() == False
        )
        assert (lat_not_loc_gifsclean['pt #s'].sum()
                == lat_not_loc_gifsclean.shape[0])

        # test MTG on right 155 gif # gives 1:
        heatmap, _ = patient.get_num_datapoints_dict(method='minmax')
        assert 156 not in heatmap  # left
        assert heatmap[155] == 1  # right

    def test_latnotloc_and_latandloc_2(self):
        """
        Test capturing the lateralising but not localising data rather than skipping it.
        integrated with lat and loc data.
        """
        patient = Semiology('lat_', Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df
        lat_not_loc_all_combined_gifs = patient.query_lateralisation(
            one_map_dummy)

        # inspect result
        lat_not_loc_result = patient.query_semiology()

        self.assertIs(type(lat_not_loc_all_combined_gifs), pd.DataFrame)
        assert not lat_not_loc_all_combined_gifs.empty

        # drop the zero entries - should be only the IL left ones which aren't MTG of TL:
        lat_not_loc_all_combined_gifs = lat_not_loc_all_combined_gifs[['Gif Parcellations', 'pt #s']].astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        lat_not_loc_all_combined_gifs.set_index(
            'Gif Parcellations', inplace=True)
        lat_not_loc_gifsclean = lat_not_loc_all_combined_gifs.loc[
            lat_not_loc_all_combined_gifs['pt #s'] != 0, :]

        gifs_right, gifs_left = gifs_lat_factor()
        lat_not_loc_gifsclean_rights = (
            lat_not_loc_gifsclean.drop(index=156).index.isin(gifs_right).all()
        )

        # inspect result assertions
        assert(lat_not_loc_result.Localising.sum() == 1)
        assert(lat_not_loc_result['Lateralising'].sum() == 2)

        # all_combined_gifs assertions
        # all except GIF 156 (L MTG) are in the right GIFs:
        assert((
            lat_not_loc_gifsclean_rights == True)
        )
        assert(
            (
                lat_not_loc_gifsclean.index.isin(gifs_left)).any() == True
        )
        # assert using shape as all pt #s are 1:
        assert (lat_not_loc_gifsclean['pt #s'].sum()
                == lat_not_loc_gifsclean.shape[0])

        # check that latnotloc gives 1 and latandloc adds zero to right MTG GIF #155
        heatmap, _ = patient.get_num_datapoints_dict(method='minmax')
        assert heatmap[155] == 1  # right

    def test_latexceedsloc_3(self):
        """
        Test capturing lateralisation value when it exceeds localising value (part1) and combining with lat_no_loc and lat_and_loc (part 2).
        Note that the default in Q_L of  normalise_lat_to_loc = False and using norm_ratio = lower_value / higher_value
            results in capping of lateralisation influence on data visualisation.

        In the specific case of latexceedsloc semiology, despite 500 lat cumulative datapoints and 2 localising points,
            the GIF results are:
            {155: 2.0, 156:1.0}
        """
        patient = Semiology('latexceedsloc', Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df

        # (part 1) test latexceedsloc alone using norm_ratio/oddsratio method of Q_L:
        heatmap, _ = patient.get_num_datapoints_dict(method='minmax')
        assert heatmap[156] == 200.0
        assert heatmap[155] == 300.0

        # (part 2) combine above with lat_not_loc and lat_and_loc:
        patient = Semiology('lat', Laterality.LEFT, Laterality.LEFT)
        patient.data_frame = self.df

        lat_allgifs = patient.query_lateralisation(
            one_map_dummy)

        # drop the zero entries - should be only the IL left ones which aren't MTG of TL:
        lat_allgifs = lat_allgifs[['Gif Parcellations', 'pt #s']].astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        lat_allgifs.set_index(
            'Gif Parcellations', inplace=True)
        lat_allgifs = lat_allgifs.loc[
            lat_allgifs['pt #s'] != 0, :]

        # assert using shape this not all are 1 so should not be the same:
        assert not lat_allgifs['pt #s'].sum() == lat_allgifs.shape[0]
        # check the MTG on the left (IL) GIF # 156 is == 3,
        #   which it isn't due to the norm_ratio method in Q_L - as can be seen from part 1
        #   so instead we see in part 1 156 was 1, but in the spreadsheet it was 2. so will give 2.
        #   3 is better but lost due to norm_ratio method in Q_L
        assert (lat_allgifs.loc[156, 'pt #s'] == 201)

        # for the right sided GIF, 155, latexceedsloc gives 2 [/],
        #   lat_not_loc gives 1 (CL) (See test_lat_not_loc_1)[/], and
        #   lat_and_loc adds none [/]
        assert (lat_allgifs.loc[155, 'pt #s'] == 301)

    def test_only_postictal_cases(self):
        """
        Include only the single postictal aphasia. Note Dominant in dummy data.
        cf test_postictal_exclusions
        """
        # Low level test
        df_postictal = only_postictal_cases(self.df)
        query, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
            df_postictal,
            semiology_term=['aphasia'],
            ignore_case=True,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category',
        )
        assert(query['Localising'].sum() == 1)
        assert(query['Lateralising'].sum() == 1)

        # High level test
        patient = Semiology('aphasia', Laterality.NEUTRAL,
                            dominant_hemisphere=Laterality.LEFT)
        patient.data_frame = self.df
        patient.include_postictals = True
        patient.include_only_postictals = True
        patient.granular = True

        lat_allgifs = patient.query_lateralisation(
            one_map_dummy)
        lat_allgifs = lat_allgifs[['Gif Parcellations', 'pt #s']].astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        lat_allgifs.set_index(
            'Gif Parcellations', inplace=True)

        # note that dominant_hemisphere == Laterality.LEFT as set above. Just to clarify results change if dominace changes. Also 1's become 2's if not granular.
        assert (lat_allgifs.loc[164, 'pt #s'] == 1)
        assert (lat_allgifs.loc[166, 'pt #s'] == 1)
        assert (lat_allgifs.loc[163, 'pt #s'] == 0)
        assert (lat_allgifs.loc[165, 'pt #s'] == 0)

        lat_allgifs = lat_allgifs.loc[lat_allgifs['pt #s'] != 0, :]
        SVT_output, _ = patient.get_num_datapoints_dict(method='minmax')
        assert SVT_output == dict((lat_allgifs)['pt #s'])


# for debugging with __init__():
# query = TestDummyDataDummyDictionary()
# query.test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary()
# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
