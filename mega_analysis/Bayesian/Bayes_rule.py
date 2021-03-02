import pandas as pd
# import os
# os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
from .Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation, summary_semio_loc_df_from_scripts
from mega_analysis import Semiology, Laterality
from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from collections import Counter
from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query


Lobes = top_level_lobes(Bayesian=True)

def Bayes_rule(prob_S_given_L, p_Semio, p_Loc):
    """
    Give it p(S | L) from topological data (generative/likelihood of semiologies).
    Returns p(L | S) Bayesian estimate (posterior) using marginal probabilities and Bayes' Rule.

    The marginals are from all data but can be tweaked as sensitivity analyses in future.

    > p_Loc is pd.Series with columns as {top level lobes}
    > p_Semio is pd.DataFrame with index as {Semiology} and a probability column
    > prob_S_given_L is index of semiologies and cols of lobes

    Alim-Marvasti Feb 2021
    """
    # initialise posterior
    prob_L_given_S = pd.DataFrame()
    # set non-existing GIF parcellations to zero:
    try:
        prob_S_given_L[[loc for loc in p_Loc.columns if loc not in prob_S_given_L.columns]] = 0
        p_Loc[[loc for loc in prob_S_given_L.columns if loc not in p_Loc.columns]] = 0
    except:
        pass

    # Bayes rule using two for loops for multiple cases.
    # The simple case would be: prob_L_given_S = (prob_S_given_L * p_Loc) / p_Semio
    for semio in p_Semio.index:
        for loc in p_Loc.columns:
            if "Unnamed" in loc:
                continue
            prob_L_given_S.loc[semio, loc] = (prob_S_given_L.loc[semio, loc] * p_Loc[loc].values) / p_Semio.loc[semio, 'probability']

    return prob_L_given_S


def renormalised_probabilities(df):
    """
    To ensure the Bayes_rule() outputs are probabilities given a semiology.
    This was not the case when erroneously using all-data for the marginals.
        df rows: semiologies
        df columns: localisations/GIF parcellations.
    """
    renormalised_prob = df.div(df.sum(axis=1), axis='index')
    return renormalised_prob


def wrapper_TS_GIFs(p_S_norm,
        global_lateralisation=False,
        include_paeds_and_adults=True,
        include_only_postictals=False,
        symptom_laterality='NEUTRAL',
        dominance='NEUTRAL',
        normalise_to_localising_values=True,
        ):
    """
    Get all Gifs for all semiologies from Toplogical (include_spontaneous_semiology=False) studies.
    See below to make more efficient.
    """
    # initialise
    pt = {}
    all_combined_gifs_superdict = {}
    added_all_gifs = {}
    added_all_gifs = Counter(added_all_gifs)
    p_S_given_GIF = pd.DataFrame()

    for semiology in p_S_norm.index:
        pt[semiology] = Semiology(
                                    semiology,
                                    include_spontaneous_semiology=False, # crucial
                                    symptoms_side=Laterality.NEUTRAL,
                                    dominant_hemisphere=Laterality.NEUTRAL,
                                    include_postictals=False,
                                    include_paeds_and_adults=include_paeds_and_adults,
                                    normalise_to_localising_values=normalise_to_localising_values,
                                    global_lateralisation=global_lateralisation,
                                )
        pt[semiology].include_only_postictals = include_only_postictals
        all_combined_gifs_superdict[semiology] = pt[semiology].get_num_datapoints_dict(method='normalised')  # method=anything but default proportions

    # now add the dictionaries: this seems to repeat what marginal_GIF_probabilities does - can make more efficient
    for semio_dict_result, v in all_combined_gifs_superdict.items():  # equivalent: for semiology in p_S_norm.index:
        temp_dict = Counter(all_combined_gifs_superdict[semio_dict_result])
        added_all_gifs = added_all_gifs + temp_dict
    # turn counter back to dict
    added_all_gifs = dict(added_all_gifs)

    # so totals for each semiology, given a GIF, is added_all_gifs[GIF #]
    # now we need to look at each individual GIF and semio
    for semiology in p_S_norm.index:
        for GIF_no, v in all_combined_gifs_superdict[semiology].items():
            p_S_given_GIF.loc[semiology, GIF_no] = v / added_all_gifs[GIF_no]

    return p_S_given_GIF


def multiple_melt_pivots(topology_results, p_S_norm):
    pivot_result = {}  # dict of dfs
    for semio in p_S_norm.index:
        df_a = topology_results[semio]['query_inspection']
        pivot_result[semio] = melt_then_pivot_query('', df_a, semio)
        # list comprehension to keep top-level lobes only in df:
        pivot_result[semio] = pivot_result[semio][[i for i in Lobes if i in pivot_result]]
    return pivot_result


def wrapper_generative_from_TS(pivot_result, p_S_norm):
    # initialise
    prob_S_given_TopLevelLobes_norm = pd.DataFrame()
    prob_S_given_TopLevelLobes_notnorm = pd.DataFrame()
    added_all_pivot_results = {}
    added_all_pivot_results = Counter(added_all_pivot_results)
    # # first find the total of top lobes:
    for semio in p_S_norm.index:
        temp_dict = Counter(pivot_result[semio].to_dict('index').pop(semio))
        added_all_pivot_results = added_all_pivot_results + temp_dict
    # turn counter back to dict: so totals for each lobe is added_all_pivot_results[lobe]
    added_all_pivot_results = dict(added_all_pivot_results)

    for semio in p_S_norm.index:
        for toplobe in Lobes:
            prob_S_given_TopLevelLobes_norm.loc[semio, toplobe] = \
                pivot_result[semio][toplobe] / added_all_pivot_results[toplobe]
    return prob_S_given_TopLevelLobes_norm


def Bayes_All():
    """ Apply Bayes_rule to the GIFs and Top-Level Regions """
    # get marginal probabilities (p_S as DataFrames, p_Loc as Series): takes <4 mins
    p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
    p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,  # p_GIF is a row -vector df of marginal probabilities, cols as GIF #s and "probability"
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )

    # get likelihoods from Topological data: takes >5mins per each call to summary_semio_loc_df_from_scripts
    prob_S_given_GIFs_norm = wrapper_TS_GIFs(p_S_norm, normalise_to_localising_values=True)
    prob_S_given_GIFs_notnorm = wrapper_TS_GIFs(p_S_norm, normalise_to_localising_values=False)

    query_results_norm = summary_semio_loc_df_from_scripts(normalise=True)
    query_results_notnorm = summary_semio_loc_df_from_scripts(normalise=False)
    topology_results_norm = query_results_norm['topology']
    topology_results_notnorm = query_results_notnorm['topology']
    pivot_result_norm = multiple_melt_pivots(topology_results_norm, p_S_norm)
    pivot_result_notnorm = multiple_melt_pivots(topology_results_notnorm, p_S_norm)
    prob_S_given_TopLevelLobes_norm = wrapper_generative_from_TS(pivot_result_norm, p_S_norm)
    prob_S_given_TopLevelLobes_notnorm = wrapper_generative_from_TS(pivot_result_notnorm, p_S_norm)

    # GIFS
    prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
    # if using marginals from all-data, need to renormalise
    # prob_GIF_given_S_norm = renormalised_probabilities(prob_GIF_given_S_norm)
    prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_GIFs_notnorm, p_S_notnorm, p_GIF_notnorm)
    # prob_GIF_given_S_notnorm = renormalised_probabilities(prob_GIF_given_S_notnorm)

    # TOP LEVEL LOCS
    prob_TopLevel_given_S_norm = Bayes_rule(prob_S_given_TopLevelLobes_norm, p_S_norm, p_Loc_norm)
    # prob_TopLevel_given_S_norm = renormalised_probabilities(prob_TopLevel_given_S_norm)
    prob_TopLevel_given_S_notnorm = Bayes_rule(prob_S_given_TopLevelLobes_notnorm, p_S_notnorm, p_Loc_notnorm)
    # prob_TopLevel_given_S_notnorm = renormalised_probabilities(prob_TopLevel_given_S_notnorm)

    return prob_GIF_given_S_norm, prob_GIF_given_S_notnorm, prob_TopLevel_given_S_norm, prob_TopLevel_given_S_notnorm







# # %%
# import os
# os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
# from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation

# p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
# p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
#                                        include_paeds_and_adults=True,
#                                        include_only_postictals=False,
#                                        symptom_laterality='neutral',
#                                        dominance='neutral',
#                                        )

# # %%
# import os
# os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
# from mega_analysis.Bayesian.Bayes_rule import Bayes_All

# prob_GIF_given_S_norm, prob_GIF_given_S_notnorm = Bayes_All()

# # %%

# # %%
