import unittest
import pandas as pd
from mega_analysis.semiology import mega_analysis_df


CS = 'Cortical Stimulation (CS)'
SS = 'Spontaneous Semiology (SS)'
ET = 'Epilepsy Topology (ET)'
SEEG_ES = 'sEEG (y) and/or ES (ES)'
POST_OP = 'Post-op Sz Freedom (Engel Ia, Ib; ILAE 1, 2)'
CONCORDANT = 'Concordant Neurophys & Imaging (MRI, PET, SPECT)'


class TestGroundTruthsAndPriors(unittest.TestCase):
    def setUp(self):
        self.df = mega_analysis_df.copy()

        # some rows are for information or cumulative sums or annotations
        # these won't have reported semiology, remove them first for this test
        self.df.dropna(
            subset=['Reported Semiology'], axis=0, inplace=True)

    def test_ground_truths(self):
        """
        Semio2Brain Database test.
        A test to ensure all the data from MEGA_ANALYSIS (after cleaning) have at least 1 ground truth label.
        If fails, needs Semio2Brain Database correction of missing data.
        """
        GT_subset = [CONCORDANT, SEEG_ES, POST_OP]

        # first test thresh 0 dropna which is equivalent to not dropping anything.
        # this should pass by definition
        df_thresh_zero = self.df.dropna(
            subset=GT_subset, thresh=0, axis=0, inplace=False)
        assert (df_thresh_zero.shape == self.df.shape)

        # if actual test fails, help to check the Semio2Brain Database entries:
        df_ground_truths_at_least_one_notNaN = self.df.dropna(
            subset=GT_subset, thresh=1, axis=0, inplace=False)

        if (df_ground_truths_at_least_one_notNaN.shape != self.df.shape):
            indices = [
                i for i in self.df.index if i not in df_ground_truths_at_least_one_notNaN.index]
            print('\n\nThese are the GT discrepancies: ',
                  self.df.loc[indices, ['Reference', 'Reported Semiology']])

        # now for the actual test assertion
        assert (df_ground_truths_at_least_one_notNaN.shape == self.df.shape)

    def test_Bayesian_selection_priors(self):
        """
        Semio2Brain Databse integrity test.
        Testing to ensure there are at least one "y" labels for the BAyesian priors
            Spontaneous Semiology
            Topological prior
            Cortical stimulation
        """
        Bayesian_priors = [CS, SS, ET]
        df_Bayesian_priors_atleast_one_notNaN = self.df.dropna(
            subset=Bayesian_priors, thresh=1, axis=0, inplace=False)

        indices = [
            i for i in self.df.index if i not in df_Bayesian_priors_atleast_one_notNaN.index]

        if (df_Bayesian_priors_atleast_one_notNaN.shape != self.df.shape):
            print('\n\nBayesian discrepancies: ',
                  self.df.loc[indices, ['Reference', 'Reported Semiology']])
        assert (df_Bayesian_priors_atleast_one_notNaN.shape == self.df.shape)
