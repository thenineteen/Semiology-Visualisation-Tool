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

# define paths
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
    def setUp(self):
        self.df = test_df.copy()

    def test_default_no_exclusions(self):
        assert self.df.equals(exclusions(self.df))