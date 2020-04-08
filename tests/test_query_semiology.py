import unittest
import pandas as pd
from mega_analysis.semiology import (
    semiology_dict_path,
    mega_analysis_df,
    all_semiology_terms,
)
from mega_analysis.semiology import QUERY_SEMIOLOGY


class TestQuerySemiology(unittest.TestCase):
    def query(self, term):
        path = semiology_dict_path if term in all_semiology_terms else None
        inspect_result = QUERY_SEMIOLOGY(
            mega_analysis_df,
            semiology_term=term,
            semiology_dict_path=path,
        )
        return inspect_result

    def test_aphasia(self):
        inspect_result = self.query('Aphasia')
        self.assertIs(type(inspect_result), pd.DataFrame)

    def test_aphemia(self):
        inspect_result = self.query('Aphemia')
        self.assertIs(type(inspect_result), pd.DataFrame)

    def test_blink(self):
        inspect_result = self.query('Blink')
        self.assertIs(type(inspect_result), pd.DataFrame)

    def test_head_version(self):
        inspect_result = self.query('Head version')
        self.assertIs(type(inspect_result), pd.DataFrame)

    def test_figure_of_four(self):
        inspect_result = self.query('Figure of 4')
        self.assertIs(type(inspect_result), pd.DataFrame)

    def test_non_existing(self):
        inspect_result = self.query('No semiology')
        self.assertIs(type(inspect_result), pd.DataFrame)
