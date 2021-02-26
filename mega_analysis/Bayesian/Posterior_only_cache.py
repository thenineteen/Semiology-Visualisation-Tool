
# import os
# os.chdir('C:/Users/ali_m/AnacondaProjects/PhD/Semiology-Visualisation-Tool/')
from .Bayes_rule import Bayes_All
from pandas.testing import assert_series_equal, assert_frame_equal
import pandas as pd
from pathlib import Path
from collections import defaultdict

from mega_analysis.crosstab.file_paths import file_paths
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.Bayesian.Bayesian_marginals import summary_semio_loc_df_from_scripts
from mega_analysis.Bayesian.Bayes_rule import Bayes_rule
from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query
from mega_analysis.crosstab.lobe_top_level_hierarchy_only import top_level_lobes

# --------------Load----------------------------
directory = Path(__file__).parent.parent.parent/'resources' / 'Bayesian_resources'
prob_S_given_GIFs_norm = pd.read_csv(directory / 'prob_S_given_GIFs_norm.csv', index_col=0)
p_S_norm = pd.read_csv(directory / 'p_S_norm.csv', index_col=0)
p_GIF_norm = pd.read_csv(directory / 'p_GIF_norm.csv', index_col=0)
prob_S_given_GIFs_notnorm = pd.read_csv(directory / 'prob_S_given_GIFs_notnorm.csv', index_col=0)
p_S_notnorm = pd.read_csv(directory / 'p_S_notnorm.csv', index_col=0)
p_GIF_notnorm = pd.read_csv(directory / 'p_GIF_notnorm.csv', index_col=0)
p_Loc_norm = pd.read_csv(directory / 'p_Loc_norm.csv', index_col=0)
p_Loc_notnorm = pd.read_csv(directory / 'p_Loc_notnorm.csv', index_col=0)
# --------------^--------------------------------------------------------------


def df_to_dict_like_allcombinedgifs(df, semio, method=2):
    # make the loaded df's astype SemiologyVisualisation and semiology handle:
    # ensure df, fillna, index as int not string
    if isinstance(df, pd.Series):
        df = pd.DataFrame(df)
    df.fillna(0, inplace=True)
    df['GIF'] = df.index
    df = df.astype({'GIF':int})
    df.set_index(df['GIF'], inplace=True)
    df.drop(columns='GIF', inplace=True)

    if method==1:
        num_datapoints_dict = defaultdict(list)
        df.to_dict('records', into=num_datapoints_dict)
    else:
        num_datapoints_dict = df.to_dict().pop(semio)

    # these GIFs are zero on marginal and p_GIF_given_S.. and SVT doesn't support these structures:
    # all related to cerebellum exterior, white matter, and cerebellar vermal lobules
    zero_GIF = [39, 40, 41, 42, 72, 73, 74]
    for gif in zero_GIF:
        num_datapoints_dict.pop(gif)
    return num_datapoints_dict


def Bayes_posterior_GIF_only(ready_made_semiology, normalise_to_loc):
    """
    This only shows the GIF #s and posterior probabilities, using TS data, without SS.
    All-data is used for the marginal probabilities.

    > ready_made_semiology: as this is in the form of pre-ran csv (takes time), semiology term can only be from the ready made list.
    > normalise to number of patients or not.

    Most of this is from the Debug_Bayes_Rule_FastLoad which is a faster cached loading of data of Bayes_All().

    Alim-Marvasti 2021
    """

    # GIFS
    if normalise_to_loc:
        prob_GIF_given_S_norm = Bayes_rule(prob_S_given_GIFs_norm, p_S_norm, p_GIF_norm)
        df = prob_GIF_given_S_norm.loc[ready_made_semiology]
        num_datapoints_dict = df_to_dict_like_allcombinedgifs(df, ready_made_semiology, method=2)

    elif not normalise_to_loc:
        prob_GIF_given_S_notnorm = Bayes_rule(prob_S_given_GIFs_notnorm, p_S_notnorm, p_GIF_notnorm)
        df = prob_GIF_given_S_notnorm.loc[ready_made_semiology]
        num_datapoints_dict = df_to_dict_like_allcombinedgifs(df, ready_made_semiology, method=2)

    return num_datapoints_dict
