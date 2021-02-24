import sys
import unittest
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation


class Test_BAYES(unittest.TestCase):
    def setUp(self):
        print('setup')

    def test_bayes(self):
        """ The results are very similar but not exactly the same when normalising to the localising value column,
        or to the (sum of sum) of the top level regions. This is after lots of redistribution, dropping cerebellum etc
        so need to accept ~1% error rate. """
        p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full',
                                                                                        test=True)



if __name__ == '__main__':
    sys.argv.insert(1, '--verbose')
    unittest.main(argv=sys.argv)