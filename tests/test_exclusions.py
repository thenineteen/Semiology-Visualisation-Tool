import unittest
from mega_analysis.semiology import mega_analysis_df
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclusions,
    exclude_ET,
    exclude_sEEG_ES,
)


class TestExclusions(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()

    def test_default_no_exclusions(self):
        assert self.df.equals(exclusions(self.df))

    def test_exclusions(self):
        assert not self.df.equals(exclusions(self.df, CONCORDANCE=True))

    def test_exclude_et(self):
        assert not self.df.equals(exclude_ET(self.df))

    def test_exclude_seeg_es(self):
        assert not self.df.equals(exclude_sEEG_ES(self.df))
