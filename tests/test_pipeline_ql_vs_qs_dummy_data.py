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
test_df, _, _ = MEGA_ANALYSIS(
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


class PipelineSequenceTesting(unittest.TestCase):
    """
    any tests/fixtures with gifs, rely on the mapping strategy used.
    Therefore these can be commented out or updated when mapping is updated.

    Note this uses the dummy data mapping not the live SemioBrain Database.
        to use dummy data mappings for top level query_lat, need to pass the argument
        map_df_dict=dummy_map_df_dict
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

    def test_prelim1_qs_lateralises(self):
        """
        Pipeline sequence testing of dummy data: lateralises.
        This test is a standalone to ensure qs/QS find the dummy semiology.

        Test query_semiology which calls QUERY_SEMIOLOGY.
        The call to the semiology_dictionary is the dummy_semio_dict.
        """
        patient = Semiology('pipeline_laateralises_semioA',
                            Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 10)
        assert(inspect_result['Lateralising'].sum() == 9)

    def test_prelim2_qs_doesnot_lateralise(self):
        """
        Pipeline sequence testing of dummy data: does not lateralise.
        This is a standalone test to ensure qs/QS find dummy semiology.

        Test query_semiology which calls QUERY_SEMIOLOGY.
        The call to the semiology_dictionary is the dummy_semio_dict.
        """
        patient = Semiology('pipeline_notlaat_semioB',
                            Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert(inspect_result['Localising'].sum() == 10)
        assert(inspect_result['Lateralising'].sum() == 0)

    def test_prelim3_ql_lateralises(self):
        """
        Pipeline sequence test of ql: lateralises
        The call to the semiology_dictionary is the dummy_semio_dict as passed as an argument to q_l.
        Relies on mapping strategy as uses gifs.
        """
        patient = Semiology('pipeline_laateralises_semioA',
                            Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df

        # returns the results from Q_L pipeline
        all_combined_gifs = patient.query_lateralisation(
            map_df_dict=dummy_map_df_dict)

        self.assertIs(type(all_combined_gifs), pd.DataFrame)
        assert not all_combined_gifs.empty
        return all_combined_gifs

    def test_prelim4_ql_doesnot_lateralise(self):
        """
        """
        patient = Semiology('pipeline_notlaat_semioB',
                            Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df

        # as no lateralising data, the below will run a manual pipeline
        # involving melt_then_pivot_query and pivot_result_to_one_map:
        all_combined_gifs = patient.query_lateralisation(
            map_df_dict=dummy_map_df_dict)

        self.assertIs(type(all_combined_gifs), pd.DataFrame)
        assert not all_combined_gifs.empty
        return all_combined_gifs

    def test_compare_pipelines1(self):
        """
        Compares query_lateralisation() with and without lateralising data.
        The GIF numbers should be the same (as the lateralising one is 90% CL and 10% IL so no GIFs are removed).
        The IL GIFs will have lower values.
        """
        QL_lateralising_PipelineResult = self.test_prelim3_ql_lateralises()
        QS_nonlat_ManualPipelineResult = self.test_prelim4_ql_doesnot_lateralise()

        # shapes are the same
        assert (QL_lateralising_PipelineResult.shape) == (
            QS_nonlat_ManualPipelineResult.shape)

        # GIFs should be the same
        QL_lateralising_PipelineResult = QL_lateralising_PipelineResult.astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        QS_nonlat_ManualPipelineResult = QS_nonlat_ManualPipelineResult.astype(
            {'Gif Parcellations': 'int32', 'pt #s': 'int32'})
        GIF_parcellations = QL_lateralising_PipelineResult[
            'Gif Parcellations'].all() == QS_nonlat_ManualPipelineResult['Gif Parcellations'].all()
        assert GIF_parcellations

    # for debugging with __init__():
    # query = TestDummyDataDummyDictionary()
    # query.test_parenthesis_and_caps_QUERY_SEMIOLOGY_with_dictionary()
    # for debugging with setUp(self):


if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
