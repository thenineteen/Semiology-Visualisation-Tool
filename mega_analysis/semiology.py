import copy
import warnings
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import yaml
import numpy as np
import pandas as pd

from .crosstab.file_paths import file_paths
from .crosstab.hierarchy_class import Hierarchy
from .crosstab.gif_sheet_names import gif_sheet_names
from .crosstab.mega_analysis.exclusions import (
    exclude_cortical_stimulation,
    exclude_ET,
    exclude_sEEG,
    exclude_seizure_free,
    exclude_spontaneous_semiology,
    exclude_paediatric_cases,
    exclude_postictals,
    exclusions,
    only_paediatric_cases,
    only_postictal_cases,
)
from .crosstab.mega_analysis.mapping import pivot_result_to_one_map, big_map
from .crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from .crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query
from .crosstab.mega_analysis.pivot_result_to_pixel_intensities import \
    pivot_result_to_pixel_intensities
from .crosstab.mega_analysis.QUERY_LATERALISATION import QUERY_LATERALISATION
from .crosstab.mega_analysis.QUERY_LATERALISATION_GLOBAL import QUERY_LATERALISATION_GLOBAL
from .crosstab.mega_analysis.QUERY_SEMIOLOGY import QUERY_SEMIOLOGY
from .crosstab.NORMALISE_TO_LOCALISING_VALUES import NORMALISE_TO_LOCALISING_VALUES
from .crosstab.lobe_top_level_hierarchy_only import drop_minor_localisations


GIF_SHEET_NAMES = gif_sheet_names()

# Define paths
repo_dir = Path(__file__).parent.parent
resources_dir = repo_dir / 'resources'
excel_path = resources_dir / 'Semio2Brain Database.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'

# Read Excel file only three times at initialisation
mega_analysis_df, _, _, num_database_articles, num_database_patients, num_database_lat, num_database_loc = MEGA_ANALYSIS(
    excel_data=excel_path)
map_df_dict = pd.read_excel(
    excel_path,
    header=1,
    sheet_name=GIF_SHEET_NAMES,
    engine="openpyxl",
)
gif_lat_file = pd.read_excel(
    excel_path,
    header=0,
    sheet_name='Full GIF Map for Review ', engine="openpyxl",
)
one_map = big_map(map_df_dict)

# Read lateralities for GUI
neutral_only_path = resources_dir / 'semiologies_neutral_only.txt'
neutral_also_path = resources_dir / 'semiologies_neutral_also.txt'
semiologies_neutral_only = neutral_only_path.read_text().splitlines()
semiologies_neutral_also = neutral_also_path.read_text().splitlines()

# Read postictal lateralities for GUI
postictal_neutral_only_path = resources_dir / \
    'semiologies_postictalsonly_neutral_only.txt'
postictal_neutral_also_path = resources_dir / \
    'semiologies_postictalsonly_neutral_also.txt'
postictal_semiologies_neutral_only = postictal_neutral_only_path.read_text().splitlines()
postictal_semiologies_neutral_also = postictal_neutral_also_path.read_text().splitlines()


def recursive_items(dictionary):
    """https://stackoverflow.com/a/39234154/3956024"""
    for key, value in dictionary.items():
        if type(value) is dict:
            yield from recursive_items(value)
        else:
            yield key


def get_all_semiology_terms():
    with open(semiology_dict_path) as f:
        dictionary = yaml.load(f, Loader=yaml.FullLoader)
    return sorted(recursive_items(dictionary))


# Read YAML
all_semiology_terms = get_all_semiology_terms()

# Define constants


class Laterality(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    NEUTRAL = None


class Semiology:
    def __init__(
            self,
            term: str,
            symptoms_side: Laterality,
            dominant_hemisphere: Laterality,
            granular: bool = True,
            include_seizure_freedom: bool = True,
            include_concordance: bool = True,
            include_seeg: bool = True,
            include_cortical_stimulation: bool = True,
            include_et_topology_ez: bool = True,
            include_spontaneous_semiology: bool = True,
            include_only_paediatric_cases: bool = False,
            include_paeds_and_adults: bool = False,
            include_postictals: bool = False,
            possible_lateralities: Optional[List[Laterality]] = None,
            normalise_to_localising_values: bool = False,
            top_level_lobes: bool = False,
            global_lateralisation: bool = False,
            # all_combined_gif_df: Optional[pd.DataFrame] = None,
    ):
        self.term = term
        self.symptoms_side = symptoms_side
        self.dominant_hemisphere = dominant_hemisphere
        self.include_seizure_freedom = include_seizure_freedom
        self.include_concordance = include_concordance
        self.include_seeg = include_seeg
        self.include_cortical_stimulation = include_cortical_stimulation
        self.include_et_topology_ez = include_et_topology_ez
        self.include_spontaneous_semiology = include_spontaneous_semiology
        self.include_only_paediatric_cases = include_only_paediatric_cases
        self.include_paeds_and_adults = include_paeds_and_adults
        self.include_postictals = include_postictals
        self.data_frame = mega_analysis_df
        if possible_lateralities is None:
            possible_lateralities = get_possible_lateralities(self.term)
        self.possible_lateralities = possible_lateralities
        self.granular = granular
        self.normalise_to_localising_values = normalise_to_localising_values
        self.top_level_lobes = top_level_lobes
        self.include_only_postictals = self.is_postictals_only()
        if self.include_only_postictals:
            self.include_postictals = True
        self.global_lateralisation = global_lateralisation
        # self.all_combined_gif_df = all_combined_gif_df

    def is_postictals_only(self) -> bool:
        postictals = (
            postictal_semiologies_neutral_only
            + postictal_semiologies_neutral_also
        )
        return self.term in postictals

    def remove_exclusions(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.include_postictals:
            df = exclude_postictals(df)
        if self.include_only_postictals:
            df = only_postictal_cases(df)
        if self.include_only_paediatric_cases:
            df = only_paediatric_cases(df)
        elif self.include_paeds_and_adults:
            pass
        else:
            df = exclude_paediatric_cases(df)
        if not self.include_concordance:
            df = exclusions(df, CONCORDANCE=True)
        if not self.include_seizure_freedom:
            df = exclude_seizure_free(df)
        if not self.include_et_topology_ez:
            df = exclude_ET(df)
        if not self.include_seeg:
            df = exclude_sEEG(df)
        if not self.include_cortical_stimulation:
            df = exclude_cortical_stimulation(df)
        if not self.include_spontaneous_semiology:
            df = exclude_spontaneous_semiology(df)
        return df

    def query_semiology(self) -> pd.DataFrame:
        if self.term in all_semiology_terms:
            path = semiology_dict_path
        else:
            path = None
        self.data_frame = self.remove_exclusions(self.data_frame)
        inspect_result, num_query_lat, num_query_loc = QUERY_SEMIOLOGY(
            self.data_frame,
            semiology_term=self.term,
            semiology_dict_path=path,
        )
        if self.granular:
            hierarchy_df = Hierarchy(inspect_result)
            hierarchy_df.all_hierarchy_reversal()
            inspect_result = hierarchy_df.new_df
            if self.normalise_to_localising_values:
                inspect_result = NORMALISE_TO_LOCALISING_VALUES(inspect_result)
        elif self.top_level_lobes:
            inspect_result = drop_minor_localisations(inspect_result)
            if self.normalise_to_localising_values:
                inspect_result = NORMALISE_TO_LOCALISING_VALUES(inspect_result)
        return inspect_result

    def query_lateralisation(self, one_map=one_map) -> Optional[pd.DataFrame]:
        query_semiology_result = self.query_semiology()
        if query_semiology_result is None:
            print('No such semiology found')
            return None
        else:
            # Same as saying (query_semiology_result['Localising'].sum() != 0)
            # OR
            # (query_semiology_result['Lateralising'].sum() != 0)
            columns = ['Localising', 'Lateralising']
            localising_lateralising = query_semiology_result[columns]
            ll_empty = localising_lateralising.sum().sum() == 0

            if ll_empty:
                message = f'No query_semiology results for term "{self.term}"'
                raise ValueError(message)
            elif self.global_lateralisation:
                all_combined_gifs, num_QL_lat, num_QL_CL, num_QL_IL, num_QL_BL, num_QL_DomH, num_QL_NonDomH = \
                    QUERY_LATERALISATION_GLOBAL(
                        self.term,
                        query_semiology_result,
                        self.data_frame,
                        one_map,
                        gif_lat_file,
                        side_of_symptoms_signs=self.symptoms_side.value,
                        pts_dominant_hemisphere_R_or_L=self.dominant_hemisphere.value,
                    )
            elif not self.global_lateralisation:
                all_combined_gifs, num_QL_lat, num_QL_CL, num_QL_IL, num_QL_BL, num_QL_DomH, num_QL_NonDomH = \
                    QUERY_LATERALISATION(
                        query_semiology_result,
                        self.data_frame,
                        one_map,
                        gif_lat_file,
                        side_of_symptoms_signs=self.symptoms_side.value,
                        pts_dominant_hemisphere_R_or_L=self.dominant_hemisphere.value,
                    )
                if all_combined_gifs is None:
                    # Either no lateralising pt data, or empty lat column
                    # Run manual pipeline:
                    pivot_result = melt_then_pivot_query(
                        mega_analysis_df,
                        query_semiology_result,
                        self.term,
                    )
                    all_combined_gifs = pivot_result_to_one_map(
                        pivot_result, one_map,
                        # map_df_dict=map_df_dict,
                    )
        return all_combined_gifs

    def get_num_datapoints_dict(self, method: str = 'proportions') -> Optional[dict]:
        """
        all_combined_gif_df is the normalised or not normalised frequency counts used for i;vnerse variance weighting.
        """
        query_lateralisation_result = self.query_lateralisation()
        if query_lateralisation_result is None:
            message = f'No results generated for semiology term "{self.term}"'
            raise ValueError(message)
        array = np.array(query_lateralisation_result)
        _, labels, patients = array.T
        num_datapoints_dict = {
            int(label): float(num_datapoints)
            for (label, num_datapoints)
            in zip(labels, patients)
            if num_datapoints > 0}
        # all_combined_gif_df = pd.DataFrame.from_dict(dict(zip(labels, patients)), orient='index')
        all_combined_gif_df = pd.DataFrame.from_dict(num_datapoints_dict, orient='index')
        if method == 'Bayesian only':
            from .Bayesian.Posterior_only_cache import Bayes_posterior_GIF_only
            num_datapoints_dict = Bayes_posterior_GIF_only(self.term, normalise_to_loc=self.normalise_to_localising_values)
            return num_datapoints_dict, all_combined_gif_df  # recalculate all_combined_gif_df here as it's incorrect placeholder
        if method != 'proportions':
            return num_datapoints_dict, all_combined_gif_df
        elif method == 'proportions':
            total = sum(list(num_datapoints_dict.values()))
            new_datatpoints = {k: v/total for (k, v) in num_datapoints_dict.items()}
            return new_datatpoints, all_combined_gif_df


def get_possible_lateralities(term) -> List[Laterality]:
    lateralities = [Laterality.LEFT, Laterality.RIGHT]
    if term in (semiologies_neutral_only + postictal_semiologies_neutral_only):
        lateralities = [Laterality.NEUTRAL]
    if term in (semiologies_neutral_also + postictal_semiologies_neutral_also):
        lateralities.append(Laterality.NEUTRAL)
    return lateralities


def combine_semiologies(semiologies: List[Semiology], normalise_method: Optional[str] = 'proportions', normalise_zero_axis: bool = True) -> Dict[int, float]:
    """
    This function doesn't seem to be called. Instead UpdateColors calls both normalise_semiologies_df and combine_semiologies_df.
    """
    df, all_combined_gif_dfs = get_df_from_semiologies(semiologies, normalise_method)
    if normalise_method is not None:
        df = normalise_semiologies_df(df, method=normalise_method)
    combined_df = combine_semiologies_df(df, method=normalise_method, normalise=normalise_zero_axis, num_df=all_combined_gif_dfs)
    return combined_df


def get_df_from_semiologies(semiologies: List[Semiology], method: str = 'proportions') -> pd.DataFrame:
    num_datapoints_dicts = {}
    all_combined_gif_dfs = pd.DataFrame()
    for semiology in semiologies:
        num_datapoints_dict, all_combined_gif_df = semiology.get_num_datapoints_dict(method=method)
        if num_datapoints_dict is None:
            message = (
                f'Information for semiology term "{semiology.term}"'
                ' could not be retrieved'
            )
            warnings.warn(message)
        else:
            num_datapoints_dicts[semiology.term] = num_datapoints_dict
            all_combined_gif_df.rename(columns={0:semiology.term}, inplace=True)
            if all_combined_gif_dfs.empty:
                all_combined_gif_dfs = all_combined_gif_df
            else:
                all_combined_gif_dfs = all_combined_gif_dfs.join(all_combined_gif_df, how='outer')
    df = get_df_from_dicts(num_datapoints_dicts)
    df.fillna(value=0, inplace=True)
    return df, all_combined_gif_dfs


def get_df_from_dicts(semiologies_dicts: Dict[str, Dict[int, float]]) -> pd.DataFrame:
    records = []
    semiologies_dicts = copy.deepcopy(semiologies_dicts)
    for term, num_datapoints_dict in semiologies_dicts.items():
        num_datapoints_dict['Semiology'] = term
        records.append(num_datapoints_dict)
    df = pd.DataFrame.from_records(records, index='Semiology')
    return df


def normalise_semiologies_df(semiologies_df: pd.DataFrame, method='proportions') -> pd.DataFrame:
    if method == 'proportions':
        return semiologies_df

    table = np.array(semiologies_df)
    data = table.T
    if method == 'minmax':
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler((0, 1))
        scaler.fit(data)
        normalised = scaler.transform(data).T
    elif method == 'softmax':
        from scipy.special import softmax
        normalised = softmax(semiologies_df, axis=1)
    normalised_df = pd.DataFrame(normalised, columns=semiologies_df.columns, index=semiologies_df.index)
    return normalised_df


def combine_semiologies_df(df: pd.DataFrame,
                        method: str = 'proportions',
                        normalise: bool = True,
                        inverse_variance_method: bool = True, from_marginals: bool = True,
                        num_df: pd.DataFrame = None,) -> Dict[int, float]:
    """
    df is rows of semiologies and columns of GIFs as proportions.

    returns combined_df which is, after a transpose,
    columns of semiologies and rows of 'Score' then GIFs.

    If proportions, then using inverse variance weighted mean of proportions.

    > num_df: all_combined_gif_dfs, rows as GIFs, cols as semios
    """
    if method == 'proportions':
        assert (df.sum(axis=1)).all() == 1
        if inverse_variance_method:
            combination_technique = 'Score'#'Inv Var Weighted'
            combined_df = inv_variance_combine_semiologies(df, num_df, normalise=normalise, from_marginals=from_marginals)
        else:
            # Equal weights to each semiology i.e., variances between semiology observations per GIF assumed equal:
            combined_df = df.mean(axis=0)
            combination_technique = 'Score'#'Mean of proportions'
    else:
        combination_technique = 'Score'
        combined_df = df.sum()
        if normalise:
            combined_df = (combined_df / combined_df.max()) * 100
    combined_df = pd.DataFrame(combined_df).T
    combined_df.index = [combination_technique]
    combined_df.fillna(value=0, inplace=True)
    return combined_df


def inv_variance_combine_semiologies(df, num_df,
                                    normalise, from_marginals=True):
    """
    More general instead of equal weights:
        Inverse Variance Weighted Mean of Proportions: each GIF is approximated as a binomial random variable. Pseudocode:
        combined_df.loc[0 ,j] = (df.loc[i, j] / variance[j]).sum(axis=0) /
                                               (1/variance[j]).sum(axis=0)
                   where variance of binomial proportion is = p(1-p)/n;
                       n is the number of trials for each semiology and
                       p is posterior likelihood probabilities (or the marginal prior obtained from .csv cache stored using the (Bayes_All()) debug script)
                   http://www.stat.yale.edu/Courses/1997-98/101/binom.htm
                   https://stats.stackexchange.com/questions/29641/standard-error-for-the-mean-of-a-sample-of-binomial-random-variables#:~:text=The%20standard%20error%20of%20%C2%AF,elsewhere%3A%20%E2%88%9Apqn

    Alim-Marvasti 2021
    """
    if num_df is None:
            raise Exception("No patient numbers or datapoints DataFrame passed to combine semiologies")
    if from_marginals:
        # get marginal probabilities: p per GIF is the same across semios

        marginal_dir = resources_dir / 'Bayesian_resources'
        if normalise:
            marginal_path = marginal_dir / 'p_GIF_norm.csv'
        if not normalise:
            marginal_path = marginal_dir / 'p_GIF_notnorm.csv'
        # load and clean:
        p_GIF = pd.read_csv(marginal_path, index_col=0)
        p_GIF.fillna(0, inplace=True)
        p_GIF = p_GIF.T
        p_GIF['GIF'] = p_GIF.index
        p_GIF = p_GIF.astype({'GIF':int})
        p_GIF.set_index(p_GIF['GIF'], inplace=True)
        p_GIF.drop(columns='GIF', inplace=True)
        p_GIF = p_GIF.T
        p_1_minus_p = p_GIF * (1 - p_GIF)
        # now repeat p_1_minus_p marginals as many times as there are semios and rename, ready for division:
        p_1_minus_p = p_1_minus_p.loc[p_1_minus_p.index.repeat(df.shape[0])]
        # If the frequencies of the occurence of semiologies are equal, results in simple mean between the semiology proportions.
        p_1_minus_p.reset_index(drop=True, inplace=True)
        p_1_minus_p.rename(index={i:semio for i, semio in zip((range(0, df.shape[0])), df.index) }, inplace=True)
    elif not from_marginals:
        # use actual frequencies per semiology as the probability, which is more a posterior likelihood. Has different probabilities per GIF per semio.
        p_1_minus_p = df * (1-df)
    n = num_df.sum(axis=0)  # sum each semiology separately as number of trials
    variances_df = p_1_minus_p.div(n, axis='index')
    inv_variances_df = 1 / variances_df
    inv_var_weighted_df = (df / variances_df)
    combined_df = (inv_var_weighted_df.sum(axis=0)) / (inv_variances_df.sum(axis=0))

    return combined_df
