from pandas.testing import assert_series_equal, assert_frame_equal
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation, summary_semio_loc_df_from_scripts
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule, wrapper_TS_GIFs
import pandas as pd

# --------------Load----------------------------
directory = r'D:\Ali USB Backup\1 PhD\papers\Brain Landscape of Semiology\Bayesian correction\variables'
prob_S_given_GIFs_norm = pd.read_csv(directory +r'\prob_S_given_GIFs_norm.csv', index_col=0)
p_S_norm = pd.read_csv(directory +r'\p_S_norm.csv', index_col=0)
p_GIF_norm = pd.read_csv(directory +r'\p_GIF_norm.csv', index_col=0)
prob_S_given_GIFs_notnorm = pd.read_csv(directory +r'\prob_S_given_GIFs_notnorm.csv', index_col=0)
p_S_notnorm = pd.read_csv(directory +r'\p_S_notnorm.csv', index_col=0)
p_GIF_notnorm = pd.read_csv(directory +r'\p_GIF_notnorm.csv', index_col=0)
p_Loc_norm = pd.read_csv(directory +r'\p_Loc_norm.csv', index_col=0)
p_Loc_notnorm = pd.read_csv(directory +r'\p_Loc_notnorm.csv', index_col=0)

# --------------^--------------------------------------------------------------


# marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
# worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
# normalised and notnormalised marginal probabilities of semiologies are exactly the same:
assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)





# --------------Copy more Bayes_All() here----------------------------
# get likelihood from Topological data:


# GIFS
prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_GIFs_notnorm, p_S_notnorm, p_GIF_notnorm)

# TOP LEVEL LOCS
# prob_TopLevel_given_S_norm = Bayes_rule(prob_S_given_TopLevelLobes_norm, p_S_norm, p_Loc_norm)
# prob_TopLevel_given_S_notnorm = Bayes_rule(prob_S_given_TopLevelLobes_notnorm, p_S_notnorm, p_Loc_notnorm)

# --------------^--------------------------------------------------------------