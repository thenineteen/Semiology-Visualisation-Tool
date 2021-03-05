import sys
import unittest
import pandas as pd
from pathlib import Path

from mega_analysis.Bayesian.Bayesian_marginals import p_GIFs, p_Semiology_and_Localisation
from mega_analysis.Bayesian.Posterior_only_cache import Bayes_posterior_GIF_only
from pandas.testing import assert_series_equal, assert_frame_equal
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule, renormalised_probabilities
from mega_analysis import Semiology, Laterality
from mega_analysis.semiology import get_df_from_semiologies, combine_semiologies


# --------------Load----------------------------
directory = Path(__file__).parent.parent/'resources' / 'Bayesian_resources'
marginal_folder = 'SemioMarginals_fromSS_GIFmarginals_from_TS'
variables_folder = 'Variables_from_all_data_not_renormalised'
prob_S_given_GIFs_norm = pd.read_csv(directory / 'prob_S_given_GIFs_norm.csv', index_col=0)
p_S_norm = pd.read_csv(directory / marginal_folder / 'p_S_norm_SS.csv', index_col=0)
p_GIF_norm = pd.read_csv(directory / marginal_folder / 'p_GIF_norm_TS.csv', index_col=0)
prob_S_given_GIFs_notnorm = pd.read_csv(directory / 'prob_S_given_GIFs_notnorm.csv', index_col=0)
p_S_notnorm = pd.read_csv(directory / marginal_folder / 'p_S_notnorm_SS.csv', index_col=0)
p_GIF_notnorm = pd.read_csv(directory / marginal_folder / 'p_GIF_notnorm_TS.csv', index_col=0)
p_Loc_norm = pd.read_csv(directory / 'p_Loc_norm.csv', index_col=0)
p_Loc_notnorm = pd.read_csv(directory / 'p_Loc_notnorm.csv', index_col=0)
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
# --------------^--------------------------------------------------------------

class Test_BAYES(unittest.TestCase):
    def setUp(self):
        print('setup')

    def test_bayes(self):
        """ The results are very similar but not exactly the same when normalising to the localising value column,
        or to the (sum of sum) of the top level regions. This is after lots of redistribution, dropping cerebellum etc
        so need to accept ~1% error rate.

        see assert_frame_equal in Bayesian_marginals for the test assertion and tolerance"""

        # --------------Copy paste parts of Bayes rule Bayes_All() here----------------------------
        # p_S_norm, p_Loc_norm, p_S_notnorm, p_Loc_notnorm = p_Semiology_and_Localisation(publication_prior='full', test=False)
        # p_GIF_norm, p_GIF_notnorm = p_GIFs(global_lateralisation=False,
        #                                     include_paeds_and_adults=True,
        #                                     include_only_postictals=False,
        #                                     symptom_laterality='neutral',
        #                                     dominance='neutral',
        #                                     )
        # --------------^--------------------------------------------------------------

        # marginal top level lobe localisations are equal to within 3.7% aboslute tolerance or within 35.1% of relative tolerance
        # worse for cingulate (35.1% less on normalisation), then for Parietal lobe (16.8% less on normalisation) and then for frontal lobe (13.7% less on normalisation) all others are within 7 % error
        assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, atol=0.037)
        assert_frame_equal(p_Loc_norm, p_Loc_notnorm, check_exact=False, check_dtype=False, rtol=0.351)
        # normalised and notnormalised marginal probabilities of semiologies are exactly the same:
        assert_frame_equal(p_S_norm, p_S_notnorm, check_exact=True, check_dtype=True)

    def test_renormalisation_of_posterior_from_Bayes_using_all_data_marginals(self):
        """
        Hypomotor does not occur in SS dataset but renormalisation should still give 1.
        Renormalised when posterior est from Bayes used all-data for marginal priors, the posterior didn't add up to 1.

        """
        prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
        prob_GIF_given_S_norm = renormalised_probabilities(prob_GIF_given_S_norm)

        assert prob_GIF_given_S_norm.shape[0] == 35  # number of semiologies
        assert (
            round(
            (prob_GIF_given_S_norm.sum().sum()), 1
            ) == round(34, 1))  # semiologies minus the zero for hypomotor as doesn't occur in SS dataset
        # # they all add up to 1 (probabilities)
        # assert (prob_GIF_given_S_norm.sum(axis=1).sum() == prob_GIF_given_S_norm.shape[0])


class Bayesian_Global_Lateralisation(unittest.TestCase):
    def setUp(self):
        print('setup')

    def test_SS_control(self):
        """
        control: right visual global lateralisation gives left hemisphere > right hemisphere for SS-database query.
        #32 RIGHT ANYGDALA
        #33 LEFT AMYGDALA
        """
        method='proportions'
        Patient_VisualRight = Semiology(
            'Visual',
            symptoms_side=Laterality.RIGHT,
            dominant_hemisphere=Laterality.NEUTRAL,
            normalise_to_localising_values=True,
            global_lateralisation=True,
            include_et_topology_ez=False,
            include_cortical_stimulation=False,
            include_spontaneous_semiology=True,
        )
        df_proportions, all_combind_gif_dfs = get_df_from_semiologies([Patient_VisualRight], method=method)
        try:
            df_proportions.loc['Visual', 32] > 0
        except KeyError:  # re,oved as it was zero
            df_proportions.loc['Visual', 32] = 0
        assert round(df_proportions.loc['Visual', 32], 3) < round(df_proportions.loc['Visual', 33], 3)


    def test_Bayesian_global_lateralisation(self):
        """
        For Bayesian Global Lateralisation, we want right-sided visual-TS-posterior estimate to not have symmetrical GIF values.
        When this test passes, we have global lateralisation enabled for bayesian-posterior-TS-only estimate
            [and also work when combining with SS, because posteror-from-TS is averaged (mean) with SS, and both will now be lateralised.]
        #32 RIGHT ANYGDALA
        #33 LEFT AMYGDALA
        """
        method = 'Bayesian only'
        Patient_VisualRight = Semiology(
            'Visual',
            symptoms_side=Laterality.RIGHT,
            dominant_hemisphere=Laterality.LEFT,
            normalise_to_localising_values=True,
            global_lateralisation=True,  # again not relevant as using BAyesian only - not using the df from this, but just the lateralising values
            # include_et_topology_ez=False,  # not relevant as using Bayesian only
            # include_cortical_stimulation=False,
            # include_spontaneous_semiology=True,
        )
        df_proportions, all_combind_gif_dfs = get_df_from_semiologies([Patient_VisualRight], method=method)
        # we want <. all_combind_gif_dfs is globally-laterlised df_proportions
        #   but get_df_from_semiologies is a function and doesn't store the self.symptoms_side information
        #   so use the next function down the chain:
        num_datapoints_dict, all_combined_gif_df = Patient_VisualRight.get_num_datapoints_dict(method=method)
        assert round(num_datapoints_dict[32], 3) < round(num_datapoints_dict[33], 3)
