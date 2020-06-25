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
from mega_analysis.crosstab.hierarchy_class import Hierarchy


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


class TestDummyDataHierarchyReversal(unittest.TestCase):
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

    def test_hierarchy(self):
        """
        first test postcode system which duplicates mapping
        before testing its reversal

        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()
        assert(inspect_result['TL'].sum() == 12)
        assert(inspect_result['Anterior (temporal pole)'].sum() == 5)
        assert(inspect_result['Lateral Temporal'].sum() == 4)
        assert(inspect_result['ITG'].sum() == 4)
        assert(inspect_result['Mesial Temporal'].sum() == 5)
        assert(inspect_result['FL'].sum() == 1)
        assert(inspect_result['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n7 hierarchy\n')

    def test_temporal_hierarchy_reversal(self):
        """
        now test reversal postcode system which duplicates mapping
        for new class Hierarchy
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.temporal_hierarchy_reversal()  # deafult max option
        inspect_result_reversed = hierarchy_df.temporal_hr

        assert(inspect_result_reversed['TL'].sum() == 3)
        assert(inspect_result_reversed['Anterior (temporal pole)'].sum() == 5)
        assert(inspect_result_reversed['Lateral Temporal'].sum() == 0)
        assert(inspect_result_reversed['ITG'].sum() == 4)
        assert(inspect_result_reversed['Mesial Temporal'].sum() == 5)
        print('\n8 temporal hierarchy reversal\n')

    def test_frontal_hierarchy_reversal(self):
        """
        continuing testing reversal of postcode system
        for new class Hierarchy
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.frontal_hierarchy_reversal()  # deafult max option
        inspect_result_reversed = hierarchy_df.frontal_hr

        assert(inspect_result_reversed['FL'].sum() == 0)
        assert(inspect_result_reversed['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n9 frontal dictionary hierarchy reversal\n')

    def test_temporal_and_frontal_hierarchy_reversal(self):
        """
        test combined temporal and frontals
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.temporal_hierarchy_reversal()  # deafult max option
        hierarchy_df.frontal_hierarchy_reversal()
        inspect_result_reversed = hierarchy_df.new_df

        assert hierarchy_df.frontal_hr.equals(hierarchy_df.new_df)
        assert not hierarchy_df.temporal_hr.equals(hierarchy_df.new_df)
        # ^ because self.new_df.copy() in the Hierarchy.temporal_hierarchy_reversal() method, so order matters.
        assert(inspect_result_reversed['TL'].sum() == 3)
        assert(inspect_result_reversed['Anterior (temporal pole)'].sum() == 5)
        assert(inspect_result_reversed['Lateral Temporal'].sum() == 0)
        assert(inspect_result_reversed['ITG'].sum() == 4)
        assert(inspect_result_reversed['Mesial Temporal'].sum() == 5)
        assert(inspect_result_reversed['FL'].sum() == 0)
        assert(inspect_result_reversed['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n10 combined T & F hierarchy reversals\n')

    def test_all_hierarchy_reversals(self):
        """
        test all.
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.all_hierarchy_reversal()  # deafult max option
        inspect_result_reversed = hierarchy_df.new_df

        # assert object doesn't have any _hr aatribute:
        assert not hasattr(hierarchy_df, 'temporal_hr')
        assert(inspect_result_reversed['TL'].sum() == 3)
        assert(inspect_result_reversed['Anterior (temporal pole)'].sum() == 5)
        assert(inspect_result_reversed['Lateral Temporal'].sum() == 0)
        assert(inspect_result_reversed['ITG'].sum() == 4)
        assert(inspect_result_reversed['Mesial Temporal'].sum() == 5)
        assert(inspect_result_reversed['FL'].sum() == 0)
        assert(inspect_result_reversed['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n11 all_hierarchy reversals\n')


# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
