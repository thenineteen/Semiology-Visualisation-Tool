import unittest
from mega_analysis.semiology import mega_analysis_df
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclusions,
    exclude_ET,
    exclude_sEEG,
    exclude_cortical_stimulation,
    exclude_seizure_free,
)


class TestExclusions(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()

    def test_default_no_exclusions(self):
        assert self.df.equals(exclusions(self.df))

    def test_exclude_concordance(self):
        assert not self.df.equals(exclusions(self.df, CONCORDANCE=True))

    def test_exclude_seizure_freedom(self):
        assert not self.df.equals(exclude_seizure_free(self.df))

    def test_exclude_et(self):
        assert not self.df.equals(exclude_ET(self.df))

    def test_exclude_seeg(self):
        assert not self.df.equals(exclude_sEEG(self.df))

    def test_exclude_cortical_stimulation(self):
        assert not self.df.equals(exclude_cortical_stimulation(self.df))

    def test_cortical_stimulation_columns_data_integrity(self):
        """
        A test to ensure all SEEG_ES = 'ES' are the same as CES.notnull() in the data.
        """
        CS = 'Cortical Stimulation (CS)'
        SEEG_ES = 'sEEG (y) and/or ES (ES)'
        indices1 = (self.df.loc[self.df[SEEG_ES]=='ES', :]).index
        indices2 = (self.df.loc[self.df[CS].notnull(), :]).index
        assert (indices1 == indices2)
