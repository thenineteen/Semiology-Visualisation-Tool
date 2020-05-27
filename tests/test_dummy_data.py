import unittest
import pandas as pd
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from resources.file_paths import file_paths
from resources.gif_sheet_names import gif_sheet_names
from mega_analysis.semiology import (
    semiology_dict_path,
    mega_analysis_df,
    all_semiology_terms,
    map_df_dict,
    gif_lat_file,
    Semiology,
    Laterality,
    QUERY_SEMIOLOGY,
    QUERY_LATERALISATION,
    melt_then_pivot_query,
    pivot_result_to_one_map,
)
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclude_postictals,
    exclusions,
    exclude_ET,
    exclude_spontaneous_semiology,
    exclude_cortical_stimulation,
    exclude_sEEG,
    exclude_seizure_free,
    exclude_paediatric_cases,
)

# define paths: note dummy data has a tab called test_counts as a hand crafted test fixture count
repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = file_paths(dummy_data=True)

# Define the gif sheet names
gif_sheet_names = gif_sheet_names()

# Read Excel file only three times at initialisation
test_df, _, _ = MEGA_ANALYSIS(
    excel_data=dummy_data_path,
    n_rows = 100,
    usecols = "A:DH",
    header = 1,
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
    for debugging run as such (at end of file):
        query = TestDummyDataDummyDictionary()
        query.test_default_no_exclusions()
    """
    def __init__(self):
        self.df = test_df.copy()

    def test_default_vs_exclusions(self):
        assert not self.df.equals(exclusions(self.df))
            # exclusions default is to exclude postictals and PETs only

    def test_parenthesis_and_caps_QUERY_SEMIOLOGY_regex_pickup(self):
        query = QUERY_SEMIOLOGY(
            self.df,
            semiology_term=['aphasia'],
            ignore_case=True,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category'
            )
        print(query['Localising'].sum() == 13)
        print(query['Lateralising'].sum() == 6)

    def test_caps_QUERY_SEMIOLOGY_regex_pickup(self):
        query = QUERY_SEMIOLOGY(
            self.df,
            semiology_term=['aphasia'],
            ignore_case=False,
            semiology_dict_path=None,
            col1='Reported Semiology',
            col2='Semiology Category'
            )
        print(query['Localising'].sum() == 12)
        print(query['Lateralising'].sum() == 6)

# for debugging:
query = TestDummyDataDummyDictionary()
query.test_caps_QUERY_SEMIOLOGY_regex_pickup()