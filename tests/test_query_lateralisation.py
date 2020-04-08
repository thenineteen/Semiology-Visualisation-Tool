import unittest
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
    melt_then_pivot_query,
    pivot_result_to_one_map,
)


class TestQueryLateralisation(unittest.TestCase):
    def query(self, term, symptoms_side, dominant_hemisphere):
        path = semiology_dict_path if term in all_semiology_terms else None
        query_semiology_result = QUERY_SEMIOLOGY(
            mega_analysis_df,
            semiology_term=term,
            semiology_dict_path=path,
        )
        all_combined_gifs = QUERY_LATERALISATION(
            query_semiology_result,
            mega_analysis_df,
            map_df_dict,
            gif_lat_file,
            side_of_symptoms_signs=symptoms_side.value,
            pts_dominant_hemisphere_R_or_L=dominant_hemisphere.value,
        )
        if all_combined_gifs is None:
            pivot_result = melt_then_pivot_query(
                mega_analysis_df,
                query_semiology_result,
                term,
            )
            all_combined_gifs = pivot_result_to_one_map(
                pivot_result,
                suppress_prints=True,
                map_df_dict=map_df_dict,
            )
        return all_combined_gifs

    def test_aphasia(self):
        all_combined_gifs = self.query(
            'Aphasia',
            Laterality.NEUTRAL,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_aphasia_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Aphasia',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty


    def test_aphemia(self):
        all_combined_gifs = self.query(
            'Aphemia',
            Laterality.NEUTRAL,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_aphemia_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Aphemia',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty


    def test_blink(self):
        all_combined_gifs = self.query(
            'Blink',
            Laterality.LEFT,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_blink_neutral_side(self):
        all_combined_gifs = self.query(
            'Blink',
            Laterality.NEUTRAL,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_blink_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Blink',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty


    def test_head_version(self):
        all_combined_gifs = self.query(
            'Head version',
            Laterality.LEFT,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_head_version_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Head version',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty


    def test_figure_of_four(self):
        all_combined_gifs = self.query(
            'Figure of 4',
            Laterality.LEFT,
            Laterality.LEFT,
        )
        assert not all_combined_gifs.empty

    def test_figure_of_four_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Figure of 4',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert not all_combined_gifs.empty


    def test_non_existing(self):
        all_combined_gifs = self.query(
            'Non existing',
            Laterality.LEFT,
            Laterality.LEFT,
        )
        assert all_combined_gifs.empty

    def test_non_existing_neutral_dominant(self):
        all_combined_gifs = self.query(
            'Non existing',
            Laterality.NEUTRAL,
            Laterality.NEUTRAL,
        )
        assert all_combined_gifs.empty
