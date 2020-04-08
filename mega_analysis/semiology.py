import warnings
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict

import yaml
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from mega_analysis.crosstab.mega_analysis.melt_then_pivot_query import melt_then_pivot_query
from mega_analysis.crosstab.mega_analysis.pivot_result_to_pixel_intensities import pivot_result_to_pixel_intensities
from mega_analysis.crosstab.mega_analysis.mapping import pivot_result_to_one_map
from mega_analysis.crosstab.mega_analysis.MEGA_ANALYSIS import MEGA_ANALYSIS
from mega_analysis.crosstab.mega_analysis.QUERY_SEMIOLOGY import QUERY_SEMIOLOGY
from mega_analysis.crosstab.mega_analysis.QUERY_LATERALISATION import QUERY_LATERALISATION
from mega_analysis.crosstab.mega_analysis.exclusions import (
    exclusions,
    exclude_ET,
    exclude_sEEG,
    exclude_cortical_stimulation,
    exclude_seizure_free,
)


# Define paths
repo_dir = Path(__file__).parent.parent
resources_dir = repo_dir / 'resources'
excel_path = resources_dir / 'syst_review_single_table.xlsx'
semiology_dict_path = resources_dir / 'semiology_dictionary.yaml'


# Read Excel file only three times at initialisation
mega_analysis_df, _, _ = MEGA_ANALYSIS(excel_data=excel_path)
map_df_dict = pd.read_excel(
    excel_path,
    header=1,
    sheet_name=['GIF TL', 'GIF FL', 'GIF PL', 'GIF OL', 'GIF CING', 'GIF INSULA', 'GIF CEREBELLUM']
)
gif_lat_file = pd.read_excel(
    excel_path,
    header=0,
    sheet_name='Full GIF Map for Review '
)

# Read lateralities for GUI
neutral_only_path = resources_dir / 'semiologies_neutral_only.txt'
neutral_also_path = resources_dir / 'semiologies_neutral_also.txt'
semiologies_neutral_only = neutral_only_path.read_text().splitlines()
semiologies_neutral_also = neutral_also_path.read_text().splitlines()


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
            include_seizure_freedom: bool = True,
            include_concordance: bool = True,
            include_seeg: bool = True,
            include_cortical_stimulation: bool = True,
            include_et_topology_ez: bool = True,
            possible_lateralities: Optional[List[Laterality]] = None,
            ):
        self.term = term
        self.symptoms_side = symptoms_side
        self.dominant_hemisphere = dominant_hemisphere
        self.data_frame = self.remove_exclusions(
            mega_analysis_df,  # global variable
            include_seizure_freedom,
            include_concordance,
            include_seeg,
            include_cortical_stimulation,
            include_et_topology_ez,
        )
        if possible_lateralities is None:
            possible_lateralities = get_possible_lateralities(self.term)
        self.possible_lateralities = possible_lateralities

    @staticmethod
    def remove_exclusions(
            df: pd.DataFrame,
            include_seizure_freedom: bool,
            include_concordance: bool,
            include_seeg: bool,
            include_cortical_stimulation: bool,
            include_et_topology_ez: bool,
            ) -> pd.DataFrame:
        if not include_concordance:
            df = exclusions(df, CONCORDANCE=True)
        if not include_seizure_freedom:
            df = exclude_seizure_free(df)
        if not include_et_topology_ez:
            df = exclude_ET(df)
        if not include_seeg:
            df = exclude_sEEG(df)
        if not include_cortical_stimulation:
            df = exclude_cortical_stimulation(df)
        return df

    def query_semiology(self) -> pd.DataFrame:
        if self.term in all_semiology_terms:
            path = semiology_dict_path
        else:
            path = None
        inspect_result = QUERY_SEMIOLOGY(
            self.data_frame,
            semiology_term=self.term,
            semiology_dict_path=path,
        )
        return inspect_result

    def query_lateralisation(self) -> Optional[pd.DataFrame]:
        query_semiology_result = self.query_semiology()
        all_combined_gifs = QUERY_LATERALISATION(
            query_semiology_result,
            self.data_frame,
            map_df_dict,
            gif_lat_file,
            side_of_symptoms_signs=self.symptoms_side.value,
            pts_dominant_hemisphere_R_or_L=self.dominant_hemisphere.value,
        )

        if all_combined_gifs is None:
            pivot_result = melt_then_pivot_query(
                mega_analysis_df,
                query_semiology_result,
                self.term,
            )
            all_combined_gifs = pivot_result_to_one_map(
                pivot_result,
                suppress_prints=True,
                map_df_dict=map_df_dict,
            )

        return all_combined_gifs

    def get_num_patients_dict(self) -> Optional[dict]:
        query_lateralisation_result = self.query_lateralisation()
        if query_lateralisation_result is None:
            message = f'No results generated for semiology term "{self.term}"'
            raise ValueError(message)
        array = np.array(query_lateralisation_result)
        _, labels, patients = array.T
        num_patients_dict = {
            int(label): float(num_patients)
            for (label, num_patients)
            in zip(labels, patients)
        }
        return num_patients_dict


def get_possible_lateralities(term) -> List[Laterality]:
    lateralities = [Laterality.LEFT, Laterality.RIGHT]
    if term in semiologies_neutral_only:  # global variable
        lateralities = [Laterality.NEUTRAL]
    elif term in semiologies_neutral_also:  # global variable
        lateralities.append(Laterality.NEUTRAL)
    return lateralities


def combine_semiologies(
        semiologies: List[Semiology],
        normalise: bool = True,
        ) -> Dict[int, float]:
    df = get_df_from_semiologies(semiologies)
    if normalise:
        df = normalise_semiologies_df(df)
    scores_dict = combine_semiologies_df(df, normalise=normalise)
    return scores_dict


def get_df_from_semiologies(semiologies: List[Semiology]) -> pd.DataFrame:
    num_patients_dicts = {}
    for semiology in semiologies:
        num_patients_dict = semiology.get_num_patients_dict()
        if num_patients_dict is None:
            message = (
                f'Information for semiology term "{semiology.term}"'
                ' could not be retrieved'
            )
            warnings.warn(message)
        else:
            num_patients_dicts[semiology.term] = num_patients_dict
    df = get_df_from_dicts(num_patients_dicts)
    return df


def get_df_from_dicts(
        semiologies_dicts: Dict[str, Dict[int, float]],
        ) -> pd.DataFrame:
    records = []
    for term, num_patients_dict in semiologies_dicts.items():
        num_patients_dict['Semiology'] = term
        records.append(num_patients_dict)
    df = pd.DataFrame.from_records(records, index='Semiology')
    return df


def normalise_semiologies_df(semiologies_df: pd.DataFrame) -> pd.DataFrame:
    table = np.array(semiologies_df)
    data = table.T
    scaler = MinMaxScaler((0, 100))
    scaler.fit(data)
    normalised = scaler.transform(data).T
    normalised_df = pd.DataFrame(
        normalised,
        columns=semiologies_df.columns,
        index=semiologies_df.index,
    )
    return normalised_df


def combine_semiologies_df(
        df: pd.DataFrame,
        normalise: bool = True,
        ) -> Dict[int, float]:
    combined_df = df.sum()
    if normalise:
        combined_df = combined_df / combined_df.max() * 100
    scores_dict = dict(combined_df)
    return scores_dict
