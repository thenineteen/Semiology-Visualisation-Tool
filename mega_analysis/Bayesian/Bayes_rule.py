import pandas as pd
import os
os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
from .Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation, summary_semio_loc_df_from_scripts
from mega_analysis import Semiology, Laterality
from pathlib import Path
from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from collections import Counter

file = Path(__file__).parent/'resources'/'semiologies_neutral_only.txt'
list_of_terms = list(open(file, 'r'))

def Bayes_rule(prob_S_given_L, p_Semio, p_Loc):
    """
    Give it p(S | L) from topological data (generative/likelihood).
    Returns p(L | S) Bayesian estimate (posterior) using marginal probabilities and Bayes' Rule.

    The marginals are from all data but can be tweaked as sensitivity analyses in future.

    Alim-Marvasti Feb 2021
    """
    prob_L_given_S = (prob_S_given_L * p_Loc) / p_Semio

    return prob_L_given_S


def wrapper_TS_GIFs(p_S_norm,
        global_lateralisation=False,
        include_paeds_and_adults=True,
        include_only_postictals=False,
        symptom_laterality='neutral',
        dominance='neutral',
        ):
    """
    Get all Gifs for all semiologies
    """
    pt = {}
    added_all_gifs = {}
    all_combined_gifs_superdict = {}
    for semiology in p_S_norm.index:
        pt[semiology] = Semiology(
                                    semiology,
                                    include_spontaneous_semiology=False,
                                    symptoms_side=Laterality.NEUTRAL,
                                    dominant_hemisphere=Laterality.NEUTRAL,
                                    include_postictals=False,
                                    include_paeds_and_adults=include_paeds_and_adults,
                                    normalise_to_localising_values=True,
                                    global_lateralisation=global_lateralisation,
                                )
        pt[semiology].include_only_postictals = include_only_postictals
        all_combined_gifs_superdict[semiology] = pt[semiology].get_num_datapoints_dict(method='normalised')  # method=anything but default proportions

    # now add the dictionaries:
    for semio_dict_result, v in all_combined_gifs_superdict.items():
        temp_dict = Counter(all_combined_gifs_superdict[semio_dict_result])
        added_all_gifs.update(temp_dict)

    # so totals for each semiology, given a GIF, is added_all_gifs[GIF #]
    return added_all_gifs


def Bayes_All():
    """ Apply Bayes_rule to the GIFs """
    # get marginal probabilities:
    p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full')
    p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,  # p_GIF is a row df of marginal probabilities, cols as GIF #s and "probability"
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )

    # get likelihood from Topological data:
    query_results = summary_semio_loc_df_from_scripts(normalise=True)
    prob_S_given_L_TopLevelLobes = query_results['topology']
    all_combined_gifs_superdict = wrapper_TS_GIFs()  # now we need to look at each individual GIF



    # GIFS
    prob_GIF_given_S_norm = Bayes_rule(prob_S_given_L_GIFs, p_S_norm, p_GIF_norm)
    prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_L_GIFs, p_S_notnorm, p_GIF_notnorm)

    return prob_GIF_given_S_norm, prob_GIF_given_S_notnorm




# %%
import os
os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation

p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )

# %%

