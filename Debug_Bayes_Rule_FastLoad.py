from pandas.testing import assert_series_equal, assert_frame_equal
import pandas as pd
from pathlib import Path
from collections import Counter

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.Bayesian.Bayesian_marginals import summary_semio_loc_df_from_scripts
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query
from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes
from mega_analysis.Bayesian.Posterior_only_cache import Bayes_posterior_GIF_only


# to debug and test Posterior_only_cache.Bayes_posterior_GIF_only:
num_datapoints_dict = Bayes_posterior_GIF_only('Epigastric', True)
type(num_datapoints_dict)

# --------------Load----------------------------
directory = Path(__file__).parent/'resources' / 'Bayesian_resources'
prob_S_given_GIFs_norm = pd.read_csv(directory / 'prob_S_given_GIFs_norm.csv', index_col=0)
p_S_norm = pd.read_csv(directory / 'p_S_norm.csv', index_col=0)
p_GIF_norm = pd.read_csv(directory / 'p_GIF_norm.csv', index_col=0)
prob_S_given_GIFs_notnorm = pd.read_csv(directory / 'prob_S_given_GIFs_notnorm.csv', index_col=0)
p_S_notnorm = pd.read_csv(directory / 'p_S_notnorm.csv', index_col=0)
p_GIF_notnorm = pd.read_csv(directory / 'p_GIF_notnorm.csv', index_col=0)
p_Loc_norm = pd.read_csv(directory / 'p_Loc_norm.csv', index_col=0)
p_Loc_notnorm = pd.read_csv(directory / 'p_Loc_notnorm.csv', index_col=0)


# --------------^--------------------------------------------------------------


# marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
# worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
# normalised and notnormalised marginal probabilities of semiologies are exactly the same:
assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)





# --------------Copy more Bayes_All() here----------------------------
# get likelihood from Topological data:
query_results_norm = summary_semio_loc_df_from_scripts(normalise=True)
query_results_notnorm = summary_semio_loc_df_from_scripts(normalise=False)
topology_results_norm = query_results_norm['topology']
topology_results_notnorm = query_results_notnorm['topology']
prob_S_given_TopLevelLobes_norm = pd.DataFrame()
prob_S_given_TopLevelLobes_notnorm = pd.DataFrame()

Lobes = top_level_lobes(Bayesian=True)

def multiple_melt_pivots(topology_results, p_S_norm):
    pivot_result = {}  # dict of dfs
    for semio in p_S_norm.index:
        df_a = topology_results[semio]['query_inspection']
        df_b = melt_then_pivot_query('', df_a, semio)
        # list comprehension to keep top-level lobes only in df:
        new_dict = {semio : df_b[[i for i in Lobes if i in df_b]]}
        pivot_result.update(new_dict)
    return pivot_result

def wrapper_generative_from_TS(pivot_result, p_S_norm):
    # initialise
    added_all_pivot_results = {}
    added_all_pivot_results = Counter(added_all_pivot_results)
    pivot_result_copy = pivot_result.copy()
    # # first find the total of top lobes:
    for semio in p_S_norm.index:
        temp_dict = Counter(pivot_result_copy[semio].to_dict('index')) #.pop(semio))
        added_all_pivot_results = added_all_pivot_results + temp_dict
    # turn counter back to dict: so totals for each lobe is added_all_pivot_results[lobe]
    added_all_pivot_results = dict(added_all_pivot_results)

    for semio in p_S_norm.index:
        for toplobe in Lobes:
            prob_S_given_TopLevelLobes_norm.loc[semio, toplobe] = \
                pivot_result[semio][toplobe] / added_all_pivot_results[toplobe]
    return prob_S_given_TopLevelLobes_norm


pivot_result_norm = multiple_melt_pivots(topology_results_norm, p_S_norm)
prob_S_given_TopLevelLobes_norm = wrapper_generative_from_TS(pivot_result_norm, p_S_norm)
pivot_result_notnorm = multiple_melt_pivots(topology_results_notnorm, p_S_norm)
prob_S_given_TopLevelLobes_notnorm = wrapper_generative_from_TS(pivot_result_notnorm), p_S_norm

# GIFS
prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_GIFs_notnorm, p_S_notnorm, p_GIF_notnorm)

# TOP LEVEL LOCS: currently this is incorrectly curated: prob_S_given_TopLevelLobes_norm
prob_TopLevel_given_S_norm = Bayes_rule(prob_S_given_TopLevelLobes_norm, p_S_norm, p_Loc_norm)
prob_TopLevel_given_S_notnorm = Bayes_rule(prob_S_given_TopLevelLobes_notnorm, p_S_notnorm, p_Loc_notnorm)


# --------------^--------------------------------------------------------------
print('stop')