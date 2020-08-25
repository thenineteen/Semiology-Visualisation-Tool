import unittest
import sys

from mega_analysis.semiology import mega_analysis_df
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclusions,
    exclude_ET,
    exclude_sEEG,
    exclude_cortical_stimulation,
    exclude_seizure_free,
    exclude_paediatric_cases,
    exclude_postictals,
    exclude_spontaneous_semiology
)


class TestExclusions(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()

    def test_default_no_exclusions(self):
        # excl_df = exclusions(self.df)
        # assert not self.df.shape == excl_df.shape
        assert not self.df.equals(exclusions(self.df))

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

    def test_exclude_paeds(self):
        assert not self.df.equals(exclude_paediatric_cases(self.df))

    # def test_exclude_postictal(self):
    #     assert not self.df.equals(exclude_postictals(self.df))

    def test_exclude_spontaneous(self):
        assert not self.df.equals(exclude_spontaneous_semiology(self.df))

    def test_cortical_stimulation_columns_data_integrity(self):
        """
        A test to ensure all SEEG_ES = 'ES' are the same as CES.notnull() in the data.
        This test fails when a new updated excel file is added - can then manually check data
        using the returned indices from this test. As of 13/5/20 Marvasti has checked and is happy.
        Uncomment again when new excel uploaded.
        """
        CS = 'Cortical Stimulation (CS)'
        SEEG_ES = 'sEEG (y) and/or ES (ES)'
        indices1 = (self.df.loc[self.df[SEEG_ES].str.contains(
            'ES', na=False, case=False), :]).index
        indices2 = (self.df.loc[self.df[CS].notnull(), :]).index
        i1noti2 = [i for i in indices1 if i not in indices2]
        i2noti1 = [i for i in indices2 if i not in indices1]

        # test nothing besides np.nan and 'y' in CS
        assert len(set(self.df[CS])) == 2

        # test all ES in sEEG_ES are marked as y in CS
        if indices1.all() != indices2.all():
            print('\n\nsEEG_ES indices1 not in CES: ',
                  self.df.loc[i1noti2, 'Reference'])
            print('\n\nCES indices 2 not in sEEG_ES: ',
                  self.df.loc[i2noti1, 'Reference'])
        assert (indices1.all() == indices2.all())


if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)
