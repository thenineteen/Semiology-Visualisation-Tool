from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation
# import os
# os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')


def test_Bayes_nearly():
    """ The results are very similar but not exactly the same when normalising to the localising value column,
    or to the sum of the top level regions. This is after lots of redistribution, dropping cerebellum etc
    so need to accept 1% error rate. """
    p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = \
        p_Semiology_and_Localisation(publication_prior='full',
                                     test=True)
