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
        return path, inspect_result

    def test_aphasia(self):
        path, inspect_result = self.query('Aphasia')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert path is not None

    def test_aphemia(self):
        path, inspect_result = self.query('Aphemia')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert path is not None

    def test_blink(self):
        path, inspect_result = self.query('Blink')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert path is not None

    def test_non_existing_semio(self):
        path, inspect_result = self.query('enja hichi nist')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert inspect_result.empty
        assert path is None

    def test_head_version(self):
        # Head version here has a lower case v so won't find in semio_dict
        path, inspect_result = self.query('Head version')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert path is None

    def test_head_version(self):
        # Head Version here has an upper case v so WILL find it in semio_dict
        path, inspect_result = self.query('Head Version')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert not inspect_result.empty
        assert path is not None

    def test_non_existing_path(self):
        path, inspect_result = self.query('love')
        self.assertIs(type(inspect_result), pd.DataFrame)
        assert ~inspect_result.empty
        assert path is None
