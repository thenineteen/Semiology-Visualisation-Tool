import sys
import unittest
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation
from pandas.testing import assert_series_equal, assert_frame_equal


class Test_BAYES(unittest.TestCase):
    def setUp(self):
        print('setup')

    def test_bayes(self):
        """ The results are very similar but not exactly the same when normalising to the localising value column,
        or to the (sum of sum) of the top level regions. This is after lots of redistribution, dropping cerebellum etc
        so need to accept ~1% error rate.

        see assert_frame_equal in Bayesian_marginals for the test assertion and tolerance"""

        # --------------Copy paste parts of Bayes rule Bayes_All() here----------------------------
        p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
        # p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
        #                                     include_paeds_and_adults=True,
        #                                     include_only_postictals=False,
        #                                     symptom_laterality='neutral',
        #                                     dominance='neutral',
        #                                     )
        # --------------^--------------------------------------------------------------

        # marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
        # worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
        assert_series_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
        assert_series_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
        # normalised and notnormalised marginal probabilities of semiologies are exactly the same:
        assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)



if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)