import unittest
import pandas as pd
from mega_analysis.semiology import (
    semiology_dict_path,
    mega_analysis_df,
    all_semiology_terms,
)
from mega_analysis.semiology import QUERY_SEMIOLOGY


class TestQuerySemiology(unittest.TestCase):
    def query(self, data_frame, term):
        path = semiology_dict_path if term in all_semiology_terms else None
        inspect_result = QUERY_SEMIOLOGY(
            data_frame,
            semiology_term=term,
            semiology_dict_path=path,
        )
        return inspect_result

    def test_aphasia(self):
        inspect_result = self.query(mega_analysis_df, 'Aphasia')
        assert not inspect_result.empty

    def test_aphemia(self):
        inspect_result = self.query(mega_analysis_df, 'Aphemia')
        assert not inspect_result.empty

    def test_blink(self):
        inspect_result = self.query(mega_analysis_df, 'Blink')
        assert not inspect_result.empty

    def test_head_version(self):
        inspect_result = self.query(mega_analysis_df, 'Head version')
        assert not inspect_result.empty

    def test_figure_of_four(self):
        inspect_result = self.query(mega_analysis_df, 'Figure of 4')
        assert not inspect_result.empty

    def test_non_existing(self):
        inspect_result = self.query(mega_analysis_df, 'No semiology')
        assert inspect_result.empty
