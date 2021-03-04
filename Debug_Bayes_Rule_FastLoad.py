from pandas.testing import assert_series_equal, assert_frame_equal
import pandas as pd
from pathlib import Path
from collections import Counter

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule, Bayes_All, renormalised_probabilities
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query
from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes
from mega_analysis.Bayesian.Posterior_only_cache import Bayes_posterior_GIF_only


# to debug and test SVT GIF - Posterior_only_cache.Bayes_posterior_GIF_only:
num_datapoints_dict = Bayes_posterior_GIF_only('Epigastric', True)



# to debug using saved GIF posteriors given Semiology.
# --------------Load----------------------------
directory = Path(__file__).parent/'resources' / 'Bayesian_resources'
marginal_folder = 'SemioMarginals_fromSS_GIFmarginals_from_TS'
prob_S_given_GIFs_norm = pd.read_csv(directory / 'prob_S_given_GIFs_norm.csv', index_col=0)
p_S_norm = pd.read_csv(directory / marginal_folder / 'p_S_norm_SS.csv', index_col=0)
p_GIF_norm = pd.read_csv(directory / marginal_folder / 'p_GIF_norm_TS.csv', index_col=0)
prob_S_given_GIFs_notnorm = pd.read_csv(directory / 'prob_S_given_GIFs_notnorm.csv', index_col=0)
p_S_notnorm = pd.read_csv(directory / marginal_folder / 'p_S_notnorm_SS.csv', index_col=0)
p_GIF_notnorm = pd.read_csv(directory / marginal_folder / 'p_GIF_notnorm_TS.csv', index_col=0)
# --------------^--------------------------------------------------------------
# drop the zero GIFs:
    # # these GIFs are zero on marginal and p_GIF_given_S.. and SVT doesn't support these structures:
    # # all related to cerebellum exterior, white matter, and cerebellar vermal lobules
    # for gif in zero_GIF:
    #     num_datapoints_dict.pop(gif)
zero_GIF = ['39', '40', '41', '42', '72', '73', '74']
zero_GIF_int = [39, 40, 41, 42, 72, 73, 74]
p_GIF_norm.drop(columns=zero_GIF, inplace=True, errors='ignore')
p_GIF_notnorm.drop(columns=zero_GIF, inplace=True, errors='ignore')
prob_S_given_GIFs_norm.drop(columns=zero_GIF, inplace=True, errors='ignore')
prob_S_given_GIFs_notnorm.drop(columns=zero_GIF, inplace=True, errors='ignore')
# # --------------^--------------------------------------------------------------


prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
prob_GIF_given_S_norm = renormalised_probabilities(prob_GIF_given_S_norm)

assert prob_GIF_given_S_norm.shape[0] == 35  # number of semiologies
assert (prob_GIF_given_S_norm.sum(axis=1)).values.sum()  == 35
# they all add up to 1 (probabilities)
assert (prob_GIF_given_S_norm.sum(axis=1).sum() == prob_GIF_given_S_norm.shape[0])





# # marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
# # worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
# assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
# assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
# # normalised and notnormalised marginal probabilities of semiologies are exactly the same:
# assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)



# # get marginal probabilities (p_S as DataFrames, p_Loc as Series): takes <4 mins
# p_S_norm_SS, _, p_S_notnorm_SS, _ = p_Semiology_and_Localisation(publication_prior='spontaneous', test=False, skip_L=True)
# p_GIF_norm_TS, p_GIF_notnorm_TS = p_GIFs(global_lateralisation=False,  # p_GIF is a row-vector df of marginal probabilities, cols as GIF #s and "probability"
#                                     include_paeds_and_adults=True,
#                                     include_only_postictals=False,
#                                     symptom_laterality='neutral',
#                                     dominance='neutral',
#                                     )
