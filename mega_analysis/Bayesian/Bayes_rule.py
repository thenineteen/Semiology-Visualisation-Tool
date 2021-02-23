import os
os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
from .Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation



def Bayes_rule(prob_S_given_L, p_Semio, p_Loc):
    """
    Give it p(S | L) from topological data (generative/likelihood).
    Returns p(L | S) Bayesian estimate (posterior) using marginal probabilities and Bayes' Rule.

    The marginals are from all data but can be tweaked as sensitivity analyses in future.

    Alim-Marvasti Feb 2021
    """
    prob_L_given_S = (prob_S_given_L * p_Loc) / p_Semio

    return prob_L_given_S


def Bayes_GIF(normalise=True):
    """ Apply Bayes_rule to the GIFs """
    # get marginal probabilities:
    p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full')
    p_GIF_norm, p_GIF_nornorm = p_GIFs(global_lateralisation=False,
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )

    # get likelihood:
    prob_S_given_L =

    if normalise:
        prob_GIF_given_S = Bayes_rule(prob_S_given_L, p_S_norm, p_GIF_norm)
    elif not normalise:
        prob_GIF_given_S = Bayes_rule(prob_S_given_L, p_S_notnorm, p_GIF_nornorm)

    return prob_GIF_given_S

