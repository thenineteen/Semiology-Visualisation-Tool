import unittest
import pandas as pd
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from resources.file_paths import file_paths
from mega_analysis.semiology import (
    semiology_dict_path,
    mega_analysis_df,
    all_semiology_terms,
    map_df_dict,
    gif_lat_file,
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

repo_dir, resources_dir, dummy_data_path, dummy_semiology_dict_path = file_paths()

test_df, _, _ = MEGA_ANALYSIS(excel_data=dummy_data_path)
map_df_dict = pd.read_excel(
    excel_path,
    header=1,
    sheet_name=gif_sheet_names
)
gif_lat_file = pd.read_excel(
    excel_path,
    header=0,
    sheet_name='Full GIF Map for Review '
)

class TestExclusions(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()