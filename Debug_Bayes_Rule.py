from pandas.testing import assert_series_equal, assert_frame_equal
from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation, summary_semio_loc_df_from_scripts
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule, wrapper_TS_GIFs

# --------------Copy paste parts of Bayes rule Bayes_All() here----------------------------
p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
                                       include_paeds_and_adults=True,
                                       include_only_postictals=False,
                                       symptom_laterality='neutral',
                                       dominance='neutral',
                                       )
# --------------^--------------------------------------------------------------


# marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
# worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
assert_series_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
assert_series_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
# normalised and notnormalised marginal probabilities of semiologies are exactly the same:
assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)





# --------------Copy more Bayes_All() here----------------------------
# get likelihood from Topological data:
query_results_norm = summary_semio_loc_df_from_scripts(normalise=True)
query_results_notnorm = summary_semio_loc_df_from_scripts(normalise=False)
prob_S_given_TopLevelLobes_norm = query_results_norm['topology']
prob_S_given_TopLevelLobes_notnorm = query_results_notnorm['topology']
prob_S_given_GIFs_norm = wrapper_TS_GIFs(p_S_norm, normalise_to_localising_values=True)
prob_S_given_GIFs_notnorm = wrapper_TS_GIFs(p_S_norm, normalise_to_localising_values=False)

# GIFS
prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_GIFs_notnorm, p_S_notnorm, p_GIF_notnorm)

# TOP LEVEL LOCS
# prob_TopLevel_given_S_norm = Bayes_rule(prob_S_given_TopLevelLobes_norm, p_S_norm, p_Loc_norm)
# prob_TopLevel_given_S_notnorm = Bayes_rule(prob_S_given_TopLevelLobes_notnorm, p_S_notnorm, p_Loc_notnorm)

# --------------^--------------------------------------------------------------