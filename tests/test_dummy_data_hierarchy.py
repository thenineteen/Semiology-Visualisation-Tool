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
test_df, _, _, _, _, _, _ = MEGA_ANALYSIS(
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
        first tested postcode system which duplicates mapping
        before testing its reversal.

        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        # default behaviour of query_semiology changed to use granular hierarchy reversal:
        patient.granular = False
        inspect_result = patient.query_semiology()
        assert(inspect_result['TL'].sum() == 12)
        assert(inspect_result['Anterior (temporal pole)'].sum() == 5)
        assert(inspect_result['Lateral Temporal'].sum() == 4)
        assert(inspect_result['ITG'].sum() == 4)
        assert(inspect_result['Mesial Temporal'].sum() == 5)
        # # by default postictal are excluded. Otherwise add +1 to both below
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
        patient.granular = False
        inspect_result = patient.query_semiology()

        # # the three lines below were integrated into default query_semiology() using.granular = True
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

        # # note default is to exclude post ictals, otherwise add +1 to both below
        assert(inspect_result_reversed['FL'].sum() == 0)
        assert(inspect_result_reversed['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n9 frontal dictionary hierarchy reversal\n')

    def test_temporal_and_frontal_hierarchy_reversal(self):
        """
        test combined temporal and frontals
        """
        patient = Semiology('Aphasia', Laterality.NEUTRAL, Laterality.NEUTRAL)
        patient.data_frame = self.df
        patient.granular = False
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.temporal_hierarchy_reversal()  # deafult max option
        hierarchy_df.frontal_hierarchy_reversal()
        inspect_result_reversed = hierarchy_df.new_df

        assert hierarchy_df.frontal_hr.equals(hierarchy_df.new_df)
        assert inspect_result.all().all() == inspect_result_reversed.all().all()
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
        # these two lines should be +1 if not excluding postictals
        assert(inspect_result_reversed['FL'].sum() == 0)
        assert(inspect_result_reversed['IFG (F3)\n(BA 44,45,47)'].sum() == 1)
        print('\n11 all_hierarchy reversals\n')

    def use_SemioBrainBeta_notDummyData(self):
        """
        factor function.
        Uses the beta version callled syst_review_single_table.
        Note the arguments for MEGA_ANALYSIS differ for the beta version.
        """
        # load the Beta SemioBrain Database:
        repo_dir, resources_dir, SemioBrainBeta_data_path, SemioDict_path = \
            file_paths(dummy_data=False, Beta=True)
        SemioBrainBeta_df, _, _ = MEGA_ANALYSIS(
            excel_data=SemioBrainBeta_data_path,
            n_rows=2500,
            usecols="A:DH",
            header=1,
            exclude_data=False,
            plot=True,
        )
        return SemioBrainBeta_df

    def test_MappingsCalibration_HierarchyReversal_SemioBrainBeta_TLf(self):
        """
        Test the mappings TL for mapping calibration visualisation in the systReview (SemioBrain Database - beta version)
        i.e.  not dummy data
        """
        patient = Semiology(
            'mappings TLf', Laterality.NEUTRAL, Laterality.NEUTRAL)

        patient.data_frame = self.use_SemioBrainBeta_notDummyData()
        patient.granular = False
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.all_hierarchy_reversal()  # deafult max option
        inspect_result_reversed = hierarchy_df.new_df

        # test postcodes
        assert(inspect_result['TL'].sum() == 1)
        assert(inspect_result['Lateral Temporal'].sum() == 1)
        assert(
            inspect_result['STG (includes Transverse Temporal Gyrus, Both Planum)'].sum() == 1)
        assert(inspect_result['Planum Temporale'].sum() == 1)

        # test hierarchy reversal
        assert(inspect_result_reversed['TL'].sum() == 0)
        assert(inspect_result_reversed['Lateral Temporal'].sum() == 0)
        assert(
            inspect_result_reversed['STG (includes Transverse Temporal Gyrus, Both Planum)'].sum() == 0)
        assert(inspect_result_reversed['Planum Temporale'].sum() == 1)

    def test_MappingsCalibration_HierarchyReversal_SemioBrainBeta_TLd(self):
        """
        Test the mappings TL for mapping calibration visualisation in the systReview (SemioBrain Database - beta version)
        i.e.  not dummy data
        """
        patient = Semiology(
            'mappings TLd', Laterality.NEUTRAL, Laterality.NEUTRAL)

        patient.data_frame = self.use_SemioBrainBeta_notDummyData()
        patient.granular = False
        inspect_result = patient.query_semiology()

        hierarchy_df = Hierarchy(inspect_result)
        hierarchy_df.all_hierarchy_reversal()  # deafult max option
        inspect_result_reversed = hierarchy_df.new_df

        # test postcodes
        assert(inspect_result['TL'].sum() == 1)
        assert(inspect_result['Lateral Temporal'].sum() == 1)
        assert(
            inspect_result['STG (includes Transverse Temporal Gyrus, Both Planum)'].sum() == 1)
        assert 'Planum Temporale' not in inspect_result

        # test hierarchy reversal
        assert(inspect_result_reversed['TL'].sum() == 0)
        assert(inspect_result_reversed['Lateral Temporal'].sum() == 0)
        assert(
            inspect_result_reversed['STG (includes Transverse Temporal Gyrus, Both Planum)'].sum() == 1)
        assert 'Planum Temporale' not in inspect_result
        assert 'Planum Polare' not in inspect_result


# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
