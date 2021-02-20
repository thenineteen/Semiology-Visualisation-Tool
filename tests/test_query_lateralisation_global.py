import unittest
import sys
import pandas as pd
from mega_analysis.semiology import (
    semiology_dict_path,
    mega_analysis_df,
    all_semiology_terms,
    map_df_dict,
    gif_lat_file,
    Laterality,
    QUERY_SEMIOLOGY,
    QUERY_LATERALISATION,
    # melt_then_pivot_query,
    # pivot_result_to_one_map,
    Semiology,
)
from mega_analysis.crosstab.mega_analysis.mapping import big_map
from mega_analysis.crosstab.mega_analysis.QUERY_LATERALISATION_GLOBAL import QUERY_LATERALISATION_GLOBAL

one_map = big_map(map_df_dict)


class TestQueryLateralisation(unittest.TestCase):
    def query(self, term, symptoms_side, dominant_hemisphere):
        path = semiology_dict_path if term in all_semiology_terms else None
        query_semiology_result, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
            mega_analysis_df,
            semiology_term=term,
            semiology_dict_path=path,
        )
        if query_semiology_result is None:
            return None
        all_combined_gifs, num_QL_lat, num_QL_CL, num_QL_IL, num_QL_BL, num_QL_DomH, num_QL_NonDomH = QUERY_LATERALISATION_GLOBAL(
            term,
            query_semiology_result,
            mega_analysis_df,
            one_map,
            gif_lat_file,
            side_of_symptoms_signs=symptoms_side.value,
            pts_dominant_hemisphere_R_or_L=dominant_hemisphere.value,
        )
        return all_combined_gifs

    # def test_aphasia(self):
    #     all_combined_gifs = self.query(
    #         'Aphasia',
    #         Laterality.NEUTRAL,
    #         Laterality.LEFT,
    #     )
    #     assert not all_combined_gifs.empty

    def test_aphasia_neutral_neutral(self):
        all_combined_gifs = self.query(
            'Aphasia',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty

    # def test_aphemia(self):
    #     all_combined_gifs = self.query(
    #         'Aphemia',
    #         Laterality.NEUTRAL,
    #         Laterality.LEFT,
    #     )
    #     assert not all_combined_gifs.empty

    # def test_aphemia_neutral_dominant(self):
    #     all_combined_gifs = self.query(
    #         'Aphemia',
    #         Laterality.NEUTRAL,
    #         Laterality.NEUTRAL,
    #     )
    #     assert not all_combined_gifs.empty

    # def test_blink(self):
    #     all_combined_gifs = self.query(
    #         'Blink',
    #         Laterality.LEFT,
    #         Laterality.LEFT,
    #     )
    #     assert not all_combined_gifs.empty

    # def test_blink_neutral_side(self):
    #     all_combined_gifs = self.query(
    #         'Blink',
    #         Laterality.NEUTRAL,
    #         Laterality.LEFT,
    #     )
    #     assert not all_combined_gifs.empty

    # def test_blink_neutral_dominant(self):
    #     all_combined_gifs = self.query(
    #         'Blink',
    #         Laterality.LEFT,
    #         Laterality.NEUTRAL,
    #     )
    #     assert not all_combined_gifs.empty

    def test_head_version(self):
        all_combined_gifs = self.query(
            'Head Version',
            Laterality.LEFT,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_head_version_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Head Version',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty

    # def test_asymmetric_tonic(self):
    #     all_combined_gifs = self.query(
    #         'Asymmetric Tonic',
    #         Laterality.LEFT,
    #         Laterality.LEFT,
    #     )
    #     assert not all_combined_gifs.empty

    # def test_asymmetric_tonic_neutral_dominant(self):
    #     all_combined_gifs = self.query(
    #         'Asymmetric Tonic',
    #         Laterality.LEFT,
    #         Laterality.NEUTRAL,
    #     )
    #     assert not all_combined_gifs.empty


# for debugging with setUp(self):
if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
